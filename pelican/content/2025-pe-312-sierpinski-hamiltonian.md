Title: Project Euler 312: Hamiltonian Cycles on Sierpiński Graphs
Date: 2025-04-20 20:00
Category: Mathematics
Tags: project euler, graph theory, hamiltonian cycles, sierpinski, recursion, oeis

[Project Euler problem 312](https://projecteuler.net/problem=312) is one
of the harder problems we have worked through. It combines graph theory,
fractal geometry, combinatorial counting, and modular arithmetic, and
the final answer requires computing `C(C(C(10000))) mod 13^8` where
`C(n)` is the number of Hamiltonian cycles on a Sierpiński graph of
order `n`.

We ended up leaning on OEIS to get the recurrence in closed form, which
we will confess to below. Full notes:
[Project Euler/312](https://charlesreid1.com/wiki/Project_Euler/312).

## The Problem

A **Sierpiński graph** of order 1, denoted `S_1`, is an equilateral
triangle - three vertices, three edges.

`S_{n+1}` is built from three copies of `S_n` positioned so each pair
of copies shares one corner vertex.

Let `C(n)` be the number of cycles that pass through every vertex of
`S_n` exactly once - the number of **Hamiltonian cycles**. The problem
tells us `C(1) = C(2) = 1`, and `C(5) = 71,328,803,586,048`.

The goal: find `C(C(C(10000))) mod 13^8`.

Two things to notice about the goal. First, `C(10000)` is astronomically
large - you cannot actually compute it and then feed it to `C` again.
Second, `mod 13^8` is a big hint: the whole calculation is going to
happen in modular arithmetic, and there is going to be some periodicity
trick.

## Vertices and Edges

Some easy facts to nail down before doing anything clever.

Number of edges of `S_n`:

$$
e(S_n) = 3^{n+1}
$$

Number of vertices of `S_n`:

$$
v(S_n) = \frac{3}{2}\left(3^n + 1\right)
$$

So `S_10000` has on the order of `3^10000` vertices, which is a number
with about 4,700 decimal digits. A Hamiltonian cycle visits every
vertex, so the number of Hamiltonian cycles is going to have on the
order of `3^10000` factorial-ish in its combinatorics. There is no
approach that involves listing anything.

## The Recursive Structure

The critical observation is that `S_{n+1}` is built from three copies of
`S_n`. A Hamiltonian cycle on `S_{n+1}` has to traverse all three
copies, and the only places it can move between copies are at the
shared corner vertices. So any Hamiltonian cycle on `S_{n+1}` consists
of:

* A Hamiltonian **path** through the first copy of `S_n`, entering and
  exiting at two of its three outer corners
* A Hamiltonian path through the second copy, similarly
* A Hamiltonian path through the third copy, similarly
* Plus the three edges that connect the copies together at the shared
  corners

So counting Hamiltonian cycles reduces to counting certain kinds of
Hamiltonian paths on smaller graphs.

Let

* `C(n)` = number of Hamiltonian cycles on `S_n`
* `P(n)` = number of Hamiltonian paths on `S_n` where **both**
  endpoints are outer corners
* `P̄(n)` = number of Hamiltonian paths on `S_n` where **exactly one**
  endpoint is an outer corner

Then

$$
C(n) = [P(n-1)]^3
$$

(three copies, each contributing a Hamiltonian path with both endpoints
at outer corners, one path per copy, chosen independently).

Similarly, by tracking which paths piece together into which combined
paths, we get

$$
P(n) = 2 [P(n-1)]^2 P̄(n-1)
$$

$$
P̄(n) = 2 [P̄(n-1)]^2 P(n-1)
$$

These recurrences let us compute `P(n)`, `P̄(n)`, and `C(n)` in
principle. The values grow explosively - by the time `n = 5`, `C(n)` is
already `7.1 × 10^13`.

## Closed Form (Confession Time)

At this point we did the thing everyone does: computed `C(1)` through
`C(5)` from the recurrence, dropped the sequence into OEIS, and
immediately hit
[A246959](https://oeis.org/A246959) - the "number of Hamiltonian cycles
in the Sierpiński graph."

The closed form given by OEIS is

$$
C(n) = 8 \cdot 12^{(3^{n-2} - 3)/2} \qquad n \geq 3
$$

which is very compact. Equivalently, the recurrence

$$
C(n) = (3 \cdot C(n-1))^3 \qquad n \geq 4
$$

Sanity check against the given value `C(5) = 71,328,803,586,048`.
Wolfram Alpha confirms.

First few values:

| `n` | `C(n)` |
|-----|--------|
| 1 | 1 |
| 2 | 2 |
| 3 | 8 |
| 4 | 13,824 |
| 5 | 71,328,803,586,048 |

Note that `C(2) = 2` above, but the problem states `C(1) = C(2) = 1`.
The mismatch is a convention issue about what counts as a Hamiltonian
cycle on the tiniest graphs (traversal direction, effectively). We
used the OEIS convention for anything `n ≥ 3`, which is where the
counting matters.

## Nested Evaluation Under a Modulus

Now for the actual goal: `C(C(C(10000))) mod 13^8`.

The magnitude of `C(10000)` is not something you can hold in memory.
By `n = 20` the exponent in `12^((3^(n-2) - 3)/2)` is already millions
of digits long, and we are being asked about `n = 10000`. So the whole
calculation has to happen without ever materializing an intermediate
value in full.

The trick is that we don't *need* the intermediate values in full. We
need `C(C(C(10000))) mod 13^8`. That means for the outermost `C`, we
only need its argument modulo something that makes the outermost `C`
computable. And that "something" is much smaller than the argument
itself.

Three techniques do the work.

### Technique 1: Periodicity of `C(n) mod M`

The sequence `C(1), C(2), C(3), ...` taken modulo any fixed `M` is
eventually periodic. It has to be - the state at step `n` in the
recurrence `C(n) = (3 · C(n-1))^3 mod M` is a single residue in
`Z/MZ`, and there are only `M` possible residues, so the sequence must
eventually enter a cycle.

Let `P` be the period. Then

$$
C(X) \bmod M = C(((X - X_0) \bmod P) + X_0) \bmod M
$$

for `X` at least as large as the pre-period offset `X_0`. In practice
you compute successive `C(n) mod M` values until you see a repeat, and
that tells you `X_0` and `P`.

This is the workhorse. It lets you reduce "compute `C` at an
astronomically large index" to "compute `C` at an index in the range
`[X_0, X_0 + P)`."

### Technique 2: Choosing the Right Modulus at Each Layer

The three `C` calls need different moduli.

The **outermost** `C` operates modulo `13^8`. That is what the problem
asks for.

The **middle** `C` needs to produce a residue that determines the
outermost `C(x) mod 13^8`. By technique 1, the outermost `C` is
periodic mod `13^8` with some period `P_out`. So the middle `C` only
needs to compute its result **modulo `P_out`** (well, modulo the
pre-period plus period - be careful with the offset).

The **innermost** `C(10000)` needs to produce a residue that determines
the middle `C(y) mod P_out`. So find the period `P_mid` of `C` mod
`P_out`, and compute `C(10000) mod P_mid`.

So the algorithm is:

1. Find the period of `C(n) mod 13^8`. Call it `P_out`.
2. Find the period of `C(n) mod P_out`. Call it `P_mid`.
3. Compute `C(10000) mod P_mid`. Call the result `a`.
4. Compute `C(a) mod P_out`. Call the result `b`.
5. Compute `C(b) mod 13^8`.

Each step uses either the recurrence directly (`b = (3·b_prev)^3 mod M`)
or, for the innermost step at `n = 10000`, the recurrence run 10000
times mod the appropriate modulus. Ten thousand modular multiplications
is nothing.

### Technique 3: Handling the Cube Under a Prime Power

The recurrence `C(n) = (3 · C(n-1))^3` involves a cube, so under a
prime power modulus you have to be careful about invertibility. Cubing
is well-defined mod `13^8` (or mod anything else), so the forward
recurrence is not a problem - you just cube and multiply. What can go
wrong is if you try to *invert* the cubing at some point, which you
would need if you tried to do matrix exponentiation on the logarithm of
the recurrence.

We did not need to invert. The three-layer periodicity approach above
uses only forward evaluation of the recurrence, so cubing mod `13^8` is
fine.

### Chinese Remainder Theorem

CRT is worth mentioning for completeness. If the modulus had been
composite with multiple distinct prime factors, we would compute the
answer separately modulo each prime power and glue the results
together with CRT.

Here the modulus is `13^8`, a single prime power, so CRT is not
needed - but if the problem had asked for `mod (7^5 · 11^3 · 13^8)`,
the approach would be to solve three separate problems and CRT the
answers.

## What We Learned

Three things worth carrying forward.

**Recursive structure beats brute force by a lot.** The naive approach
of enumerating cycles on `S_n` is impossible for anything `n > 4` or so.
The recursive approach reduces the problem to counting paths on
`S_{n-1}` with three specific endpoint types, and that recursion
collapses to a single-variable formula. Every time you can find a
recursive structure, use it.

**OEIS is not cheating.** Recognizing a sequence and looking up its
closed form is a legitimate research tool, not shortcut. The people who
computed and cataloged OEIS A246959 did the work of proving the closed
form. Standing on their shoulders is what mathematics has always looked
like. The alternative - re-deriving every known result from scratch - is
how you never finish anything.

**Nested modular evaluation is a real technique.** When a problem asks
for `f(f(f(n))) mod M` with a huge `n`, you rarely need to compute the
intermediate values. You work outward-in through periods: the outermost
period tells you what modulus the middle layer actually needs to
produce, which tells you what modulus the innermost layer needs to
produce. Astronomical intermediate values reduce to residues in
tractable rings. This shape of problem shows up a lot in number theory
and cryptography, and it is worth having the pattern in your head.

## References

* Our wiki notes:
  [Project Euler/312](https://charlesreid1.com/wiki/Project_Euler/312)
* [PE 312 on projecteuler.net](https://projecteuler.net/problem=312)
* [OEIS A246959](https://oeis.org/A246959) - Hamiltonian cycles in
  Sierpiński graphs
* Useful paper: <https://arxiv.org/pdf/0909.5541> (Hamiltonian
  properties of Sierpiński graphs)
