Title: Generating Functions Part 2: Marbles in a Can
Date: 2022-10-24 12:00
Category: Mathematics
Tags: mathematics, generating functions, combinatorics, ogf, trotter

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

## The General Problem: How Do You Read Coefficients Off *Anything*?

The step above worked because we recognized $\tfrac{1}{(1-z)^3}$ on
sight. That is not the general case. In real problems you multiply four
or five generating functions together, simplify, and end up staring at
some expression like

$$
\dfrac{1 + z^2}{(1 - z)^2 (1 - 2z)}
$$

and the question is: **now what?** How do you turn that back into a
sequence, a closed form for $a_n$, or at least something you can look
up? This is the reverse direction of the whole generating-function
program, and it deserves an explicit toolkit rather than a "you'll
recognize it" hand-wave.

Here is the toolkit we actually reach for, in order of first resort.
The first three steps are practical tools that will hand you an answer
in seconds. The rest are the by-hand techniques that let you *understand*
or *manipulate* what the tools give back.

### 1. Just ask Wolfram Alpha

This is the first tool to reach for. Full stop. Ahead of the algebra,
ahead of the cheat sheet, ahead of everything. Type your generating
function into [Wolfram Alpha](https://www.wolframalpha.com) with a
natural-language series request and it will hand you back the expansion:

```
series (1-z^4)/((2-4z^2)*(1-z)) to 50 terms
```

or

```
series expansion of z/(1-z)^3 at z=0 to order 22
```

You get the first N coefficients, immediately, with no setup, no
notebook, no environment. Wolfram Alpha will also do partial fractions
(`partial fractions of ...`), Taylor expansions, and single-coefficient
extraction (`coefficient of z^20 in ...`) as one-line queries. If you
want a closed form, `sequence 1, 3, 6, 10, 15, 21` will often produce
one, plus the generating function and recurrence.

The reason this matters more than it might sound: an enormous class of
counting problems has generating functions that factor into a product
of $\tfrac{1}{1 - z^{c_i}}$ terms — one factor per denomination, coin
type, box size, whatever the allowed "units" are in the problem.
Polya's classic *change for a dollar* problem is exactly this shape:

$$
G(z) = \dfrac{1}{(1 - z)(1 - z^5)(1 - z^{10})(1 - z^{25})(1 - z^{50})(1 - z^{100})}
$$

The number of ways to make change for $n$ cents is $[z^n] G(z)$. Doing
partial fractions on that by hand is a slog and the closed form is
ugly. Asking Wolfram Alpha
`series expansion of 1/((1-z)(1-z^5)(1-z^10)(1-z^25)(1-z^50)(1-z^100)) to 101 terms`
gives you the whole table in one shot, including the famous answer of
293 for $n = 100$.

For anything in this family — restricted partitions, compositions with
allowed part sizes, Frobenius / coin problems, our marble problem —
this is a one-shot solution. Do not talk yourself out of using it. The
by-hand techniques below are for when you want a closed form or an
identity you can prove; if all you want is the *number*, Wolfram Alpha
is done before you have finished writing the query.

### 2. Compute a few terms and look them up in OEIS

Once you have coefficients from step 1 (or by hand), if the sequence
does not have an obvious closed form, type the integers into
the [Online Encyclopedia of Integer Sequences](https://oeis.org).

OEIS will tell you the sequence's name, closed-form expression if one
exists, recurrence, generating function, and every combinatorial
interpretation anyone has ever noticed. If your sequence starts
$1, 1, 2, 5, 14, 42, \dots$, OEIS hands you back "Catalan numbers" and
a page of context. If it starts $1, 3, 11, 50, 274, \dots$ you learn it
is A000670, the Fubini numbers, counting ordered set partitions — a
connection you would probably not have made from the generating
function alone.

The Wolfram Alpha → OEIS pipeline is the single most powerful move in
this whole toolkit. Half the sequences that come up in combinatorics
have names, and knowing the name gives you access to identities and
asymptotics that would take you weeks to rederive.

### 3. Drop into a computer algebra system

When you want to keep the result in a script, do further manipulation,
or extract many coefficients programmatically, use `sympy` or
Mathematica. In `sympy`:

```python
from sympy import symbols, series, apart
z = symbols('z')
G = z / (1 - z)**3
series(G, z, 0, 22)          # expand as a power series
apart(G, z)                  # partial fraction decomposition
G.series(z, 0, 22).coeff(z, 20)   # coefficient of z^20
```

Wolfram Alpha handles one-off queries in the browser; `sympy` is what
you reach for when the generating function is being constructed
programmatically or the coefficients feed into further computation.

---

The three tools above will get you a *number* — often the number you
wanted. The next four techniques are for the case where you want more
than a number: a closed form, a proof, or an understanding of *why* the
sequence looks the way it does.

### 4. Match against a table of standard series

The single most productive by-hand move is to keep a cheat sheet of
standard generating functions and their coefficients. If you can
massage your expression into a sum of these, you have a closed form.

The core list:

$$
\dfrac{1}{1 - z} = \sum_{n \geq 0} z^n
\qquad
\dfrac{1}{(1 - z)^2} = \sum_{n \geq 0} (n+1)\, z^n
$$

$$
\dfrac{1}{(1 - z)^k} = \sum_{n \geq 0} \binom{n + k - 1}{k - 1} z^n
\qquad
\dfrac{1}{1 - az} = \sum_{n \geq 0} a^n z^n
$$

$$
(1 + z)^k = \sum_{n \geq 0} \binom{k}{n} z^n
\qquad
e^z = \sum_{n \geq 0} \dfrac{z^n}{n!}
$$

The third one, the **negative binomial series**, is the workhorse.
Almost every rational generating function with only $(1-z)^k$-style
denominators reduces to a sum of these, and their coefficients are
binomial coefficients in $n$.

### 5. Partial fractions to break the expression apart

If your expression is a rational function $\tfrac{P(z)}{Q(z)}$ where
$Q(z)$ factors into simple pieces like $(1 - a_i z)^{k_i}$, expand it by
partial fractions:

$$
\dfrac{P(z)}{(1 - a_1 z)(1 - a_2 z)^2 \cdots}
= \dfrac{A}{1 - a_1 z}
+ \dfrac{B}{1 - a_2 z}
+ \dfrac{C}{(1 - a_2 z)^2}
+ \cdots
$$

Each piece is a standard series from step 4. Reading coefficients off
the sum is then just adding standard-series coefficients term by term.
This is how you get closed forms with mixed geometric and polynomial
behavior, like $a_n = A \cdot a_1^n + (B + C n) \cdot a_2^n$.

For the Fibonacci generating function $\tfrac{z}{1 - z - z^2}$, this
exact procedure produces Binet's formula. It is a very general hammer.

### 6. Use the calculus of generating functions

A handful of operations on a generating function correspond to clean
operations on its coefficient sequence. Recognizing them lets you build
up unfamiliar expressions from familiar ones.

* **Multiplying by $z$** shifts coefficients: if
  $A(z) = \sum a_n z^n$ then $z \cdot A(z) = \sum a_{n-1} z^n$. This is
  what we used above to get from $\binom{n+2}{2}$ to $\binom{n+1}{2}$.
* **Differentiating** produces $A'(z) = \sum n \, a_n \, z^{n-1}$, and
  multiplying that by $z$ gives $\sum n \, a_n \, z^n$. So the "times
  $n$" operator on a sequence is $z \tfrac{d}{dz}$ on the generating
  function. This is how you get things like $\sum n z^n$ from
  $\sum z^n$.
* **Integrating** goes the other way: dividing coefficients by $n$.
* **Multiplying two generating functions** convolves their coefficient
  sequences: $\sum_{k=0}^{n} a_k \, b_{n-k}$. Sometimes you will
  recognize a convolution in a combinatorial identity you are trying
  to prove.
* **Substituting** $z \to z^m$ spreads coefficients out, putting zeros
  between them. Substituting $z \to a z$ multiplies coefficient $n$
  by $a^n$.

If you see a generating function that looks like a standard one with an
extra factor of $z$ or an extra power of $n$ in front, these operations
are usually how it got there — and they tell you how to undo it.

### 7. Extract a single coefficient directly

Sometimes you do not need the whole sequence, just one term. The
formal notation is

$$
[z^n] \, A(z) = a_n
$$

and there are algebraic rules for pushing $[z^n]$ around:

$$
[z^n] \, z \cdot A(z) = [z^{n-1}] \, A(z)
\qquad
[z^n] \, A(z) B(z) = \sum_{k=0}^{n} [z^k] A(z) \cdot [z^{n-k}] B(z)
$$

For rational $A(z)$ with small denominators, you can also just do long
division of the series until you reach the $z^n$ term. Tedious but
mechanical, and useful for a sanity check against Wolfram Alpha.

### 8. When nothing closes: asymptotics

Some generating functions simply do not have a nice closed-form
coefficient. That is fine. In those cases you switch questions: instead
of "what is $a_n$ exactly?" you ask "how does $a_n$ grow with $n$?" The
answer usually falls out of the location and type of the singularities
of $A(z)$ nearest the origin — this is *singularity analysis*, and
Flajolet and Sedgewick's [*Analytic Combinatorics*](https://charlesreid1.com/wiki/Analytic_Combinatorics) is the reference. It
is out of scope for this series, but worth knowing exists: even when
you cannot read off an answer, you can often read off the growth rate.

### Applied to our expression

For $\tfrac{z}{(1-z)^3}$ we used step 4 (recognize a standard series)
and step 6 (multiply by $z$ shifts the index). Two lines of algebra
and a closed form falls out. But we could just as easily have typed
`series z/(1-z)^3 to 22 terms` into Wolfram Alpha, read off 210 as the
coefficient of $z^{20}$, dropped $1, 3, 6, 10, 15, 21$ into OEIS, and
learned that these are triangle numbers with generating function
$\tfrac{z}{(1-z)^3}$ and closed form $\binom{n+1}{2}$ — arriving at the
same place from the other direction.

Both directions are legitimate. Which one you use depends on whether
you want the answer or the understanding. Usually you want both, which
means using the tools to get the answer fast and then doing the algebra
to see why.

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
* Flajolet and Sedgewick,
  [*Analytic Combinatorics*](https://charlesreid1.com/wiki/Analytic_Combinatorics)
  — for singularity analysis and asymptotics
