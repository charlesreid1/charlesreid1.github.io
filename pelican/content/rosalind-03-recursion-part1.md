Title: Recursive Backtracking in Go for Bioinformatics Applications: 1. Counting Variations
Date: 2018-12-26 18:00
Category: Rosalind
Tags: go, golang, rosalind, bioinformatics, recursion, backtracking, strings, combinatorics

_This is the first in a series of three blog posts describing our
solution to a bioinformatics problem from Rosalind.info,
[Problem BA1(i) (Find most frequent words with mismatches
in a string)](http://rosalind.info/problems/ba1i/).
To solve this problem and generate variations of a DNA string
as required, we implemented a recursive backtracking method
in the Go programming language._

* _Part 1: Counting Variations (you are here)_
* _[Part 2: Generating Variations](#)_
* _[Part 3: Go Implementation of Recursive Backtracking](#)_

<br />
<br />

<a name="toc"></a>
## Table of Contents

* [Problem Description](#problem-descr)
* [Useful Functions](#functions)
    * [Binomial Function](#binomial)
    * [Factorial Function](#factorial)
* [Counting Permutations](#counting-permutations)
    * [Deriving the Formula](#deriving)
    * [Term 1: Picking DNA Indices](#indices)
    * [Term 1: Side Note on Ordering](#side-note)
    * [Term 2: Modifying DNA Codons](#modifying)
* [Final Counting Formula](#final)
* [Implementing in Go](#golang)
    * [Binomial and Factorial Functions in Go](#golang-bionomial-factorial)
    * [Variations Counting Function in Go](#variations)

Addendum:

* [Why is it important to count permutations anyway?](#why)

<br />
<br />

<a name="problem-descr"></a>
## Problem Description

The task at hand is to take a given input strand of DNA,
and generate variations from it that have up to $d$ differences
(a Hamming distance of $d$) in the codons (base pairs).

In [part 1 of this series](#), we walk through the
construction of an analytical formula to count the number
of variations of a given DNA string that can be generated,
given the constraints of the problem.

In part 2 of this series, we cover several techniques to
generate variations on a DNA string, and present pseudocode
for the recursive backtracking method that we use here.

In part 3 of this series, we will cover our implementation
of the recursive backtracking method using two of Go's
unique features: channels, and Go routines. We implement
code that can utilize concurrency to generate variations
efficiently and collect results using a channel.



<a name="functions"></a>
## Useful Functions

It's always useful to review some basic mathematics
useful for combinatorics applications. We'll review
the factorial and binomial functions, which will
show up in our final formula for the total nubmer
of variations we will be generating.

<a name="factorial"></a>
### Factorial Function

The factorial function for an integer $n$ is written
$n!$ and is defined for $n \geq 1$ as:

$$
n! = n \cdot (n-1) \cdot \dots \cdot 2 \cdot 1
$$

for example, $5!$ would be:

$$
5! = 5 \times 4 \times 3 \times 2 \times 1 = 120
$$

<a name="binomial"></a>
### Binomial Function

The binomial function has many applications in combinatorics.
It is the number of ways of independently selecting $k$ items
from a set of $n$ items, and is written:

$$
\binom{n}{k} = \dfrac{ n! }{ k! (n-k)! }
$$

<br />
<br />

<a name="counting-permutations"></a>
## Counting Permutations

What we want is a formula to count the number of permutations

To derive a formula, it helps to think through the problem
starting with smaller special cases, and generalize 
from there in terms of the problem parameters.

<a name="deriving"></a>
### Deriving the Formula

The problem we're trying to solve is generating all perms
with hamming distance less than or equal to d, but let's
start with a simpler problem: generating all perms with 
hamming distance of exactly d.

Then we can just sum up over each d.

Start with a simple situation: string of dna with 3 codons.
Case of hamming distance 0 too trivial, so start with case of
hamming distance of 1.

There are two terms in our combinatorics formula that we
need to think about:

* **Term 1:** We have a certain number of codons to modify (this is fixed
  by the Hamming distance d that we pick). Term 1 counts up the
  number of ways of selecting which indices of the original 
  DNA string to modify.

* **Term 2:** Once we've picked out the indices we are going to modify, we
  have several variations for each index (4 total codons, so 3
  variations). Term 2 is a count of the number of variations that are
  possible, given the choice of indices in the original DNA string
  to modify.

The approach here is to think about these two terms
independently and separately. Each term has a formula
to count the number of possibilities indexed by each.
Then, because these are independent choices, the total
number of combined choices is the product of these two
terms.

<a name="indices"></a>
### Term 1: Picking DNA Indices

The first term in our formula for number of variations
will be the term representing the number of ways of 
choosing which indices in the original DNA input string
to edit.

Given a Hamming distance of $d$, and the fact that we
have one and only one edit (Hamming distance unit) per
base pair, Term 1 counts the number of ways of picking
$d$ items from a set of $n$ items. Order does not matter.

This problem is equivalent to having a row of $n$ on/off
switches, all in the off position, and counting the number
of ways of throwing exactly $d$ of them into the on position.

Likewise, it is equivalent to having $d$ identical colored balls, 
and counting the number of ways of placing them into $n$
slots, one ball per slot.

We can see how the problem has a kind of triangular structure.
Returning to the scenario of $n$ on/off switches:

* If we have $d = n$ switches to throw, or if we have 
  $d = 0$ switches to throw, in either case we have
  only 1 possible outcome.

* If we have $d = n-1$ switches to throw, or if we 
  have $d = 1$ switch to throw, either way we have
  $n$ possible outcomes

* If we have $d = n-2$ or $d = 2$ switches to throw,
  there are $n (n-1)$ possible outcomes; etc.

In fact, this problem - choosing $d$ things
from a set of $n$ things - is common enough that
there is a special function just to describe it,
and that's the binomial function (covered above).

The binomial function is defined as:

$$
\binom{n}{k} = \dfrac{ n! }{ k! (n-k)! }
$$

In the scenarios posed above, the order of our choices
did not matter - the balls were not numbered, the order
in which we threw each switch did not affect the outcome.

If the order did matter, if the order in which the on/off
switches were thrown mattered or if the balls that were
placed into slots had sequential numbers on them, then we
would need a different function - the expression above 
to count the number of outcomes would not have a $k!$ in 
the denominator.


<a name="side-note"></a>
### Term 1: Side Note on Ordering

If the order of the index choices does not matter, 
the $k!$ term in the denominator must be included 
to cancel out double-counting in the situations where
(for example) $i$ is chosen first and $j$ is chosen second,
and then the situation where $j$ is chosen first and $i$
is chosen second.

If the $k!$ term is present in the denominator, it says
that the order in which items are selected does not matter,
in which case we are generating _combinations_.

To count combinations, use the "n choose k" function. See the 
[Combination](http://mathworld.wolfram.com/Combination.html)
article on Wolfram MathWorld.

If the $k!$ term is _not_ present in the denominator, it says
that the order in which items are selected does matter,
in which case we are generating _permutations_.

To count permutations, use the "n pick k" function. See the 
[Permutation](http://mathworld.wolfram.com/Permutation.html)
article on Wolfram MathWorld.

<a name="modifying"></a>
### Term 2: Modifying DNA Codons

Once we've selected the $d$ indices in the original DNA
string that we are going to modify, we have to count the
number of ways those base pairs can be modified.

We have $d$ base pairs to modify, and $c = 4$ total
codons (ATGC). Each base pair that we are modifying
has $c-1$ possible codons that it we can swap it out
with, and each choice is independent, so the number
of possibile outcomes (Term 2) is:

$$
(c-1)^{d}
$$

<br />
<br />

<a name="final"></a>
## Final Counting Formula

To write the final formula for counting the number of variations $V$
of a given DNA string of length $n$ that are a Hamming
distance of less than or equal to $d$, with $c$ possible codons 
(A, T, G, C), we will need to sum over Hamming distances
from 0 to $d$:

$$
V = \sum_{k = 0}^{d} \binom{n}{k} (c-1)^{k}
$$

<a name="golang"></a>
## Implementing in Go

Now, let's look at how we would implement this counting
formula in Go. This will be useful, since programs run 
much faster when they are able to allocate all the sapce
they need in memory ahead of time. Counting the number
of variations of our DNA input string will allow us to
do just that.

<a name="golang-binomial-factorial"></a>
### Binomial and Factorial Functions in Go

We'll start with binomial and factorial functions in Go:
continuing with our theme of recursion, we implement
a recursive factorial function.

```go
// Compute the factorial of an integer.
func Factorial(n int) int {
	if n < 2 {
		// base case
		return 1
	} else {
		// recursive case
		return n * Factorial(n-1)
	}
}
```

The factorial function will behave correctly for the
case of $n=1$ and $n=0$, and will return 1 if $n$ is
negative (which is reasonable behavior for our purposes.)

The binomial function utilizes the factorial function:

```go
// Returns value of the binomial coefficient Binom(n, k).
func Binomial(n, k int) int {

	result := 1

	// Since C(n, k) = C(n, n-k)
	if k > (n - k) {
		k = n - k
	}

	// Calculate value of:
    //
	// ( n * (n-1) * ... * (n-k+1) )
	// -----------------------------
	//   ( k * (k-1) * ... * 1 )
    // 
	for i := 0; i < k; i++ {
		result *= n - i
		result /= i + 1
	}

	return result
}
```

(Note that we might want to add some additional error checks to the
`Binomial()` function.)

<a name="variations"></a>
### Variations Counting Function in Go

Now we can put everything together into a function to count
the number of "Hamming neighbors" - variations on a given 
DNA string that are a Hamming distance of up to $d$ away
from the original DNA string.

To count the number of Hamming neighbors, we implement
the formula above. We leave out the error checks on the
parameter values here, for brevity.

```go
// Given an input string of DNA of length n,
// a maximum Hamming distance of d,
// and a number of codons c, determine
// the number of Hamming neighbors of
// distance less than or equal to d
// using a combinatorics formula.
func CountHammingNeighbors(n, d, c int) (int, error) {

    // We require the following:
    // n > 0
    // d >= 0
    // c > 0

	// Use combinatorics to calculate number of variations
	nv := 0
	for dd := 0; dd <= d; dd++ {

		// Binomial(n,d) => number of ways we can
		//                  pick codons to edit
		next_term := Binomial(n, dd)

		// (c-1)^d => number of ways that the codons
		//            we picked to edit can be edited
		for j := 0; j < dd; j++ {
			next_term *= (c - 1)
		}
		nv += next_term
	}
	return nv, nil
}
```



