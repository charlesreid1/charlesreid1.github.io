Title: Recursive Backtracking in Go for Bioinformatics Applications: 2. Generating Variations
Date: 2018-12-30 18:00
Category: Rosalind
Tags: go, golang, rosalind, bioinformatics, recursion, backtracking, strings, combinatorics
Status: draft

_This is the second in a series of three blog posts describing our
solution to a bioinformatics problem from Rosalind.info,
[Problem BA1(i) (Find most frequent words with mismatches
in a string)](http://rosalind.info/problems/ba1i/).
To solve this problem and generate variations of a DNA string
as required, we implemented a recursive backtracking method
in the Go programming language._

* _[Part 1: Counting Variations](#)_
* _Part 2: Generating Variations (you are here)_
* _[Part 3: Go Implementation of Recursive Backtracking](#)_

<br />
<br />

<a name="toc"></a>
## Table of Contents

* [Problem Description](#problem-descr)
* [Permutations vs Combinations vs Variations](#perms-combs-vars)
* [Transforming the Problem Space](#transform)
    * [Generating Binary Numbers With Constraints](#binary)
    * [Bitvectors](#bitvectors)
    * [Recursion](#recursion)
* [Recursive Backtracking Pseudocode](#backtracking)
* [Appying to DNA Variations](#dna)
    * [Generating Visits](#generating-visits)
    * [Assembling the Variation](#assembling)

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
formulas. (See [Permutations](#)
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
binary numbers, which are often well-covered and easier
to think about. 

To generate variations, we can break up the process of
producing a variation into two steps, or choices, and
then convert these choices and the process of making them
into an equivalent problem in terms of binary numbers.

For example, if we think about the first step of creating
variations of a DNA string, the first choice we make is 
which codons to edit. 

Consider the case of an input string of DNA "AAAAA" and
$d = 1$. Then we can use a binary number as a "mask" to
indicate which codon we will edit. For example, if we 
pick the first codon, that is reprsented by the binary
number `10000`. Then the task of selecting a codon to
edit becomes the task of generating 5-digit binary 
numbers with only one 1:

```plain
00001
00010
00100
01000
10000
```

<a name="list"></a>
## List of Techniques

Want to have an algorithm that will allow us to iterate over
every possible variation. This requires us to implement an
algorithm that can:

* Choose $d$ codons to modify from an input DNA string of length $n$
* Swap out codons at these indices in every possible combination

A general strategy is to reduce the problem to one
involving binary numbers, which can be implemented
in any decent programming language, are compact and 
simple, and translate the problem into a more universal
language of binary numbers.

<a name="binary">></a>
### Generating Binary Numbers with Constraints

To generate the codons to modify,
want to generate numbers with $n$ digits
and $d$ bits (1s). We swap out the codons
at the positions with 1s.

Algorithm: [next bit permutation](https://graphics.stanford.edu/~seander/bithacks.html#NextBitPermutation)

<a name="bitvectors"></a>
### Bitvectors

More a brief aside than anything else, as this is a very
large topic that we don't have the space to cover,
but we should mention here that bitvectors are 
the data structure of choice for dealing with
binary numbers and manipulating them for the
algorithms covered here.

For more information, see the following:

* [Bitvector (wikipedia)](https://en.wikipedia.org/wiki/Bit_array)
* [Bit Twiddling Hacks](https://graphics.stanford.edu/~seander/bithacks.html)

<a name="recursion"></a>
### Recursion

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
## Recursive Backtracking Pseudocode

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
### Generating Visits

<a name="assembling"></a>
### Assembling the Variation


