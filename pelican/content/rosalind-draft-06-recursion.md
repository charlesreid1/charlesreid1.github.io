Title: Recursive Backtracking in Go for Bioinformatics Applications: 3. Go Implementation of Backtracking
Date: 2018-12-27 18:00
Category: Rosalind
Tags: go, golang, rosalind, bioinformatics, recursion, backtracking, strings, combinatorics
Status: draft

This is the third in a series of blog posts describing our
solution to a bioinformatics problem from Rosalind.info,
[Problem BA1(i) (Find most frequent words with mismatches
in a string)](http://rosalind.info/problems/ba1i/).
To solve this problem and generate variations of a DNA string
as required, we implemented a recursive backtracking method
in the Go programming language.

The task at hand is to take a given input strand of DNA,
and generate variations from it that have up to $d$ differences
in the codons (base pairs). 

In part 1 of this series, we walk through the
construction of an analytical formula to count the number
of variations of a given DNA string that can be generated,
given the constraints of the problem.

In part 2 of this series, we cover several techniques to
generate variations on a DNA string, and present pseudocode
for the recursive backtracking method that we use here.

In [part 3 of this series (you are here)](#toc), we will cover our implementation
of the recursive backtracking method using two of Go's
unique features: channels, and Go routines. We implement
code that can utilize concurrency to generate variations
efficiently and collect results using a channel.

<br />
<br />

<a name="toc"></a>
## Table of Contents

* [Problem Description](#problem-descr)

* [Recursive Backtracking Pseudocode](#backtracking)
    * [Incorporating Go Routines](#go-routines)
    * [Incorporating Go Channels](#channels)

* [Recursive Backtracking: Go Implementation](#backtracking)
    * [Visit Hamming Neighbors Method](#visit-hamming)
    * [Assemble Visit Variation Method](#assemble-visit)

* [Examples and Usage](#examples)
    * [Tests](#tests)

<br />
<br />

<a name="problem-descr"></a>
## Problem Description

Given a string of DNA, generate all related DNA strings that are
less than or equal to a Hamming distance d from the given DNA
string.

Many ways to generate all possible strings...

* One family of methods comes from transorming strings into binary numbers,
  and converting process/constraints into binary number process/constraints

* Another approach that we will explore here recursively generates all possible
  permutations using a recursive backtracking method

## Counting Permutations

Formula to count permutations

Break down the method:

* Count number of positions where we can modify codon
* Multiply by number of possibilities given the positions we have chosen



