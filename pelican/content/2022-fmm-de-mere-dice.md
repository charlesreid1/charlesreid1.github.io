Tpelican/content/2022-fmm-de-mere-dice.mditle: A Pair of Dice Games (or, Why Chevalier de Méré Lost Money)
Date: 2022-10-22 22:00
Category: Mathematics
Tags: mathematics, probability, dice, pascal, friday morning math
Status: draft

Here is a nice little problem from Paul Nahin's *Will You Be Alive 10 Years
From Now?*. It is a problem from the 1654 correspondence between Antoine
Gombaud (the Chevalier de Méré) and Blaise Pascal - one of the founding
episodes of probability theory, dressed up as a gambling puzzle.

(This one lives on our wiki as
[FMM21](https://charlesreid1.com/wiki/FMM21), part of our Friday Morning
Math Problem series.)

## The Two Games

**Game 1.** You toss a single die $N_1$ times. What should $N_1$ be to make
the probability of seeing at least one 6 greater than $\tfrac{1}{2}$?

**Game 2.** You toss a *pair* of dice $N_2$ times. What should $N_2$ be to
make the probability of seeing at least one double 6 greater than
$\tfrac{1}{2}$?

In gambling terms, the question is: what is the smallest $N$ that turns an
even-money bet on "at least one 6" (or "at least one double 6") into a bet
that favors the gambler rather than the house?

## Game 1

Pascal's trick is to count the complement. There are $6^{N_1}$ ways for the
die to land over $N_1$ tosses, and $5^{N_1}$ of them have no 6 at all. So

$$
P_1 = 1 - \left(\dfrac{5}{6}\right)^{N_1}
$$

We want $P_1 > \tfrac{1}{2}$, which is easiest to just tabulate:

* $N_1 = 1$: $P_1 = 0.167$
* $N_1 = 2$: $P_1 = 0.306$
* $N_1 = 3$: $P_1 = 0.421$
* $N_1 = 4$: $P_1 = 0.518$

So $N_1 = 4$.

## Game 2

Same trick with a pair of dice. The probability of a double 6 on a single
toss is $\tfrac{1}{36}$, so the probability of *not* rolling a double 6 is
$\tfrac{35}{36}$, and

$$
P_2 = 1 - \left(\dfrac{35}{36}\right)^{N_2}
$$

Tabulating:

* $N_2 = 24$: $P_2 = 0.491$
* $N_2 = 25$: $P_2 = 0.506$

So $N_2 = 25$.

## Gombaud's Mistake

Here is the fun part.

Gombaud believed in *strict proportionality*. He reasoned that since Game 1
had 6 outcomes per toss and Game 2 had 36 outcomes per toss, the answers
should be related by

$$
\dfrac{N_1}{6} = \dfrac{N_2}{36}
$$

With $N_1 = 4$, that gives $N_2 = 24$. And Gombaud, who was a very careful
gambler, actually played this game for money on the belief that $N_2 = 24$
was the tipping point.

But it turns out that $N_2 = 24$ gives a probability of $0.491$, which is
just barely on the wrong side of $\tfrac{1}{2}$. Gombaud noticed, over a
large number of games, that he was consistently losing money at $N_2 = 24$.
Being unable to figure out why, he wrote to Pascal.

The intuition that ratios of counts should scale linearly is one of those
things that feels obviously true and is very quietly false. The correct
answer is off by one - $N_2 = 25$, not $24$ - and that one integer of
difference was enough to drain the Chevalier's purse.

## The Moral

There are two morals, depending on your temperament:

* If you are a probability theorist, the moral is: complementary events are
  your friend, and multiplying $\tfrac{5}{6}$ by itself is a lot easier than
  enumerating all the ways to see at least one 6.

* If you are a gambler, the moral is: do not let intuition about ratios
  substitute for actual arithmetic, and if a French nobleman offers you an
  even-money bet on rolling a double 6 in 24 throws, take it.

## More

* [FMM21 on our wiki](https://charlesreid1.com/wiki/FMM21) - the full
  problem and solution
* [All Friday Morning Math Problems](https://charlesreid1.com/wiki/Category:FMM)
