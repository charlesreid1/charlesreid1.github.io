Title: Generating Functions Part 1: Solving the Quicksort Recurrence
Date: 2022-10-23 12:00
Category: Mathematics
Tags: mathematics, generating functions, algorithms, quicksort, recurrence, sedgewick
Status: draft

This post is part 1 of a series on generating functions, based on notes
we have been working through from Sedgewick and Flajolet's *Analysis of
Algorithms* and Trotter's *Applied Combinatorics*. The full set of notes
lives on our wiki:
[Generating Functions](https://charlesreid1.com/wiki/Generating_Functions).

Generating functions are one of those techniques that look completely
mysterious the first time you see them, and then look like the obvious
thing to do the tenth time you see them. They turn recurrences into
functions, functions into series, and series back into closed forms for
the coefficients you actually wanted. This post walks through one of the
nicest applications: solving the recurrence relation for quicksort.

## The Recurrence

The average number of comparisons quicksort makes on an array of size $n$
satisfies the recurrence

$$
C_n = n + 1 + \dfrac{2}{n} \sum_{1 \leq k \leq n} C_{k-1}
$$

The $n+1$ term is the cost of the partition step. The sum averages the cost
of recursing on the two subarrays over all possible choices of pivot.

Staring at that sum inside the recurrence is not a great starting point.
Everything on the right depends on every $C_k$ that came before. Generating
functions are how we get out.

## Setting Up the Generating Function

The plan is to introduce a generating function

$$
C(z) = \sum_{n \geq 0} C_n z^n
$$

and then translate each piece of the recurrence into an operation on $C(z)$.

Multiplying the recurrence by $n$ to clear the $\tfrac{2}{n}$, and then by
$z^n$, and summing over $n$, we end up with

$$
\sum_{n \geq 1} n C_n z^n = \sum_{n \geq 1} n(n+1) z^n + 2 \sum_{n \geq 1} \sum_{1 \leq k \leq n} C_{k-1} z^n
$$

Each of these three terms turns into something in $C(z)$:

* The left side is $z C'(z)$, since taking a derivative and multiplying by $z$
  pulls out an $n$ from each term of the series
* The first term on the right involves the second derivative of
  $\tfrac{1}{1-z}$, and simplifies to $\tfrac{2}{(1-z)^3}$
* The double sum is a partial-sum operation, which corresponds to multiplying
  by $\tfrac{1}{1-z}$

Putting it all together, we get

$$
C'(z) = \dfrac{2}{(1-z)^3} + \dfrac{2 C(z)}{1 - z}
$$

The recurrence has become a first-order linear differential equation.

## Solving the ODE

To solve

$$
C'(z) - \dfrac{2 C(z)}{1 - z} = \dfrac{2}{(1-z)^3}
$$

we look for an integrating factor $\rho(z)$ such that
$\rho'(z) = -\dfrac{2 \rho(z)}{1-z}$. That works out to $\rho(z) = (1-z)^2$.

Multiplying through:

$$
\left( (1-z)^2 C(z) \right)' = \dfrac{2}{1-z}
$$

Integrating both sides:

$$
(1-z)^2 C(z) = 2 \ln \left( \dfrac{1}{1-z} \right)
$$

And so

$$
C(z) = \dfrac{2}{(1-z)^2} \ln \left( \dfrac{1}{1-z} \right)
$$

That is the generating function for the average number of comparisons in
quicksort. Not obvious.

## Reading Off the Coefficient

Now we extract $C_n = [z^n] C(z)$. The expression $\tfrac{1}{(1-z)^2}$ has
the well-known expansion $\sum (n+1) z^n$, and $\ln \left( \tfrac{1}{1-z} \right)$
has the expansion $\sum \tfrac{z^k}{k}$, which is the generating function
for the sequence $H_k = 1 + \tfrac{1}{2} + \dots + \tfrac{1}{k}$ (the
harmonic numbers, once you divide by $\tfrac{1}{1-z}$ to accumulate).

Working through the convolution, we land at

$$
C_n = 2(n+1)(H_{n+1} - 1)
$$

That is the closed form. Since $H_n \approx \ln n + \gamma$ for large $n$,
this gives $C_n \sim 2 n \ln n$, which recovers the familiar
$O(n \log n)$ average case for quicksort - with an actual constant in front
of it.

## Why This Is Worth Learning

The reason this technique is so satisfying is that we started with a
recurrence that looked completely intractable - $C_n$ depends on the entire
prefix $C_0, C_1, \dots, C_{n-1}$ - and ended with a clean closed form.

The mechanical steps are:

1. Turn the recurrence into a functional equation in $C(z)$ by multiplying
   by $z^n$ and summing.
2. Solve the functional equation. Sometimes it is algebraic, sometimes it
   is a differential equation (as here).
3. Extract the $n$-th coefficient of the solution.

In upcoming posts in this series, we will look at simpler examples that
show how the coefficient extraction step works, including a nice puzzle
about distributing colored marbles into cans with weird constraints.

## References

* Our full notes:
  [Generating Functions](https://charlesreid1.com/wiki/Generating_Functions)
  on the wiki (Sedgewick/Flajolet and Trotter, side by side)
* Knuth-flavored coverage:
  [AOCP/Generating Functions](https://charlesreid1.com/wiki/AOCP/Generating_Functions)
