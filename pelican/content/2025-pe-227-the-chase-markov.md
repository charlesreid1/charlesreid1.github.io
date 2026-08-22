Title: Project Euler 227 (The Chase): When Brute Force Costs 80 Days
Date: 2025-04-19 20:00
Category: Mathematics
Tags: project euler, markov chains, probability, brute force, fundamental matrix

[Project Euler problem 227](https://projecteuler.net/problem=227) - "The
Chase" - is a nice example of a problem where the brute force approach
is completely reasonable to reach for first, completely infeasible to
actually finish, and directly points you at the right mathematical
reformulation.

This is what we ended up with. Our full working notes are on the wiki at
[Project Euler/227](https://charlesreid1.com/wiki/Project_Euler/227).

## The Problem

An even number of players sit around a table. Two players sitting
directly opposite each other each start with a die. Each round, both
players roll:

* Roll a 1 → pass the die to your left neighbor
* Roll a 6 → pass the die to your right neighbor
* Anything else → keep the die

The game ends when one player is holding both dice at the end of a
round. That player loses.

The question: with 100 players, what is the expected number of rounds
before someone loses?

## Reaching For the Brute Force

The first thing we did was write a very small Python simulator. Two
integer pointers, one per die. Each round, roll two dice, update each
pointer with `+1`, `-1`, or nothing, modulo the number of players. Stop
when the pointers collide. Average over many trials.

This works. It gives you an estimate that gets more accurate as you run
more trials. And then you start measuring how expensive that gets.

The cost has two knobs:

* **Trials.** Linear. Four decimal places of accuracy needs about 1,000
  trials. Ten decimal places needs billions.
* **Players.** Not linear. Playing with 5, 10, 15, 20, and 25 players
  and measuring, the runtime looked quadratic in the number of players.

So the total execution time is roughly

$$
T(N, S) \approx c \cdot S \cdot N^2
$$

Extrapolating our measured constant `c` from small experiments up to
`N = 100` players and `S = 9` billion trials (to get sufficient accuracy
on the answer), we got about **7,000,000 seconds**. Call it 80 days.

Project Euler problems are supposed to have solutions that run in about
a minute. 80 days is not a minute. Even switching to a compiled language
and multithreading, we would need a **10,000×** speedup to get into the
right ballpark. And the loop body is already about as tight as a loop
body gets - two random integers, two pointer updates, a comparison.
There is not much to optimize.

So the brute force is out. What is it about the problem that makes brute
force so bad, and what does the answer look like if we ask a different
question?

## Reformulating as a Markov Chain

The key observation is that the game has no memory. The next state only
depends on the current state. That is the definition of a Markov chain.

The **state** is the pair of positions of the two dice, `(i, j)`, where
`i` and `j` are player indices in `{0, 1, ..., N-1}`. For 100 players,
that's a state space with 10,000 pairs, minus the 100 pairs where `i = j`
(dice have collided - game over). So we have 9,900 transient states and
100 absorbing states.

Note: `(i, j)` and `(j, i)` represent the same physical situation. There
is a symmetry we could exploit to cut the state count roughly in half,
but for the initial derivation we ignored it and paid the extra factor.

Transitions: each die independently keeps, moves left, or moves right,
with probabilities `4/6`, `1/6`, `1/6`. So the joint transition from
`(i, j)` to `(i', j')` has probability equal to the product of the two
individual probabilities. Each transient state has at most 9 possible
next states (3 outcomes per die × 3 outcomes per die).

## The Fundamental Matrix

The clean way to compute expected time to absorption in a finite Markov
chain is via the **fundamental matrix**. It works like this.

Arrange the states so transient states come first and absorbing states
come second. Then the transition probability matrix has the block form

$$
P = \begin{bmatrix} Q & R \\ 0 & I \end{bmatrix}
$$

where

* `Q` is `t × t`, the transition probabilities among transient states
* `R` is `t × r`, the transitions from transient to absorbing states
* `0` and `I` in the bottom row represent the fact that absorbing states
  don't leave themselves

The **fundamental matrix** is

$$
N = (I - Q)^{-1}
$$

Entry `N[i, j]` gives the expected number of visits to transient state
`j` before absorption, starting from transient state `i`. That means the
expected number of steps until absorption, starting from state `i`, is
the sum of row `i` of `N`.

Or equivalently: solve the linear system `(I - Q) x = 1`, where `1` is a
column of ones. Entry `x[i]` is the expected number of steps starting
from state `i`.

## Building Q for 100 Players

For 100 players there are `100 × 99 = 9900` transient states. `Q` is
`9900 × 9900`. We only need to fill in the roughly nine nonzero entries
per row, so `Q` is very sparse.

Two things to get right when you build it:

1. **State-to-index mapping.** Some canonical ordering of the `(i, j)`
   pairs with `i ≠ j`. Any consistent bijection between pairs and row
   indices works.
2. **Iterating over next states.** For each `(i, j)`, enumerate the nine
   `(i', j')` transitions. For each, check whether `i' = j'` (in which
   case that probability mass flows to an absorbing state and doesn't
   go into `Q`).

Then invert `I - Q`, sum the row of `N` that corresponds to the starting
state `(0, 50)` (opposite sides of the table), and you have your answer.

## The Uncomfortable Confession

Ours took **1,687 seconds** to run. Twenty-eight minutes. Better than 80
days, but not great.

The slow part is inverting the 9,900 × 9,900 matrix. We tried
reformulating as a linear solve `(I - Q) x = 1` and using LU
decomposition instead of computing the full inverse, on the theory that
LU should be faster. It was almost twice as slow. That was a surprise
but probably a story about the specific dense linear algebra library we
were using rather than a fundamental issue.

The obvious next moves we did *not* take:

* **Sparse matrix representation.** `Q` has at most 9 nonzeros per row
  out of 9,900. Using a proper sparse solver would probably drop us into
  the seconds.
* **Exploit the symmetry.** Treating `(i, j)` and `(j, i)` as the same
  state cuts the matrix size in half. Combined with sparsity, this
  should be very fast.
* **Iterative methods.** The system `(I - Q) x = 1` is a great candidate
  for something like BiCGSTAB or GMRES, which don't build the inverse at
  all.

## The Real Solution Times

For fun, we looked at the Project Euler forum posts after we submitted.
The first person to solve it did it in **0.1 seconds in C++ in 2009**.
That is 16,000× faster than ours.

They used a completely different approach, involving grouping the six
die outcomes into three groups (`+1`, `-1`, keep) and using symmetries
to reduce the state space dramatically. There is a shape of insight that
turns "big linear algebra problem" into "small closed-form recurrence"
that we did not find.

Some of the fun of Project Euler is exactly this: finishing the problem,
submitting the answer, and then finding out that half the people who
solved it did it 10,000× faster with a technique you did not think of.
The correct response is not embarrassment. It is to open the forum, read
their write-ups, and steal their trick for next time.

## References

* Our full notes:
  [Project Euler/227](https://charlesreid1.com/wiki/Project_Euler/227)
* [PE 227 on projecteuler.net](https://projecteuler.net/problem=227)
* Fundamental matrix: standard reference is Kemeny & Snell, *Finite
  Markov Chains* (1960)
