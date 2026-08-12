Title: Generating Functions Part 2: Marbles in a Can
Date: 2022-10-24 12:00
Category: Mathematics
Tags: mathematics, generating functions, combinatorics, ogf, trotter
Status: draft

This is part 2 of our series on generating functions. In
[part 1](generating-functions-part-1-solving-the-quicksort-recurrence.html)
we used generating functions to solve the quicksort recurrence, which is a
serious industrial-strength application. This time we will use them for
something a lot more whimsical: counting how many different cans of colored
marbles you can put together under a bunch of arbitrary rules.

The example is from Trotter's *Applied Combinatorics*. Our working notes
for this one, along with a few related exercises, live on the
[Generating Functions](https://charlesreid1.com/wiki/Generating_Functions)
page of our wiki.

## The Problem

We are packing cans of marbles. Each can holds 20 marbles, in some
combination of red, blue, yellow, and green. The rules are:

* Each can must have **at least one** red marble.
* Each can can have **no more than three** blue marbles.
* Yellow marbles can appear in any quantity.
* Green marbles can only appear in **multiples of 4**.

How many different cans of 20 marbles are there?

## The Generating Function Approach

The trick with problems like this is to write down one generating function
per color, where the coefficient of $z^k$ represents "the number of ways to
put $k$ marbles of this color in the can." Then multiply them all together.
The coefficient of $z^{20}$ in the product is the answer.

Each rule turns into a constraint on the shape of that color's series.

**Red** must have at least one, so the $z^0$ term is missing:

$$
G_r(z) = z + z^2 + z^3 + \dots = \dfrac{z}{1-z}
$$

**Blue** can have zero to three, and no more, so it is a polynomial:

$$
G_b(z) = 1 + z + z^2 + z^3
$$

**Yellow** is unconstrained:

$$
G_y(z) = 1 + z + z^2 + z^3 + \dots = \dfrac{1}{1-z}
$$

**Green** appears only in multiples of 4. So the only nonzero coefficients
are on $z^0, z^4, z^8, \dots$:

$$
G_g(z) = 1 + z^4 + z^8 + z^{12} + \dots = \dfrac{1}{1 - z^4}
$$

(The substitution $u = z^4$ turns this into the familiar $\tfrac{1}{1-u}$,
which is where the closed form comes from.)

## Multiplying It All Together

The total generating function is

$$
G(z) = G_r(z) \cdot G_b(z) \cdot G_y(z) \cdot G_g(z)
     = \dfrac{z}{1-z} \cdot (1 + z + z^2 + z^3) \cdot \dfrac{1}{1-z} \cdot \dfrac{1}{1-z^4}
$$

There is a nice simplification hiding in there. Notice that
$1 + z + z^2 + z^3 = \tfrac{1 - z^4}{1 - z}$, so the $1 - z^4$ cancels with
the denominator of $G_g$, and the $1 - z$ in the numerator eats one power
of the $\tfrac{1}{1-z}$ factors. What is left is

$$
G(z) = \dfrac{z}{(1-z)^3}
$$

Which is much easier to work with.

## Reading Off the Answer

We want the coefficient of $z^{20}$ in $\dfrac{z}{(1-z)^3}$.

The expansion of $\dfrac{1}{(1-z)^3}$ is

$$
\dfrac{1}{(1-z)^3} = \sum_{n \geq 0} \binom{n+2}{2} z^n
$$

which is the triangle-number sequence $1, 3, 6, 10, 15, 21, \dots$.

Multiplying by $z$ shifts the coefficients up by one power, so the
coefficient of $z^n$ in $G(z)$ is $\binom{n+1}{2}$.

For a can of 20 marbles:

$$
\binom{21}{2} = 210
$$

So there are exactly 210 different cans of 20 marbles that satisfy all
the rules.

## Sanity Check on Small Cases

We can verify the closed form by walking through small $n$.

**$n = 1$ (one marble):** Only one configuration works - the single red
marble. Coefficient is $\binom{2}{2} = 1$. ✓

**$n = 2$ (two marbles):** One slot is red. The other slot can be red, blue,
or yellow (green is out because it only appears in multiples of 4). That is
3 configurations: RR, RB, RY. Coefficient is $\binom{3}{2} = 3$. ✓

**$n = 3$ (three marbles):** Same idea, one is red, the other two are drawn
from {R, B, Y}. Enumerating: RRR, RRB, RRY, RBB, RBY, RYY. That is 6.
Coefficient is $\binom{4}{2} = 6$. ✓

The pattern of $3, 6, 10, 15, \dots$ is a run of triangle numbers, which
is exactly what $\binom{n+1}{2}$ produces.

## The Point

You could solve this problem by writing a script that enumerates every
combination of $(r, b, y, g)$ with $r+b+y+g = 20$ and the constraints
respected, and it would work fine. The generating function approach does
something different: it gives you a *closed form* for the answer as a
function of $n$. Change the can size to 50, and you get $\binom{51}{2} = 1275$
without running anything.

Also, and this matters more than it sounds: turning "no more than three"
into a polynomial and "multiples of four" into a series in $z^4$ takes
the constraints out of your enumeration logic and puts them into algebra.
Algebra is easier to check than nested loops.

Next in the series: what happens when order matters, and we need to switch
from ordinary generating functions to exponential generating functions.

## References

* Our wiki notes:
  [Generating Functions](https://charlesreid1.com/wiki/Generating_Functions)
* Trotter, *Applied Combinatorics*, Chapter 8
