Title: A Hard(y) Math Problem
Date: 2017-11-03 19:00
Category: Mathematics
Tags: mathematics, calculus, integrals, hardy, cambridge, tripos

## An Integral from Hardy

Here's an integral from G. H. Hardy:

$$
\int \dfrac{dx}{\sqrt{x+a} + \sqrt{x+b}}
$$

It doesn't fit any of the standard undergraduate forms. There's no obvious
$u$-substitution, integration by parts doesn't help, and a trigonometric
substitution turns it into a mess.

## The Setup

The trouble is the sum of two square roots in the denominator. With just
one square root the integral is a power-rule exercise:

$$
\int \dfrac{dx}{\sqrt{x+a}} = 2\sqrt{x+a} + C
$$

But the sum resists the usual substitutions. Its derivative involves both
roots in a form that doesn't cancel cleanly against anything you'd put in
the numerator.

## Multiply by the Conjugate

Multiply numerator and denominator by the conjugate $\sqrt{x+a} - \sqrt{x+b}$:

$$
\dfrac{1}{\sqrt{x+a} + \sqrt{x+b}} \cdot \dfrac{\sqrt{x+a} - \sqrt{x+b}}{\sqrt{x+a} - \sqrt{x+b}}
$$

By the difference-of-squares identity $(u+v)(u-v) = u^2 - v^2$, with
$u = \sqrt{x+a}$ and $v = \sqrt{x+b}$, the denominator becomes:

$$
(\sqrt{x+a})^2 - (\sqrt{x+b})^2 = (x+a) - (x+b) = a - b
$$

The $x$'s cancel and the denominator is a constant.

## Putting It Together

The integral is now:

$$
\int \dfrac{dx}{\sqrt{x+a} + \sqrt{x+b}} = \dfrac{1}{a - b} \int \left( \sqrt{x+a} - \sqrt{x+b} \right) dx
$$

Each piece is a power-rule integral. Using $\int (x+c)^{1/2} \, dx = \tfrac{2}{3}(x+c)^{3/2}$:

$$
\int \sqrt{x+a} \, dx = \dfrac{2}{3}(x+a)^{3/2}
$$

$$
\int \sqrt{x+b} \, dx = \dfrac{2}{3}(x+b)^{3/2}
$$

So:

$$
\int \dfrac{dx}{\sqrt{x+a} + \sqrt{x+b}} = \dfrac{2}{3(a-b)} \left[ (x+a)^{3/2} - (x+b)^{3/2} \right] + C
$$

## Sanity Check by Differentiation

Let

$$
F(x) = \dfrac{2}{3(a-b)} \left[ (x+a)^{3/2} - (x+b)^{3/2} \right]
$$

Differentiating:

$$
F'(x) = \dfrac{2}{3(a-b)} \cdot \dfrac{3}{2} \left[ (x+a)^{1/2} - (x+b)^{1/2} \right] = \dfrac{\sqrt{x+a} - \sqrt{x+b}}{a-b}
$$

To match the original integrand, multiply top and bottom by $\sqrt{x+a} + \sqrt{x+b}$:

$$
\dfrac{\sqrt{x+a} - \sqrt{x+b}}{a - b} \cdot \dfrac{\sqrt{x+a} + \sqrt{x+b}}{\sqrt{x+a} + \sqrt{x+b}} = \dfrac{(x+a) - (x+b)}{(a-b)(\sqrt{x+a} + \sqrt{x+b})}
$$

The numerator is $a - b$, which cancels, leaving:

$$
F'(x) = \dfrac{1}{\sqrt{x+a} + \sqrt{x+b}}
$$

## The $a = b$ Case

The answer has $a - b$ in the denominator, so it's undefined at $a = b$. But
the original integral degenerates there: the denominator becomes $2\sqrt{x+a}$
and

$$
\int \dfrac{dx}{2\sqrt{x+a}} = \sqrt{x+a} + C
$$

The singularity is removable — taking $b \to a$ in the closed form (via
L'Hôpital or a Taylor expansion of $(x+b)^{3/2}$ around $b = a$) recovers
$\sqrt{x+a} + C$.

## References

- G. H. Hardy, *A Course of Pure Mathematics*, Cambridge University Press.
  [Available on Project Gutenberg.](https://www.gutenberg.org/ebooks/38769)
- Wikipedia, [Rationalisation (mathematics)](https://en.wikipedia.org/wiki/Rationalisation_(mathematics)).
