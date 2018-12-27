Title: Finding the Reverse Complement of a DNA String
Date: 2018-12-28 20:00
Category: Rosalind
Tags: go, golang, rosalind, bioinformatics
Status: draft

## Discussion of Problem

DNA string of base pairs

Reverse complement reverses the string and swaps AT, GC


## Brainstorming Possible Approaches

Iterative approach:
- iterate through each base pair, apply 4-case conditional
- if statements + exceptions
- map of key-value pairs

Other approaches:

Bitvector approach:
- mark positions where a particular base pair lives
- simple: e.g., A is 001000001000010001000
- applying a "mask"
- further simplifying, we really only need 3 (b/c know sum(a+t+g+c)=1)
- why is this approach useful? 
    - compact representation
    - easy to adapt
    - mark up segments of DNA with 0s 1s
    - can refer to original DNA
    - think of DNA like a library...
    - mask is like a bookmark (start here), plus a filter
- init: four bitvector masks, size of our DNA
- saving space: three bitvector masks, size of our DNA

Generalizing:
- mathematically, using "base 4" analogy: 0,1,2,3
- we can represent any base 4 number using 2 bits
- 00 = A, 01 = T, 10 = G, 11 = C, etc.
- now we have an alternative representation to the mask approach
- one bitvector mask, twice the size of our DNA
- storing numbers two bits at a time

This approach shows us that it is possible to store 
our base pairs using a more compact representation

Should be able to revisit bitvector approach and 
reduce it to two bitvectors:
- further trick: two bitvector masks
    - J one is AT(0) or GC(1)
    - K other is AG(0) or TC(1)
    - if J0 and K0, base pair is A
    - if J0 and K1, base pair is T
    - if J1 and K0, base pair is G
    - if J1 and K1, base pair is C

## Investingating Approaches

Investigating approaches:

Illustrate why this approach is inefficient.
How does it scale? 10 bp, 100 bp, 1000 bp, 1M bp.

In the next post we'll do some profiling to
investigate the reason for this big difference.

