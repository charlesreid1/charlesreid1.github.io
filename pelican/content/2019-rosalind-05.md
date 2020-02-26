Title: Recursive Backtracking in Go for Bioinformatics Applications: 3. Go Implementation of Backtracking
Date: 2019-01-03 10:30
Category: Computational Biology
Tags: go, golang, rosalind, computational biology, bioinformatics, recursion, backtracking, strings, combinatorics

_This is the third in a series of three blog posts describing our
solution to a bioinformatics problem from Rosalind.info,
[Problem BA1(i) (Find most frequent words with mismatches
in a string)](http://rosalind.info/problems/ba1i/).
To solve this problem and generate variations of a DNA string
as required, we implemented a recursive backtracking method
in the Go programming language._

* _[Part 1: Counting Variations](https://charlesreid1.github.io/recursive-backtracking-in-go-for-bioinformatics-applications-1-counting-variations.html)_
* _[Part 2: Generating Variations](https://charlesreid1.github.io/recursive-backtracking-in-go-for-bioinformatics-applications-2-generating-variations.html)_
* _[Part 3: Go Implementation of Recursive Backtracking](https://charlesreid1.github.io/recursive-backtracking-in-go-for-bioinformatics-applications-3-go-implementation-of-backtracking.html)_

[TOC]

## Problem Description

The task at hand is to take a given input strand of DNA,
and generate variations from it that have up to $d$ differences
(a Hamming distance of $d$) in the codons (base pairs).

In [part 1 of this series](https://charlesreid1.github.io/recursive-backtracking-in-go-for-bioinformatics-applications-1-counting-variations.html), we walk through the
construction of an analytical formula to count the number
of variations of a given DNA string that can be generated,
given the constraints of the problem.

In [part 2 of this series](https://charlesreid1.github.io/recursive-backtracking-in-go-for-bioinformatics-applications-2-generating-variations.html), we cover several techniques to
generate variations on a DNA string, and present pseudocode
for the recursive backtracking method that we use here.

In [part 3 of this series](https://charlesreid1.github.io/recursive-backtracking-in-go-for-bioinformatics-applications-3-go-implementation-of-backtracking.html), we will cover our implementation
of the recursive backtracking method in the Go programming
language.

<br />
<br />

<a name="backtracking"></a>
## Recursive Backtracking Pseudocode

To review from the prior post, our pseudocode
for recursive backtracking to explore variations
or combinations looks like the following:

```text
explore method:
    base case:
        visit this solution
    recursive case:
        for each available choice:
            make a choice
            explore outcomes
            unmake the choice
            move on to the next choice
```

The key elements there are the base and recursive
cases, and the mechanism of iterating over each
possible choice and making/exploring/unmaking
the choice.


<a name="go-implementation"></a>
## Recursive Backtracking: Go Implementation

In total, we have three different methods to
accomplish this task:

* `VisitHammingNeighbors(input,d)`: this is the public method
  that the user calls to generate a string array of all
  strings that are a Hamming distance of up to `d` from
  the input string `input`. This public method performs
  parameter and error checking, initializes space for
  data, and collects results.

* `visitHammingNeighbors_recursive(base_kmer, depth, choices, results_map)`:
  this method is the private recursive method available
  only to the package. This method performs the actual
  recursive work. 

**NOTE:** the function name starts with a lower case letter,
so it is not exported by the package - i.e., it is not available
to the user when they import this package.

The base case of the `visitHammingNeighbors_recursive()`
function will pass the final set of choices to the final
step:

* `assemble_variations(base_kmer, choices, results_map)`: 
  this method (private to the package) is a recursive
  method that uses the chosen indices and 


<a name="visit-hamming"></a>
### Visit Hamming Neighbors Function

The function call to visit all Hamming neighbors and add them to the `results` set
is split into two parts: a non-recursive public function, which provides a public wrapper
that is user-friendly and performs error-checking on the parameters provided, and a
recursive private function that is used internally but not intended to be called by
users directly.

#### Public, Non-Recursive Function

Here is the entry point function that the user calls
when they wish to generate all variations on a given
string of DNA, and have the variations returned as a
string slice.

```go
// Given an input string of DNA, generate variations
// of said string that are a Hamming distance of
// less than or equal to d.
func VisitHammingNeighbors(input string, d int) (map[string]bool, error) {

	// a.k.a. visit_kmer_neighbors

	// number of codons
	n_codons := 4

	// Use combinatorics to calculate the total
	// number of variation.
	buffsize, _ := CountHammingNeighbors(len(input), d, n_codons)
```

The call to `CountHammingNeighbors()` uses the counting
formula from [Part 1](https://charlesreid1.github.io/recursive-backtracking-in-go-for-bioinformatics-applications-1-counting-variations.html)
to predict the number of variations. If the user has selected
an astronomical problem size, the program warns the user.

```go
	// This blows up quickly, so warn the user
	// if their problem is too big
	MAX := int(1e6)
	if buffsize > MAX {
		msg := fmt.Sprintf("Error: you are generating over MAX = %d permutations, you probably don't want to do this.", d)
		return nil, errors.New(msg)
	}
```

Now the actual recursive backtracking algorithm begins.
The code loops over every possible value of Hamming distance
$d$ and calls the recursive method at each value of $d$.

```go
	// Store the final results in a set (string->bool map)
	results := make(map[string]bool)

    // Begin backtracking algorithm
	for dd := 0; dd <= d; dd++ {

		// The choices array will change with each recursive call.
		// Go passes all arguments by copy, which is good for us.
		choices := []int{}

		// Populate list of neighbors
		visitHammingNeighbors_recursive(input, dd, choices, results)

	}
```

We don't assign any results from the call to `visitHammingNeighbors_recursive()`
because we pass in a data structure (actually a pointer to a
data structure), `results`, that is modified in-place.

Thus, when we complete a call to `visitHammingNeighbors_recursive()`,
results will contain all variations already.

```go
	// Check if we have the right number of results
	if len(results) != buffsize {
		fmt.Printf("WARNING: number of results (%d) did not match expected value (%d)\n", len(results), buffsize)
	}

    return results
}
```

#### Private, Recursive Function

In the above function, the call to the recursive
function to visit all Hamming neighbors happens
here:

```go
		// Populate list of neighbors
		visitHammingNeighbors_recursive(input, dd, choices, results)
```

The user passes the original kmer `input`, along with the
Hamming distance parameter `dd`, the list of choices
of indices that have already been selected `choices`,
and the data structure storing all resulting strings
`results`.

As with the pseudocode, we have a base case and 
a recursive case. The recursive function is being
called repeatedly until it reaches a depth of 0,
with the depth parameter being decremented each call.

```go
// Recursive function: given an input string of DNA,
// generate Hamming neighbors that are a Hamming
// distance of exactly d. Populate the neighbors
// array with the resulting neighbors.
func visitHammingNeighbors_recursive(base_kmer string, depth int, choices []int, results map[string]bool) error {

	if depth == 0 {

		// Base case

	} else {

		// Recursive case

    }
}
```

The base case occurs when we reach a depth of 0 and have
no further choices to make. We reach this base case for
each binary number with $d$ digits set to 1; once the base
case is reached, we call the `assemble_variations()` function
to substitute all possible codons at the selected indices.

```go
func visitHammingNeighbors_recursive(base_kmer string, depth int, choices []int, results map[string]bool) error {

	if depth == 0 {

		// Base case
		assemble_variations(base_kmer, choices, results)
		return nil

```

The recursive case is slightly more complicated, but it follows
the same backtracking pseudocode covered previously: from a set
of possible choices, try each choice, recursively call this 
function, then unmake the choice and move on to the next choice.

Here, the choice is which index `c` in the kmer to modify. Each
kmer can only be modified once, so we have a for loop to
check if the index `c` is in the list of choices already made.

```go
	} else {

		// Recursive case
		for c := 0; c <= len(base_kmer); c++ {

			var indexAlreadyTaken bool
			for _, choice := range choices {
				if c == choice {
					indexAlreadyTaken = true
				}
			}
```

As before, the recursive call to this function will
not return any values that need to be stored, since 
`results` points to a data structure (map) that is 
modified in-place.

```go
			if !indexAlreadyTaken {

				// This will make a new copy of choices
				// for each recursive function call
				choices2 := append(choices, c)
				err := visitHammingNeighbors_recursive(base_kmer, depth-1, choices2, results)
				if err != nil {
					return err
				}

			}
		}

	}

	return nil
}
```

<a name="assemble-visit"></a>
### Assemble Visit Variation Function

Once we've generated each list of indices to modify,
we call a second recursive function to substitute each
codon into each index.

In the recursive method above, each recursive function
call added a new choice to `choices`; in this recursive
function, each recursive funcction call pops a choice 
from `choices`. Thus, the base case is when `choices`
is empty.

Here are the base and recursive cases:

```go
// Given a base kmer and a choice of indices where
// the kmer should be changed, generate all possible
// variations on this base_kmer.
func assemble_variations(base_kmer string, choices []int, results map[string]bool) {

	if len(choices) > 0 {

        // Recursive case
        ...

	} else {

        // Base case
        ...

	}
}
```

The recursive case pops a choice from `choices`, 
finds which nucleotide (AGCT) is at that location,
and assembles the list of possible choices (the
other 3 nucleotide values). It then performs
the recursive backtracking algorithm, choosing 
from each of the three possible nucleotide values,
exploring the choice by making a recursive call,
then un-making the choice.

```go
func assemble_variations(base_kmer string, choices []int, results map[string]bool) {

	if len(choices) > 0 {

        // Recursive case

		all_codons := []string{"A", "T", "G", "C"}

		// Pop the next choice
		// https://github.com/golang/go/wiki/SliceTricks
		ch_ix, choices := choices[0], choices[1:]

		// Get the value of the codon at that location
		if ch_ix < len(base_kmer) {
			// slice of string is bytes,
			// so convert back to string
			this_codon := string(base_kmer[ch_ix])
			for _, codon := range all_codons {

				if codon != this_codon {
					// Swap out the old codon with the new codon
					new_kmer := base_kmer[0:ch_ix] + codon + base_kmer[ch_ix+1:]
					assemble_variations(new_kmer, choices, results)
				}
			}
		}

	} else {

        // Base case
		results[base_kmer] = true

	}
}
```

<br />
<br />

<a name="tests"></a>
## Tests

The last step after some debugging was to write tests for the
function to generate all variations of a DNA string, to ensure
the recursive backtracking functions work correctly.

The pattern we use is to create a struct containing test parameters,
then create a test matrix by initializing instances of the
parameter struct with the parameters we want to test.

Here is how we set up the tests:

```go
func TestMatrixVisitHammingNeighbors(t *testing.T) {
	var tests = []struct {
		input string
		d     int
		gold  []string
	}{
		{"AAA", 1,
			[]string{"AAC", "AAT", "AAG", "AAA", "CAA", "GAA", "TAA", "ATA", "ACA", "AGA"},
		},
	}
	for _, test := range tests {

        ...

	}
}
```

Each test case should generate all Hamming neighbors, and compare to the list of
Hamming neighbors provided. This requires two tricks:

- sort before comparing, to ensure a proper comparison
- use a custom `EqualStringSlices()` function that will iterate through
  two string slices element-wise to check if they are equal.

The `EqualStringSlices()` function is required because Go does not have 
built-in equality checks for slices.

Here is what the tests look like:

```go
	for _, test := range tests {

		// Money shot
		result, err := VisitHammingNeighbors(test.input, test.d)

		// Check if there was error
		if err != nil {
			msg := fmt.Sprintf("Error: %v", err)
			t.Error(msg)
		}

		// Sort before comparing
		sort.Strings(test.gold)
		sort.Strings(result)

		if !EqualStringSlices(result, test.gold) {
			msg := fmt.Sprintf("Error testing VisitHammingNeighbors():\ncomputed = %v\ngold     = %v",
				result, test.gold)
			t.Error(msg)
		}
    }
```

<a name="final"></a>
## Final Code

The final version of the recursive function to visit all Hamming neighbors
and return them in a string array can be found in the `go-rosalind` library
on Github.

Specifically, in the file [`rosalind_ba1.go`](https://github.com/charlesreid1/go-rosalind/blob/master/rosalind/rosalind_ba1.go),
there is a [`VisitHammingNeighbors()`](https://github.com/charlesreid1/go-rosalind/blob/master/rosalind/rosalind_ba1.go#L711)
function that is the public function that calls the private recursive
function [`visitHammingNeighbors_recursive()`](https://github.com/charlesreid1/go-rosalind/blob/master/rosalind/rosalind_ba1.go#L778),
and the recursive function to swap out codons is
in the [`visit()`](https://github.com/charlesreid1/go-rosalind/blob/master/rosalind/rosalind_ba1.go#L819)
funciont.

<a name="fruitful"></a>
## Go Forth and Be Fruitful

Now that you have the basic tools to imlement a recursive
backtracking algorithm in Go to generate string variations,
you have one of the key ingredients to solve Rosalind.info
problem [BA1i, "Find Most Frequent Words with Mismatches by
String"](http://rosalind.info/problems/ba1i/).

This problem is tricky principally because it requires generating
every DNA string variation, so now you should have the key
ingredient to solve BA1i (and several problems that follow).

You can use the final version of the methods we covered by importing
the `go-rosalind` library in your Go code
([link to go-rosalind documentation on godoc.org](https://godoc.org/github.com/charlesreid1/go-rosalind/rosalind))
or you can implement your own version of these algorithms. 
The Go code we covered in this post is also on Github in the
[charlesreid1/go-rosalind](https://github.com/charlesreid1/go-rosalind) repository.

