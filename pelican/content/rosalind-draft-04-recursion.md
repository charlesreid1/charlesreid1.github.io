Title: Backtracking and Recursion in Go: Generating String Permutations
Date: 2018-12-26 18:00
Category: Rosalind
Tags: go, golang, rosalind, bioinformatics, recursion, backtracking, strings, permutations, combinatorics
Status: draft

## Problem Statement

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

