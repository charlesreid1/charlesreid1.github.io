Title: Generating Functions Part 3: Ternary Strings and Exponential Generating Functions
Date: 2022-10-25 12:00
Category: Mathematics
Tags: mathematics, generating functions, egf, combinatorics, strings
Status: draft

This is part 3 of our series on generating functions.
[Part 1](generating-functions-part-1-solving-the-quicksort-recurrence.html)
handled the quicksort recurrence.
[Part 2](generating-functions-part-2-marbles-in-a-can.html) used ordinary
generating functions to count marbles in a can.

In this post we introduce **exponential generating functions**, which are
what you reach for when the *order* of the objects you are counting matters.
As with the earlier posts, our working notes live on the
[Generating Functions](https://charlesreid1.com/wiki/Generating_Functions)
page of our wiki.

## When Order Matters

The marbles-in-a-can problem from part 2 was order-independent. A can
containing three reds, two blues, and one yellow is the same can no matter
what order you put the marbles in. That is why ordinary generating functions
worked - the coefficient of $z^n$ just counted unordered combinations.

Now suppose we are counting ternary strings: sequences of digits from
$\{0, 1, 2\}$ of length $n$. Here order matters. $012$ and $210$ are
different strings, even though they use the same digits.

For problems like this we use exponential generating functions, defined
using $\tfrac{z^n}{n!}$ instead of $z^n$. The base building block is
$e^z$ instead of $\tfrac{1}{1-z}$:

$$
e^z = \sum_{n \geq 0} \dfrac{z^n}{n!}
$$

The $n!$ in the denominator is where the "order matters" bookkeeping
happens automatically.

## The Problem

Count the ternary strings of length $n$ that contain an **even** number
of 0s.

## Setting Up

As with the marbles problem, we write one generating function per digit
and multiply.

**Digits 1 and 2** are unconstrained - any number can appear:

$$
E_1(z) = E_2(z) = e^z = \sum_{n \geq 0} \dfrac{z^n}{n!}
$$

**Digit 0** is where the constraint lives. We need an even number of them,
which means we want the series

$$
1 + \dfrac{z^2}{2!} + \dfrac{z^4}{4!} + \dfrac{z^6}{6!} + \dots
$$

Here is a nice trick. Write out $e^z$ and $e^{-z}$:

$$
e^{z}  = 1 + \dfrac{z}{1!} + \dfrac{z^2}{2!} + \dfrac{z^3}{3!} + \dfrac{z^4}{4!} + \dots
$$

$$
e^{-z} = 1 - \dfrac{z}{1!} + \dfrac{z^2}{2!} - \dfrac{z^3}{3!} + \dfrac{z^4}{4!} - \dots
$$

Adding them, the odd terms cancel and the even terms double:

$$
\dfrac{e^{z} + e^{-z}}{2} = 1 + \dfrac{z^2}{2!} + \dfrac{z^4}{4!} + \dots
$$

That is exactly the generating function we need for the 0s:

$$
E_0(z) = \dfrac{e^{z} + e^{-z}}{2}
$$

The $(e^z + e^{-z})/2$ trick is one of the most useful little identities
in this whole business. If you ever need "only even terms" or "only odd
terms", this is how you get them.

## Multiplying

The overall generating function is

$$
E(z) = E_0(z) \cdot E_1(z) \cdot E_2(z) = e^{z} \cdot e^{z} \cdot \dfrac{e^{z} + e^{-z}}{2} = \dfrac{e^{3z} + e^{z}}{2}
$$

which is beautifully compact.

## Extracting the Coefficient

Convert $e^{3z}$ and $e^{z}$ back to series:

$$
\dfrac{e^{3z} + e^{z}}{2} = \dfrac{1}{2} \sum_{n \geq 0} \dfrac{(3z)^n + z^n}{n!} = \sum_{n \geq 0} \dfrac{3^n + 1}{2} \cdot \dfrac{z^n}{n!}
$$

The coefficient of $\tfrac{z^n}{n!}$ is the number of ternary strings of
length $n$ with an even number of 0s:

$$
\dfrac{3^n + 1}{2}
$$

## Sanity Check

Length 1: $\tfrac{3 + 1}{2} = 2$. The strings are "1" and "2" (both have
zero 0s, and zero is even). ✓

Length 2: $\tfrac{9 + 1}{2} = 5$. There are 9 total ternary strings of
length 2. The ones with an even number of 0s are: 11, 12, 21, 22 (zero 0s),
and 00 (two 0s). That is 5. ✓

Length 3: $\tfrac{27 + 1}{2} = 14$. Out of 27 total, we want strings with
0 or 2 zeros. Strings with zero 0s use only {1, 2}, giving $2^3 = 8$.
Strings with two 0s have the two 0s in one of $\binom{3}{2} = 3$ positions
and a 1 or 2 in the remaining position, giving $3 \cdot 2 = 6$. Total is
$8 + 6 = 14$. ✓

## The Payoff

Ordinary generating functions counted the marbles problem, where order did
not matter. Exponential generating functions handled the ternary-strings
problem, where order did. In both cases the recipe is the same:

1. Write down a generating function per "slot" (per color, per digit).
2. Encode the constraints in the shape of the individual series.
3. Multiply.
4. Read off the coefficient.

The only real difference is whether you build out of $z^n$ or $\tfrac{z^n}{n!}$,
and which little identities you have in your toolkit for shaping series to
match constraints. The $(e^z + e^{-z})/2$ trick is one of the good ones.

## References

* Our wiki notes:
  [Generating Functions](https://charlesreid1.com/wiki/Generating_Functions)
* Trotter, *Applied Combinatorics*, Chapter 8 (exponential generating
  functions section)
