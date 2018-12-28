Title: Recursive Backtracking in Go for Bioinformatics Applications: 3. Go Implementation of Backtracking
Date: 2018-01-02 18:00
Category: Rosalind
Tags: go, golang, rosalind, bioinformatics, recursion, backtracking, strings, combinatorics
Status: draft

_This is the third in a series of three blog posts describing our
solution to a bioinformatics problem from Rosalind.info,
[Problem BA1(i) (Find most frequent words with mismatches
in a string)](http://rosalind.info/problems/ba1i/).
To solve this problem and generate variations of a DNA string
as required, we implemented a recursive backtracking method
in the Go programming language._

* _[Part 1: Counting Variations](#)_
* _[Part 2: Generating Variations](#)_
* _Part 3: Go Implementation of Recursive Backtracking (you are here)_

<br />
<br />

<a name="toc"></a>
## Table of Contents

* [Problem Description](#problem-descr)

* [Recursive Backtracking Pseudocode](#backtracking)
    * [Incorporating Go Routines](#go-routines)
    * [Incorporating Go Channels](#channels)

* [Recursive Backtracking: Go Implementation](#go-implementation)
    * [Visit Hamming Neighbors Method](#visit-hamming)
    * [Assemble Visit Variation Method](#assemble-visit)

* [Examples and Usage](#examples)
    * [Tests](#tests)

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

<br />
<br />

<a name="backtracking"></a>
## Recursive Backtracking Pseudocode

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

<br />
<br />

<a name="go-implementation"></a>
## Recursive Backtracking: Go Implementation

<a name="visit-hamming"></a>
### Visit Hamming Neighbors Method

<a name="assemble-visit"></a>
### Assemble Visit Variation Method


<br />
<br />

<a name="examples"></a>
## Examples and Usage

<a name="tests"></a>
### Tests



