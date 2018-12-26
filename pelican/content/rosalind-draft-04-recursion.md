Title: Recursive Backtracking in Go for Bioinformatics Applications: 1. Counting Variations
Date: 2018-12-26 18:00
Category: Rosalind
Tags: go, golang, rosalind, bioinformatics, recursion, backtracking, strings, combinatorics
Status: draft

This is the first in a series of blog posts describing our
solution to a bioinformatics problem from Rosalind.info,
[Problem BA1(i) (Find most frequent words with mismatches
in a string)](http://rosalind.info/problems/ba1i/).
To solve this problem and generate variations of a DNA string
as required, we implemented a recursive backtracking method
in the Go programming language.

The task at hand is to take a given input strand of DNA,
and generate variations from it that have up to $d$ differences
in the codons (base pairs). 

In [part 1 of this series (you are here)](#toc), we walk through the
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

<br />
<br />

<a name="toc"></a>
## Table of Contents

* [Problem Description](#problem-descr)
* [Counting Permutations](#counting-permutations)
    * [Deriving the Formula](#deriving)
    * [Term 1: Picking DNA Indices](#indices)
    * [Term 1: Side Note on Ordering](#side-note)
    * [Term 2: Modifying DNA Codons](#modifying)
* [Useful Functions](#functions)
    * [Binomial Function](#binomial)
    * [Factorial Function](#factorial)
* [Final Counting Formula](#final)
* [Implementing in Go](#golang)

Addendum:

* [Why is it important to count permutations anyway?](#why)

<br />
<br />

<a name="problem-descr"></a>
## Problem Description

Given a string of DNA, generate all related DNA strings that are
less than or equal to a Hamming distance d from the given DNA
string.

<a name="counting-permutations"></a>
## Counting Permutations

What we want is a formula to count the number of permutations

TO derive a formula, helps to think through the problem
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

We are given a Hamming distance of d

Input DNA string of length n

One Hamming distance unit requires/occupies one base pair

(basically a binary switch, one per index, that indicates
whether we are modifying this index)

How many ways can we pick k things from a set of n.

n slots, k balls, one ball per slot.

n switches, k can be thrown.

Problem has a kind of triangular structure:

0 switches or n switches = 1 possible outcome

1 switch or n-1 switches = n possible outcomes

2 switches or n-2 switches = n(n-1) possible outcomes

etc.

Turns out this problem is common enough that there is a
special function just for describing the number of ways
of selecting k things from n choices.

n choose k.

binomial formula.

$$
binom(n,k) = n!/(k! (n-k)!)
$$

In the scenarios posed above, the order of our choices
did not matter - the balls were not numbered, the order
in which we threw each switch did not affect the outcome.

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



<br />
<br />

<a name="functions"></a>
## Useful Functions

<a name="factorial"></a>
### Factorial Function

<a name="binomial"></a>
### Binomial Function


<br />
<br />

<a name="final"></a>
## Final Counting Formula

The final formula for counting the number of variations $V$
of a given DNA string of length $n$ that are a Hamming
distance of up to $d$, with $c$ possible codons (A, T, G, C),
can be written as follows:

$$
V = \sum_{dd =0}^{d} \binom{n}{k} (c-1)^{n}
$$






Many ways to generate all possible strings...

* One family of methods comes from transorming strings into binary numbers,
  and converting process/constraints into binary number process/constraints

* Another approach that we will explore here recursively generates all possible
  permutations using a recursive backtracking method
