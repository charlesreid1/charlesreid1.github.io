Title: Project Euler 60: Finding Five Primes That Concatenate to Primes
Date: 2025-04-14 20:00
Category: Mathematics
Tags: project euler, primes, combinatorial search, brute force

[Project Euler problem 60](https://projecteuler.net/problem=60) is a
nice mid-difficulty combinatorial search problem. It has enough
structure that pure brute force falls over, and enough structure that a
handful of small observations gives you a very tractable search.

Our working notes:
[Project Euler/60](https://charlesreid1.com/wiki/Project_Euler/60).

## The Problem

The primes 3, 7, 109, and 673 are "quite remarkable" - concatenating any
two of them in either order gives another prime. So `7109`, `1097`,
`3673`, `6733`, `109673`, `673109`, and so on, are all prime. That is 12
concatenations, all prime.

The sum of these four primes is 792, and the problem states this is the
smallest such sum for a set of four primes with this property.

Find the smallest sum for a set of **five** primes with the same
property.

## The Search Space

The naive approach: enumerate all 5-subsets of primes up to some bound
and check the property. The number of concatenations to check per
5-subset is

$$
\binom{5}{2} \times 2 = 20
$$

which is fine. The problem is the number of 5-subsets. If your prime
bound is 10,000, you have roughly 1,229 primes, and
`C(1229, 5) ≈ 2.3 × 10^13` subsets. Not fine.

So the whole game is: use structural facts about the problem to cut the
search space down.

## Pruning by Digit Constraints

The first observation is that concatenation preserves the last digit.
If `A` and `B` are primes, and you form `AB` (concatenation), then the
last digit of `AB` is the last digit of `B`. For `AB` to be prime, its
last digit must be 1, 3, 7, or 9 (or 2 or 5, but those only work if the
resulting number is exactly 2 or 5). So every prime in our set except
possibly one small one has to end in 1, 3, 7, or 9.

Similarly, since every prime except 2 has an odd last digit, and
prepending a number changes the first digit but not the last, both
primes in a pair have to end in 1, 3, 7, or 9.

Also: 2 and 5 can be immediately ruled out from consideration - any
concatenation involving 2 or 5 will produce a number ending in a digit
other than 1/3/7/9, and therefore composite.

This is a small pruning at the level of "which primes to include," but
it eliminates a lot of pointless primality tests later.

## Two-Pronged Search Strategy

Here is where things get interesting. The problem hands us the known
4-prime solution `{3, 7, 109, 673}`. So we have two very different
searches available to us:

**Extend-known search.** Take the known 4-prime set and look for a
single 5th prime `p` such that `p` concatenates to a prime with each of
`{3, 7, 109, 673}` in both orders. This is 8 primality checks per
candidate `p`, and we only need to iterate over primes.

**Fresh-set search.** Look for a completely new set of 5 primes,
possibly with a smaller total sum than the extension of the known
4-prime set.

The extend-known search is much cheaper (linear in the number of
candidate 5th primes, versus quintic in the fresh-set search). It also
gives you a solution quickly, which lets you set an upper bound on the
answer, which lets you prune the fresh-set search dramatically.

The correct order is:

1. Run extend-known first. Get some 5-prime solution and its sum, `S*`.
2. Run fresh-set search but throw out any partial set whose sum already
   exceeds `S*`.

By the time you get to step 2, you have a hard bound on how big any of
the primes can be, which shrinks the search space by orders of
magnitude.

## The Structure of a Fresh-Set Search

Even with the sum bound from step 1, a fresh search benefits from being
built up incrementally rather than as a nested 5-deep loop:

* Precompute a list of candidate primes up to some bound
* Build a **compatibility graph**: nodes are primes, an edge exists
  between `p` and `q` if both `p||q` and `q||p` are prime
* Find 5-cliques in this graph

Because a valid 5-set has to be a 5-clique in the compatibility graph
(every pair has to concatenate-to-prime with every other pair), you can
extend candidate sets incrementally:

* Start with a 2-clique (pair of primes that concatenate-to-prime)
* Extend to a 3-clique by finding a prime that concatenates-to-prime
  with both
* Extend to 4, then 5

At each stage, the set of viable extensions shrinks fast. Most 2-cliques
have no valid extension to a 3-clique. Most 3-cliques don't extend to a
4-clique. By the time you're looking for a 5-clique, the search is
narrow.

## Primality Testing

For a problem like this, the primality test gets called a lot. Two
things worth doing:

* Precompute a **prime sieve** for small numbers. The Sieve of
  Eratosthenes up to some reasonable bound gives you `O(1)` primality
  tests for anything in range.
* For the concatenated numbers (which can get large), use a
  probabilistic test like **Miller-Rabin**. Deterministic for numbers
  under `3.3 × 10^14` with the right witness set, so no false positives
  in the range this problem cares about.

## What We Learned

Two takeaways from this problem, generalizable to other combinatorial
search puzzles:

**Use the known solution as a bound.** If the problem hands you a
partial solution, get an answer from extending it first, then use that
answer's sum/cost as a pruning bound for the fuller search. This is
almost always faster than starting the fuller search cold.

**Build the compatibility graph explicitly.** For problems where "sets
of `k` things all pairwise satisfy some property" is the search shape,
converting it to "find a `k`-clique" in a precomputed compatibility
graph is usually the right structure. Clique-finding is NP-hard in
general, but for the small `k` values Project Euler cares about (5 in
this case), it is fast in practice.

## References

* Our wiki notes:
  [Project Euler/60](https://charlesreid1.com/wiki/Project_Euler/60)
* [PE 60 on projecteuler.net](https://projecteuler.net/problem=60)
* Our Java solution:
  <https://git.charlesreid1.com/cs/euler/src/branch/master/java/Problem060.java>
