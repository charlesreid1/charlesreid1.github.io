Title: A Hard(y) Math Problem
Date: 2017-11-03 19:00
Category: Mathematics
Tags: mathematics, calculus, integrals, hardy, cambridge, tripos

## An Integral from Hardy

Every once in a while you run across an integral that looks straightforward
at first glance, but the more you stare at it, the less obvious it becomes
how to proceed. This is one of those integrals. It's the sort of problem that
G. H. Hardy - the great English mathematician who taught at Cambridge for
decades and famously collaborated with Ramanujan - liked to pose to students
as a way to sharpen their instincts about integration.

Here's the integral:

$$
\int \dfrac{dx}{\sqrt{x+a} + \sqrt{x+b}}
$$

At a glance, this doesn't fit any of the standard forms you memorize as an
undergraduate. There's no obvious $u$-substitution. Integration by parts
doesn't lead anywhere useful. And trying to attack it head-on with a
trigonometric substitution leads to a mess. It's the kind of integral that
makes you wonder whether it even has a closed-form solution at all.

It does. And the trick is a delightful one.

## The Setup: Why This Is Hard

The difficulty here is entirely due to the shape of the denominator. If we
had just $\sqrt{x+a}$ in the denominator, this would be a trivial
power-rule integral:

$$
\int \dfrac{dx}{\sqrt{x+a}} = 2\sqrt{x+a} + C
$$

Similarly for $\sqrt{x+b}$. But the *sum* of two square roots in the
denominator is what gums up the works. You can't distribute the reciprocal
across a sum. You can't easily substitute for the whole denominator, because
its derivative involves both roots in a form that doesn't cleanly cancel
anything in the numerator. The two square roots are entangled in a way that
resists most of the standard tools.

The way out isn't a substitution at all. It's an algebraic manipulation you
learned in high school, applied in a place you weren't expecting to see it.

## The Trick: Multiply by the Conjugate

The move is to multiply the numerator and denominator by the *conjugate* of
the denominator - that is, by $\sqrt{x+a} - \sqrt{x+b}$:

$$
\dfrac{1}{\sqrt{x+a} + \sqrt{x+b}} \cdot \dfrac{\sqrt{x+a} - \sqrt{x+b}}{\sqrt{x+a} - \sqrt{x+b}}
$$

This is the same trick you use to rationalize a denominator in algebra
class. The reason it works is the difference-of-squares identity:

$$
(u + v)(u - v) = u^2 - v^2
$$

When $u$ and $v$ are square roots, squaring them strips them away entirely.
Applying that identity with $u = \sqrt{x+a}$ and $v = \sqrt{x+b}$, the
denominator becomes:

$$
(\sqrt{x+a})^2 - (\sqrt{x+b})^2 = (x+a) - (x+b) = a - b
$$

The two $x$'s cancel exactly, and we're left with a *constant* in the
denominator. That's the whole game. The nasty entangled denominator collapses
into $a - b$, and the two square roots that were causing all the trouble
have moved up into the numerator, where they can be integrated independently.

## Putting It Together

After the conjugate multiplication, the integral becomes:

$$
\int \dfrac{dx}{\sqrt{x+a} + \sqrt{x+b}} = \dfrac{1}{a - b} \int \left( \sqrt{x+a} - \sqrt{x+b} \right) dx
$$

Now each piece is a straightforward power-rule integral. Using
$\int (x+c)^{1/2} \, dx = \tfrac{2}{3}(x+c)^{3/2}$:

$$
\int \sqrt{x+a} \, dx = \dfrac{2}{3}(x+a)^{3/2}
$$

$$
\int \sqrt{x+b} \, dx = \dfrac{2}{3}(x+b)^{3/2}
$$

Putting it all together:

$$
\int \dfrac{dx}{\sqrt{x+a} + \sqrt{x+b}} = \dfrac{2}{3(a-b)} \left[ (x+a)^{3/2} - (x+b)^{3/2} \right] + C
$$

That's the answer. Clean, symmetric, and once you see it, obvious in
retrospect - which is the hallmark of a good trick.

## Sanity Check by Differentiation

It's always worth verifying an integral by differentiating and checking that
we recover the original integrand. Let

$$
F(x) = \dfrac{2}{3(a-b)} \left[ (x+a)^{3/2} - (x+b)^{3/2} \right]
$$

Differentiating term by term with the chain rule (the derivative of $x+a$ is
just 1, so the chain rule contributes nothing here):

$$
F'(x) = \dfrac{2}{3(a-b)} \cdot \dfrac{3}{2} \left[ (x+a)^{1/2} - (x+b)^{1/2} \right] = \dfrac{\sqrt{x+a} - \sqrt{x+b}}{a-b}
$$

Now we need to show that this equals $\dfrac{1}{\sqrt{x+a} + \sqrt{x+b}}$.
Multiply the top and bottom of our derivative by $\sqrt{x+a} + \sqrt{x+b}$:

$$
\dfrac{\sqrt{x+a} - \sqrt{x+b}}{a - b} \cdot \dfrac{\sqrt{x+a} + \sqrt{x+b}}{\sqrt{x+a} + \sqrt{x+b}} = \dfrac{(x+a) - (x+b)}{(a-b)(\sqrt{x+a} + \sqrt{x+b})}
$$

The numerator simplifies to $a - b$, which cancels with the $a - b$ in the
denominator, leaving:

$$
F'(x) = \dfrac{1}{\sqrt{x+a} + \sqrt{x+b}}
$$

Confirmed.

## What About $a = b$?

You may have noticed the answer contains $a - b$ in the denominator, which
looks alarming if $a = b$. But if $a = b$, the original integral degenerates:
the denominator becomes $2\sqrt{x+a}$, and the integral is just

$$
\int \dfrac{dx}{2\sqrt{x+a}} = \sqrt{x+a} + C
$$

So the interesting case - the one worth Hardy's attention - is when $a \neq
b$, and the formula is well-defined there. The apparent singularity at $a =
b$ is removable: if you take the limit of the closed-form answer as $b \to
a$ using L'Hôpital's rule or a Taylor expansion of $(x+b)^{3/2}$ around $b =
a$, you recover exactly $\sqrt{x+a} + C$. The answer is consistent with the
degenerate case, it just has to be teased out with a limit.

## Why This Matters

The pattern here - multiply by the conjugate to rationalize away a sum of
square roots - is worth stashing away in your bag of tricks. It shows up
more often than you'd expect, and not just in integration. Any time you have
an expression of the form $\sqrt{P} + \sqrt{Q}$ that's obstructing an
algebraic manipulation, ask yourself whether the conjugate $\sqrt{P} -
\sqrt{Q}$ would give you a cleaner form via the difference-of-squares
identity.

That's the beauty of a problem like this one. It's not that the mathematics
is deep, or that the answer is exotic. It's that the *technique* is
transferable. Hardy's problems tend to have this quality: they force you to
recognize a pattern that then generalizes far beyond the specific problem in
front of you. You learn the pattern once, and afterwards you see it
everywhere.

## References

- G. H. Hardy, *A Course of Pure Mathematics*, Cambridge University Press.
  [Available on Project Gutenberg.](https://www.gutenberg.org/ebooks/38769)
- Wikipedia, [Rationalisation (mathematics)](https://en.wikipedia.org/wiki/Rationalisation_(mathematics)).
