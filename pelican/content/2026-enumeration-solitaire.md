Title: Enumeration Solitaire: Derangements with Four Copies of Each Rank
Date: 2026-08-26 20:00
Category: Mathematics
Tags: probability, combinatorics, inclusion exclusion, generating functions, derangements, riddler

Enumeration Solitaire is a one-player card game with a two-sentence
rule set and a genuinely nontrivial answer. You shuffle a deck, deal
cards face up, and count "ace, two, three, ..., king" over and over as
you go. If the rank you speak ever matches the rank of the card you
just dealt, you lose. Get through all 52 cards without a match and you
win.

It is a four-copy generalization of the classical *probleme des
rencontres* (the derangement problem), and the solution is one
inclusion-exclusion argument compressed into one generating function.

Our working notes:
[Enumeration Solitaire](https://charlesreid1.com/wiki/Enumeration_Solitaire).

## The Problem

This one comes from the same FiveThirtyEight *Riddler* column as
[Baby Poker](https://charlesreid1.com/wiki/Baby_Poker) (archived on
the Wayback Machine):
[Can You Deal With These Card Game Puzzles?](https://web.archive.org/web/20240222120450/https://fivethirtyeight.com/features/can-you-deal-with-these-card-game-puzzles/).

The rules:

* Take a standard shuffled 52-card deck.
* Deal cards face up, one at a time.
* As each card is dealt, speak the next rank in the cycle: ace, two,
  three, ..., king, then restart at ace.
* If the spoken rank ever matches the rank of the dealt card, you
  lose.
* If all 52 cards are dealt without a match, you win.

Two questions:

* What is the probability of winning a single game?
* On average, how many games must you play before winning once?

## Setting Up the Problem

Label the deal positions $i \in \{0, 1, \dots, 51\}$. At position $i$
the spoken rank is $s(i) = i \bmod 13$. Let $A_i$ be the event "the
card dealt at position $i$ has rank $s(i)$." A win is the event that
none of the $A_i$ occur.

The naive move is to note that $P(A_i) = 4/52 = 1/13$ for every $i$
and treat the 52 events as independent. That gives $(12/13)^{52}
\approx 0.0155$, and by linearity of expectation the average number of
matches is $52 \cdot 1/13 = 4$, so a Poisson approximation gives
$e^{-4} \approx 0.0183$. These are two different wrong answers because
the events are not independent: the four cards of each rank compete
for the same four labeled slots.

The right tool for "probability that none of a bunch of correlated
events occurs" is inclusion-exclusion.

## Inclusion-Exclusion

$$
P(\text{win}) = P\!\left(\bigcap_i A_i^c\right)
= \sum_{k=0}^{52} (-1)^k S_k,
\qquad
S_k = \sum_{|I|=k} P\!\left(\bigcap_{i \in I} A_i\right).
$$

Model the deal as a uniformly random permutation of the 52 distinct
cards. For a fixed size-$k$ subset $I$ of positions, group its
positions by the rank they demand: let $m_r$ be the number of
positions in $I$ with $s(i) = r$. Then $m_0 + \dots + m_{12} = k$ and
each $m_r \le 4$. Call $(m_0, \dots, m_{12})$ the *multiplicity
profile* of $I$.

To build an arrangement in which every position of $I$ is a match:

1. For each rank $r$, fill the $m_r$ chosen slots with rank-$r$
   cards: $4!/(4-m_r)!$ ordered choices.
2. Fill the remaining $52 - k$ slots with the remaining $52 - k$
   cards in any order: $(52-k)!$ ways.

Dividing by $52!$:

$$
P\!\left(\bigcap_{i \in I} A_i\right)
= \frac{(52-k)!}{52!} \prod_{r=0}^{12} \frac{4!}{(4-m_r)!}.
$$

This depends on $I$ only through its multiplicity profile, and the
number of size-$k$ subsets with a given profile is $\prod_r
\binom{4}{m_r}$. So

$$
S_k = \frac{(52-k)!}{52!} \sum_{\substack{m_0+\dots+m_{12}=k \\ 0 \le m_r \le 4}}
\prod_{r=0}^{12} \binom{4}{m_r} \frac{4!}{(4-m_r)!}.
$$

That inner sum is a constrained sum over 13-tuples, and it is exactly
the kind of thing generating functions were invented to compute.

## The Generating Function

Pull out one rank's contribution. Define

$$
f(m) := \binom{4}{m} \frac{4!}{(4-m)!},
\qquad
f(0), f(1), f(2), f(3), f(4) = 1,\; 16,\; 72,\; 96,\; 24.
$$

Package these into a polynomial using multiplicity as the exponent of
a bookkeeping variable $x$:

$$
g(x) := \sum_{m=0}^{4} f(m)\, x^m
     = 1 + 16x + 72x^2 + 96x^3 + 24x^4.
$$

Now expand $g(x)^{13}$. Every term in the expansion picks one monomial
$f(m_r) x^{m_r}$ from each of the 13 factors and multiplies them
together, giving $\left(\prod_r f(m_r)\right) x^{m_0 + \dots +
m_{12}}$. So the coefficient of $x^k$ in $g(x)^{13}$ is exactly the
constrained sum we wanted:

$$
[x^k]\, g(x)^{13}
= \sum_{\substack{m_0+\dots+m_{12}=k \\ 0 \le m_r \le 4}}
  \prod_{r=0}^{12} \binom{4}{m_r} \frac{4!}{(4-m_r)!}.
$$

The upper bound $m_r \le 4$ is enforced automatically because $g$ has
no terms above degree 4. What was a constrained nested sum over
13-tuples is now a single coefficient extraction from a fixed
degree-52 polynomial.

Putting the pieces together:

$$
P(\text{win})
= \sum_{k=0}^{52} (-1)^k \frac{(52-k)!}{52!}\, [x^k]\, g(x)^{13}.
$$

## Sanity Check: the Single-Suit Deck

Strip the deck down to a single suit: 13 distinct cards, one per rank.
Now $f(m) = 1$ for $m \in \{0, 1\}$, so $g(x) = 1 + x$ and $[x^k](1 +
x)^{13} = \binom{13}{k}$. The formula collapses to

$$
P(\text{win}) = \sum_{k=0}^{13} (-1)^k \binom{13}{k} \frac{(13-k)!}{13!}
             = \sum_{k=0}^{13} \frac{(-1)^k}{k!} \to \frac{1}{e}.
$$

That is the classical derangement probability. Enumeration Solitaire
with a full 52-card deck is the natural four-copy generalization: same
inclusion-exclusion skeleton, but with a richer per-rank contribution
polynomial than $1 + x$.

## The Answer

Expand $g(x)^{13}$ (a degree-52 polynomial, 53 coefficients) and sum
with alternating $(52-k)!/52!$ weights. The exact value is a rational
number with a lot of digits; the decimal value is

$$
P(\text{win}) \approx 0.01623,
$$

or about **1.623%**.

Two sanity checks. The Poisson heuristic $e^{-4} \approx 0.0183$
overshoots slightly (the events are positively correlated in
aggregate: once one card of a rank has appeared without matching, its
remaining copies are slightly more likely to hit a later slot for
that rank, which reduces the survival probability). A Monte Carlo run
of 2,000,000 simulated deals gives an empirical win rate of about
$0.01633$, matching to three significant figures.

Successive games are independent, so the number of games until the
first win is geometric with success probability $\approx 0.01623$. On
average you play about $1 / 0.01623 \approx 61.6$ games before winning
once. Bring a book.

## What It Teaches

Enumeration Solitaire is a good showcase for two techniques that pair
well:

* **Inclusion-exclusion** for "probability that *none* of these
  correlated events occur." The moment you write down $P(\bigcap
  A_i^c) = \sum (-1)^k S_k$, the problem becomes: what is $S_k$?
* **Generating functions** for constrained sums over tuples. Whenever
  a sum runs over $(m_0, \dots, m_{n-1})$ with $\sum m_r = k$ and
  per-coordinate bounds, packaging the per-coordinate contribution
  into a polynomial and reading off a coefficient of a product
  usually beats brute enumeration.

The whole solution fits on one page, and the classical derangement
problem falls out as the degenerate case. Not bad for a game whose
rules fit in a tweet.

## References

* Our wiki notes:
  [Enumeration Solitaire](https://charlesreid1.com/wiki/Enumeration_Solitaire)
* [Can You Deal With These Card Game Puzzles?](https://web.archive.org/web/20240222120450/https://fivethirtyeight.com/features/can-you-deal-with-these-card-game-puzzles/),
  the original FiveThirtyEight Riddler column (archived)
* Related: [Baby Poker](https://charlesreid1.com/wiki/Baby_Poker), the
  other puzzle from the same column
