Title: Baby Poker: The Smallest Interesting Bluffing Game
Date: 2026-08-25 20:00
Category: Mathematics
Tags: game theory, probability, poker, nash equilibrium, riddler

Baby Poker is a two-player dice game that fits on a napkin and still
manages to be a real bluffing game. Each player rolls a single die
concealed in a cup. There is one round of betting. That is it. And yet
the optimal strategy involves mixed frequencies, a value range, a
bluffing range, and a call/fold cutoff. It is the smallest game I know
of that has all the moving parts of full poker.

Our working notes: [Baby Poker](https://charlesreid1.com/wiki/Baby_Poker).

## The Problem

This one comes from the FiveThirtyEight *Riddler* column (now
defunct, but happily still on the Wayback Machine):
[Can You Deal With These Card Game Puzzles?](https://web.archive.org/web/20240222120450/https://fivethirtyeight.com/features/can-you-deal-with-these-card-game-puzzles/).

The rules:

* Each player antes $1.
* Both roll a single die in a cup and look only at their own die.
* Player A acts first: **call** (both dice shown, higher wins the $2
  pot) or **raise** (bet another dollar).
* If A raises, Player B chooses **call** (match the dollar, higher wins
  the $4 pot) or **fold** (A takes the pot, B loses only the ante).
* Ties in a called pot split equally.

Two questions:

* What is the optimal strategy for each player?
* How much is the game worth to Player A? (Equivalently, how much
  should A pay B up front to make it fair?)

## Setting Up the Game

Let $x \in \{1,\dots,6\}$ be A's roll and $y \in \{1,\dots,6\}$ be
B's. Let $p_x$ be the probability A raises given $x$, and $q_y$ the
probability B calls a raise given $y$. The strategy for each player is
a vector of six numbers in $[0,1]$.

Because this is a zero-sum game of imperfect information, we are
looking for a **Nash equilibrium**: a pair of strategies $(p, q)$ such
that neither player can improve their expected value by deviating,
holding the other player's strategy fixed. The standard tool is the
**indifference principle**: at equilibrium, if a player mixes between
two actions with a given hand, they must be *indifferent* between
those actions. Otherwise they would just pick the better one and stop
mixing.

That gives us two levers to pull. B's calling frequencies $q_y$ must
be tuned so that A is indifferent to bluffing with the worst hand.
A's raising frequencies $p_x$ must be tuned so that B is indifferent
to calling with the marginal hands.

## Player B's Indifference

B only has to think when A has raised. Given a raise, folding costs B
one dollar (the ante). Calling puts B in for two more dollars into a
four-dollar pot, and the payoff depends on how A's raising range
$p_x$ is distributed.

B's EV of calling with roll $y$, conditional on A having raised, is

$$
E_B(\text{Call} \mid y) = \frac{1}{\sum_x p_x}
\left( \sum_{x<y}(+2)p_x + \sum_{x=y}(0)p_x + \sum_{x>y}(-2)p_x \right).
$$

Setting this equal to $-1$ (the EV of folding) and clearing the
denominator gives B's indifference condition on A's range:

$$
3\sum_{x<y} p_x + p_y - \sum_{x>y} p_x = 0.
$$

## Player A's Range: Value and Bluffs

The shape of A's optimal range falls out of two observations.

**Top of the range is trivial.** A should always raise with 5 and 6.
These are the hands most likely to win at showdown, and if you don't
raise them you leave money on the table. So $p_5 = p_6 = 1$.

**Bluffing balances the range.** If A only ever raised with strong
hands, B would just always fold and A would never get paid off. So A
has to raise with some bad hands too, to keep B honest. The cleanest
choice is to bluff with the *worst* hand ($x=1$). A middling hand
like 3 has real showdown equity that gets wasted by turning it into a
bluff, but a 1 has almost none.

So the trial strategy is: value-bet with 5 and 6, call with 2, 3, 4,
and bluff some fraction $p_1$ of the time with 1.

Plug this into B's indifference formula at the boundary hand $y=3$
(the marginal hand B might call with):

$$
3 p_1 + 0 - (p_5 + p_6) = 0
\;\implies\; 3 p_1 - 2 = 0
\;\implies\; p_1 = \tfrac{2}{3}.
$$

A bluffs with 1 exactly two-thirds of the time.

## Player B's Range

Same trick from the other side. A must be indifferent between calling
and raising when holding the worst hand. Calling with $x=1$ has EV

$$
E_A(\text{Call} \mid x=1) = \tfrac{1}{6}(0 - 1 - 1 - 1 - 1 - 1) = -\tfrac{5}{6}.
$$

Raising with $x=1$ wins one dollar when B folds and loses two when B
calls (a 1 loses to anything but a tie, and there is no tie with a
1). Letting $S_q = \sum_y q_y$,

$$
E_A(\text{Raise} \mid x=1)
= \left(1 - \tfrac{S_q}{6}\right)(1) + \tfrac{S_q}{6}(-2)
= 1 - \tfrac{S_q}{2}.
$$

Equating and solving: $S_q = \tfrac{11}{3}$.

B always folds 1 and always calls 5 and 6 (again, the extremes are
easy), so $q_2 + q_3 + q_4 = \tfrac{11}{3} - 2 = \tfrac{5}{3}$. The
monotone solution is $q_2 = 0$, $q_3 = \tfrac{2}{3}$, $q_4 = 1$.

## The Answer

**Player A.** Always raise with 5 and 6. Always call with 2, 3, 4.
Raise with 1 exactly $\tfrac{2}{3}$ of the time.

**Player B (facing a raise).** Always call with 4, 5, 6. Always fold
with 1 and 2. Call with 3 exactly $\tfrac{2}{3}$ of the time.

Averaging A's conditional EV over all six rolls (the arithmetic is on
[the wiki](https://charlesreid1.com/wiki/Baby_Poker)), the value of
the game is

$$
\text{EV}(A) = \tfrac{5}{54} \approx 0.093.
$$

Acting first is worth about a dime a hand. A gets to pick the timing
of the bluffs and force B into a mixing spot. To make the game fair,
A pays B $\tfrac{5}{54}$ of a dollar per hand up front.

## What It Teaches

The real point of Baby Poker is that it is a toy problem for **game
theory**. It is small enough to solve by hand, and it exercises the
full machinery: a two-player zero-sum game of imperfect information,
solved by finding a Nash equilibrium in mixed strategies via the
indifference principle. That is exactly the same math von Neumann and
Morgenstern set up in *Theory of Games and Economic Behavior*, just
shrunk to a six-sided die.

Baby Poker is a good teaching game because it has *exactly* the pieces
of full poker and nothing else:

* A **value range** (raise with 5, 6): hands you want called.
* A **bluff range** (raise with 1 sometimes): hands you want to fold
  out better hands.
* A **calling range** (call with 2, 3, 4): hands with showdown equity
  you don't want to inflate the pot with.
* A **mixed frequency** ($\tfrac{2}{3}$) that ties the two players
  together via indifference.
* A **positional advantage**: acting first is worth real money because
  you get to define the ranges the second player has to respond to.

Every one of those concepts is a game-theoretic construct that
survives all the way up to no-limit Texas hold 'em. Baby Poker just
strips the game down to the smallest version where the full solution
concept (Nash equilibrium in mixed strategies) still has all its
moving parts.

## References

* Our wiki notes:
  [Baby Poker](https://charlesreid1.com/wiki/Baby_Poker)
* [Can You Deal With These Card Game Puzzles?](https://web.archive.org/web/20240222120450/https://fivethirtyeight.com/features/can-you-deal-with-these-card-game-puzzles/),
  the original FiveThirtyEight Riddler column (archived)
* Related: [Enumeration Solitaire](https://charlesreid1.com/wiki/Enumeration_Solitaire),
  the other puzzle from the same column
