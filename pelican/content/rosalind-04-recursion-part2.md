Title: Recursive Backtracking in Go for Bioinformatics Applications: 2. Generating Variations
Date: 2018-12-28 14:00
Category: Rosalind
Tags: go, golang, rosalind, bioinformatics, recursion, backtracking, strings, combinatorics

_This is the second in a series of three blog posts describing our
solution to a bioinformatics problem from Rosalind.info,
[Problem BA1(i) (Find most frequent words with mismatches
in a string)](http://rosalind.info/problems/ba1i/).
To solve this problem and generate variations of a DNA string
as required, we implemented a recursive backtracking method
in the Go programming language._

* _[Part 1: Counting Variations](https://charlesreid1.github.io/recursive-backtracking-in-go-for-bioinformatics-applications-1-counting-variations.html)_
* _Part 2: Generating Variations (you are here)_
* _[Part 3: Go Implementation of Recursive Backtracking](#)_

<br />
<br />

<a name="toc"></a>
## Table of Contents

* [Problem Description](#problem-descr)
* [Permutations vs Combinations vs Variations](#perms-combs-vars)
* [Recursion](#recursion)
    * [Recursive Backtracking Pseudocode](#backtracking)
* [Appying to DNA Variations](#dna)
    * [Generating Visits with Binary Numbers](#generating-visits)
    * [Assembling the Variation](#assembling)

<br />
<br />

<a name="problem-descr"></a>
## Problem Description

The task at hand is to take a given input strand of DNA,
and generate variations from it that have up to $d$ differences
(a Hamming distance of $d$) in the codons (base pairs).

In [part 1 of this series](https://charlesreid1.github.io/recursive-backtracking-in-go-for-bioinformatics-applications-1-counting-variations.html), we walk through the
construction of an analytical formula to count the number
of variations of a given DNA string that can be generated,
given the constraints of the problem.

In part 2 of this series, we cover several techniques to
generate variations on a DNA string, and present pseudocode
for the recursive backtracking method that we use here.

In part 3 of this series, we will cover our implementation
of the recursive backtracking method in the Go programming
language.

<a name="perms-combs-vars"></a>
## Permutations vs Combinations vs Variations

Before covering generation of variations of a DNA string,
we should cover some terminology for clarification.

If we were to use the term _permutations_, as in, we are
counting (or generating) _permutations_ of the input DNA string, 
that would imply that we were doing some kind of
rearrangement of the elements of the input DNA string
(for example, swapping two codons). This is not the
problem that we are solving, and requires different
formulas. (See [Permutations](http://mathworld.wolfram.com/Permutation.html)
entry on Wolfram MathWorld.)

The variations that we are referring to are not
exactly _combinations_, either, though. If we were
to use the term _combinations_, it would imply that
we were choosing a set of $k$ integers from a set
of $d$ integers ${1, 2, \dots, d}$.

The variations that we are counting are similar to
combinations, but with the additional act of swapping
out each codon at the position (integer) selected
with three other possible codons, so there are
more variations than combinations (and many
more permutations than variations).

<a name="transform"></a>
## Transforming the Problem Space

A surprisingly large variety of problems in combinatorics 
can be transformed into an equivalent problem involving 
binary numbers, which are usually easier to think about.

To generate variations, we can break up the process of
producing a variation into two steps, or choices, and
then convert these choices (and the process of making them)
into an equivalent problem in terms of binary numbers.

We can decompose the cration of a DNA string variation into
the first step of choosing which codons (indices) to edit, 
and the second step of cycling through every possible codon 
(ATGC) at the selected indices.

To translate this into an equivalent binary number problem,
consider the input string of DNA "AAAAA" and let the Hamming
distance that we are considering be $d = 1$. Then we can code
each index with a 0 (not chosen) or a 1 (chosen) and turn the
problem into cycling throgh all binary numbers with 1 bit:

```plain
00001
00010
00100
01000
10000
```

The second step is to cycle through each alternate codon at
the given position, so that `00001` would generate the 
variations:

```
AAAAC
AAAAG
AAAAT
```

and so on.

We saw this two-part technique already when counting the total number of
variations that could be created in [Part 1: Counting Variations](https://charlesreid1.github.io/recursive-backtracking-in-go-for-bioinformatics-applications-1-counting-variations.html).
It resulted in a counting formula with two terms, a binomial term
for step 1 and an exponential term for step 2.

We can think of the problem as forming a tree with several
decision nodes that need to be explored; this type of problem
structure is ideal for a recursive backtracking algorithm.

We will cover the use of recursive backtracking to actually
explore the entire tree of possible outcomes (not just count
it), starting with some review and background on recursive 
backtracking and how it works.

<a name="recursion"></a>
## Recursion

Recursion is a common pattern to use for problems that require
exploring a large problem space that requires us to make
several selections.

A recursive backtracking algorithm is analogous to exploring a
maze but laying out a rope as you go, so tht you can revisit
each possible route. In this case, we are using backtracking
to make the choice of which indices of the input DNA string
to modify. We want to explore all possible choices to generate
all possible variations of the input DNA string, and backtracking
gives us the framework to do that.

For example, if we wanted to recursively generate codon choices
for the case of an input DNA string like "AAAAA" and $d = 2$,
we would call a recursive method twice; the first time through,
we would choose one of the five indices, and mark it as picked;
then we would call the method again, and choose a second index
(different from the first) and mark it as picked.

When unrolled, this is equivalent to a nested for loop,

```plain
for i in range( 0 .. len(dna_string) ):
    for j in range( 0 .. len(dna_string) ):
        if (i != j):
            Start with the binary number 00000
            Set the digit at index i to 1
            Set the digit at index j to 1
```


<a name="backtracking"></a>
### Recursive Backtracking Pseudocode

Basic pseudocode for a backtracking method:

```
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

<a name="dna"></a>
## Applying to DNA Variations

There are actually two places where we need to apply
backtracking to our problem.

<a name="generating-visits"></a>
### Generating Visits with Binary Numbers

The first application of recursive backtracking is to
carry out step 1, choosing indices in the original
DNA string to modify or cycle through altnerate 
codons. We showed above how generating variations
on a kmer of length $k$ at a distance $d$ from the
original kmer was equivalent to generating binary 
numbers with $d$ bits set to 1.

We can use recursive backtracking to generate these
numbers. By creating a method that recursively selects
an index to switch to 1, and passing that (and all prior
choices) on to further recursive calls, the function
can recurse to a given depth $d$ and visit all possible
binary numbers with $d$ bits set to 1.

The base case of this recursive method would be reached
when all $d$ choices had been made and $d$ bits were 
set to 1. Then the choice of indices to swap out with
alternate codons would be passed on to a recursive method
that would carry out Step 2 (see below).

For example, to generate variations of the 5-mer `AAAAA`,
we would start by selecting a Hamming distance $d$, then
generate a binary number with $d$ bits set to 1 to select
indices to modify. Suppose $d = 2$; then the first few
binary numbers are:

```
AAAAA
11000
10100
10010
10001
...
```

To expand on the pseudocode a bit more, to generate a
binary number with $d$ bits flipped to 1 we will want
to call a recursive method with a depth of $d$, making
a choice at each recursive call of which index to set
to 1 next.

The $n^{th}$ recursive call picks the $n^{th}$ index for
1. Each index can only be chosen once in the stack of 
recursive calls, and the indices that have been chosen
by prior recursive function calls are passed along.

Thus we need a minimum of two parameters: an integer
indicating the depth level of this recursive function
call, and an integer array of index choices.

```
function generate_binary_numbers( depth, choices[], ... ):

    if depth is 0,
        base case
        no more choices left to make
        choices[] is full
        pass along choices[] to assemble the variations

    else,
        recursive case
        for each possible index,
            if this index is not already in choices,
                add this index to choices
                generate_binary_numbers( depth+1, choices[] )
                remove this index from choices
```

<a name="assembling"></a>
### Assembling the Variation

Each binary number is then turned into variations by substituting
every combination of 3 codons in every position with a 1
possible, so the first binary number for $d=2$ would generate
the variations:

```
AAAAA
11000
-----
CCAAA
GCAAA
TCAAA
CGAAA
GGAAA
TGAAA
CTAAA
GTAAA
TTAAA
```

This would be repeated for all Hamming distances up to the
maximum specified Hamming distance.

Like the generation of binary numbers, the substitution of all
possible combinations of codons at these positions is a
task conducive to a recursive backtracking algorithm.

Like the prior task's recursive method, this task's recursive 
method will have one parameter for depth (number of choices
left to make) and a range of choices to try (codons).

```
function assemble_variations( depth, choices[], ... ):

    if depth is 0,
        base case
        no more choices left to make
        choices[] is full
        pass along choices[] to assemble the variations

    else,
        recursive case
        for each possible index,
            if this index is not already in choices,
                add this index to choices
                generate_binary_numbers( depth+1, choices[] )
                remove this index from choices
```


In the last post we'll cover the actual Go implementation
of these functions.

