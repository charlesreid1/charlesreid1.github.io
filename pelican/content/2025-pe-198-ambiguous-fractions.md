Title: Project Euler 198 and Continued Fractions: When Is a Rational Ambiguous?
Date: 2025-04-15 22:00
Category: Mathematics
Tags: project euler, continued fractions, number theory, rational approximation

[Project Euler problem 198](https://projecteuler.net/problem=198) is a
number theory problem that turns out to be almost entirely about
continued fractions. The problem hides this - the statement talks about
"ambiguous" real numbers - but the ambiguity has a clean characterization
in terms of continued fraction expansions, and once you see it, the
problem gets a lot smaller.

Wiki notes:
[Project Euler/198](https://charlesreid1.com/wiki/Project_Euler/198).

## The Problem

Define a **best approximation** to a real number `x` with denominator
bound `d` as a rational `r/s` in reduced form with `s ≤ d`, such that
any other rational `p/q` closer to `x` than `r/s` has `q > d`. In other
words: it is the rational number with the smallest denominator that
gets as close to `x` as anything with a small enough denominator can.

Usually the best approximation is unique for each denominator bound.
But sometimes there are two equally-good best approximations. The
problem gives the example of `x = 9/40`, which has both `1/4` and `1/5`
as best approximations for the denominator bound `d = 6`. Both are
tied for closest to `9/40` among rationals with denominator at most 6.

Call a real number `x` **ambiguous** if there is at least one denominator
bound for which it has two best approximations. Ambiguous numbers are
necessarily rational.

The question: how many ambiguous `x = p/q` with `0 < x < 1/100` and
`q ≤ 10^8` are there?

## Why Continued Fractions

Any real number `x` has a **continued fraction expansion**

$$
x = a_0 + \cfrac{1}{a_1 + \cfrac{1}{a_2 + \cfrac{1}{a_3 + \ddots}}}
$$

which we write compactly as `[a_0; a_1, a_2, a_3, ...]`. For rational
numbers, the expansion terminates. For irrationals, it does not.

The **convergents** of a continued fraction are the rationals you get
by truncating the expansion at each step. The convergents of
`[a_0; a_1, a_2, ..., a_n]` are

$$
[a_0], [a_0; a_1], [a_0; a_1, a_2], \ldots
$$

There is a beautiful classical theorem that says: **the convergents of
the continued fraction expansion of `x` are exactly the best
approximations to `x`**. Every convergent is a best approximation for
some denominator bound, and every best approximation is a convergent
or a certain kind of intermediate fraction.

For `x = 9/40`:

* CF expansion: `[0; 4, 2, 4]`
* First convergent: `[0; 4] = 1/4`
* Second convergent: `[0; 4, 2] = 1 / (4 + 1/2) = 2/9`
* Third (final) convergent: `[0; 4, 2, 4] = 9/40`

So `1/4` is one best approximation for `9/40` at some bound. Where does
the *other* one, `1/5`, come from?

## Where Ambiguity Comes From

The answer is that not all best approximations are convergents. There
are also **intermediate fractions**, which sit between successive
convergents. Specifically, when a partial quotient `a_k` is larger than
1, you can form intermediate fractions

$$
\frac{p_{k-1} + j \cdot p_k}{q_{k-1} + j \cdot q_k}
$$

for `j = 1, 2, ..., a_{k+1} - 1`, where `p_k / q_k` is the `k`-th
convergent. These intermediate fractions are best approximations for
certain denominator bounds.

The situation where a real number has **two** best approximations for
some denominator bound is exactly when a convergent and an intermediate
fraction happen to sit equidistant from `x`. This can only happen when
the continued fraction expansion has some partial quotient bigger than 1
sitting in the right place.

The clean characterization we ended up with is this:

**A rational `p/q` is *non-ambiguous* if and only if its continued
fraction expansion has the form**

$$
[0; a_1] \quad \text{or} \quad [0; a_1, 1, 1, \ldots, 1]
$$

Everything else is ambiguous.

This is the crux of the problem. Instead of counting ambiguous fractions
directly, count the total number of relevant fractions and subtract the
non-ambiguous ones - or, better, characterize the ambiguous ones
directly by generating their continued fraction expansions.

## Constraints From the Problem

The problem restricts to `0 < p/q < 1/100` and `q ≤ 10^8`.

Since `p ≥ 1` and `p/q < 1/100`, we have `q > 100 p ≥ 100`. So `q`
ranges from 101 up to `10^8`.

For a given `q`, valid `p` values satisfy:

* `p ≥ 1`
* `p ≤ q/100`
* `gcd(p, q) = 1` (reduced form)

That gives us roughly `q/100` candidate numerators per denominator, but
we also have to intersect with "coprime to `q`" and "continued fraction
has the right shape to be ambiguous."

## The Search

The high-level approach:

1. Iterate over denominators `q` from 101 to `10^8`
2. For each `q`, enumerate valid `p` values (coprime to `q`, in range)
3. Compute the continued fraction expansion of `p/q`
4. Check whether the expansion has the "ambiguous" shape
5. Count

The bottleneck is that step 1 is `10^8` iterations, and even a very
fast inner loop times out. So the real approach is to invert the
problem: instead of iterating over fractions and checking whether
their CF is ambiguous, iterate over the *shapes* of ambiguous CF
expansions and count the fractions those shapes produce that fall in
the range.

This is a nice example of a general technique: when you have a
characterization of the objects you want to count in terms of some
structural property, generating objects by structure is usually faster
than filtering.

## The Bigger Point

Problems that look purely computational often turn out to have a clean
structural characterization hiding underneath. The PE 198 statement
never mentions continued fractions - it's about "best approximations"
and "ambiguous real numbers." But the moment you dig into what best
approximation actually means for rationals, continued fractions appear
naturally, and the entire problem reduces to counting fractions whose
CF has a certain shape.

This kind of translation - from a definition in one language to a
characterization in another - is where number theory earns its
reputation for being satisfying. You start with "count the ambiguous
fractions" and you end with "count the fractions whose CF is not of
the form `[0; a₁, 1, 1, ..., 1]`," and the second version is much
easier to work with.

## References

* Our wiki notes:
  [Project Euler/198](https://charlesreid1.com/wiki/Project_Euler/198)
* [PE 198 on projecteuler.net](https://projecteuler.net/problem=198)
* Classical reference: Hardy & Wright, *An Introduction to the Theory
  of Numbers*, chapters on continued fractions
