Title: Ken Binmore's <i>Game Theory</i> and Nash Equilibrium in Shadowrun
Date: 2025-05-17 20:00
Category: Reading
Tags: reading, game theory, binmore, nash equilibrium, shadowrun, ttrpg, mathematics

We spent part of May 2025 reading Ken Binmore's *Game Theory: A Very
Short Introduction* (Oxford, 2007). It is a 176-page book that has no
business covering as much ground as it does. It is also the book that
gave us the excuse to work out a Nash equilibrium calculation for a
Shadowrun run, which we have been wanting to do for a while.

Full notes on the wiki:
[Game Theory - A Very Short Introduction](https://charlesreid1.com/wiki/Game_Theory_-_A_Very_Short_Introduction).

## Why This Book

Game theory has a reputation for being either trivial (rock-paper-
scissors and Prisoner's Dilemma) or impenetrable (Von Neumann's
*Theory of Games and Economic Behavior* is 700+ pages). Binmore
threads a needle: real coverage of the mathematical structure of
Nash equilibrium, mixed strategies, backward induction, mechanism
design, and evolutionary game theory - all in fewer pages than most
introductory textbooks devote to a single chapter.

The 10 chapters:

1. The name of the game (Nash equilibrium, utility, revealed preference)
2. Chance (mixed strategies, indifference, Von Neumann's minimax)
3. Time (backward induction, subgame-perfect equilibrium, common
   knowledge)
4. Conventions (focal points, coordination games, tragedy of the commons)
5. Reciprocity (repeated games, folk theorem, TIT-FOR-TAT)
6. Information (imperfect information, Harsanyi types, costly signals)
7. Auctions (mechanism design, revenue equivalence, winner's curse)
8. Evolutionary biology (evolutionarily stable strategies, Hawk-Dove,
   Hamilton's rule)
9. Bargaining and coalitions (Nash bargaining, Rubinstein alternating
   offers, Shapley value)
10. Puzzles and paradoxes (Newcomb, surprise test, common knowledge)

Any one of those chapters is a legitimate subject for a graduate
course. Binmore covers each in 15-20 pages by ruthlessly cutting the
formalism where the intuition suffices, and using clear worked
examples where the formalism doesn't.

## The Idea That Kept Us Up

The chapter that stuck with us was Chapter 2: Chance. Specifically,
the *indifference principle* for mixed-strategy Nash equilibria.

The setup: some games (Matching Pennies is the canonical example)
have no equilibrium in pure strategies. There is no stable choice of
"always play Heads" or "always play Tails" - whatever you commit to,
your opponent can exploit. The way out is a mixed strategy: randomize
between Heads and Tails with some probability.

The question is: with *what* probability?

The answer Binmore gives - and this is a genuinely counterintuitive
result the first time you see it - is that you pick your randomization
probabilities to make *your opponent* indifferent between their pure
strategies.

Read that again. You choose your randomization to make your opponent
indifferent, not to maximize your own payoff directly. Your opponent
does the same. The equilibrium is the pair of randomizations where
each player's mix leaves the other player unable to prefer any pure
strategy over any other.

The reason this works is that if your opponent had a strictly
preferred pure strategy against your mix, they would just play that
pure strategy - and then you would want to deviate from your mix to
exploit them. The only stable point is where neither of you can
improve by deviating, which requires both of you to be indifferent.

## Applying It to Shadowrun

Shadowrun is a cyberpunk tabletop RPG where players run "shadowruns" -
illegal jobs for corporate clients. Teams are usually a mix of
specialists: a decker who fights in cyberspace, a street samurai who
solves problems with cybernetically enhanced violence, a mage who
solves problems with spells, and so on.

There is a classic Shadowrun tension between the decker's preferred
approach (subtle, quiet, undetected) and the street samurai's
preferred approach (loud, fast, overwhelming firepower). Both can
succeed if the team commits to one plan and executes it. Neither
works if half the team is trying to be stealthy while the other half
is blowing walls down.

We wrote up a specific scenario:

**The setup.** A teammate, "Glitch," has been kidnapped and is
being held in a Redmond Barrens residential block. The team has two
lead operators: "Zero" the decker (prefers Ghost Op) and "Raze" the
street samurai (prefers Hard Target Extraction). They are in
different parts of the city, prepping their gear, and comms are
spotty - each has to commit to their approach before knowing what
the other has committed to.

**The payoffs** (in "Success Points"):

|  | Raze: Ghost | Raze: Hard Target |
|---|---|---|
| **Zero: Ghost** | Z: 2, R: 1 | Z: 0, R: 0 |
| **Zero: Hard Target** | Z: 0, R: 0 | Z: 1, R: 2 |

Miscoordination is disaster (0, 0) - alarms blare, Glitch gets moved
or killed, the team walks into a meatgrinder. Successful coordination
succeeds, but each operator strictly prefers their own style.

This is the pure Battle of the Sexes structure from Binmore's book,
with the payoffs adjusted for the setting.

## The Math

For Zero to mix, Raze's strategy must make Zero indifferent between
Ghost and Hard Target:

$$
E[U_Z(\text{Ghost})] = q_G \cdot 2 + (1 - q_G) \cdot 0 = 2 q_G
$$

$$
E[U_Z(\text{Hard})] = q_G \cdot 0 + (1 - q_G) \cdot 1 = 1 - q_G
$$

Setting these equal: $2 q_G = 1 - q_G$, so $q_G = 1/3$.

Raze should choose Ghost with probability 1/3 and Hard Target with
probability 2/3.

By symmetric argument, Zero should choose Ghost with probability 2/3
and Hard Target with probability 1/3.

## What This Means at the Table

With those probabilities, the outcomes distribute as:

* Both Ghost: (2/3)(1/3) = 2/9 ≈ 22.2%
* Both Hard Target: (1/3)(2/3) = 2/9 ≈ 22.2%
* Zero Ghost, Raze Hard: (2/3)(2/3) = 4/9 ≈ 44.4%
* Zero Hard, Raze Ghost: (1/3)(1/3) = 1/9 ≈ 11.1%

Total probability of miscoordination: **5/9 ≈ 55.6%**.

Expected payoff for each operator: 2/3 SP.

That is not a good outcome. Both players are worse off in expectation
than they would be under either pure-strategy coordination (which
would give at least 1 SP, and possibly 2). But it is the *equilibrium*
outcome. Given that they cannot communicate and cannot know what the
other has committed to, the mixed strategy is the only strategy pair
where neither player wants to deviate.

At the table, this maps neatly onto the Shadowrun mechanics. If you
have a d6:

* **Zero** rolls: on 5-6, assist Raze and go Hard Target. On 1-4,
  hack it alone with Ghost.
* **Raze** rolls: on 5-6, assist Zero and go Ghost. On 1-4, go in
  guns blazing.

If both rolls "succeed," both plans conflict and the run implodes.
If both rolls "fail," each does their own thing and the run also
implodes. The only good outcomes are the mixed cases where one
assists the other.

## The Deeper Lesson

The reason we like this example is that it makes very concrete a
lesson that Binmore hammers throughout the book:

**Comms are worth more than combat rolls.**

The mixed equilibrium gives each operator 2/3 SP in expectation.
Successful pure coordination would give at least 1 SP, and possibly
2. The gap between 2/3 and 2 is entirely the cost of not being able
to talk to each other before committing.

Every Shadowrun campaign should have a moment where the players
learn this the hard way. If you are a GM, staging a scenario where
comms are down and the team has to commit independently is one of
the most effective ways to teach the value of a comm channel your
players will spend Karma on for the rest of the campaign.

## A Wider Recommendation

The Shadowrun example is a toy application. The real reason to read
Binmore's book is that it gives you the vocabulary to notice
strategic structure in situations that don't look like games -
salary negotiations, whether to attend an optional meeting, whether
to vote in an election where you know your vote won't be decisive.

The Chapter 2 material on the Good Samaritan game - where the
probability of anyone helping decreases as the population increases,
because rational individuals wait for someone else to help - is the
kind of thing that changes how you read the news.

If you are reading one game theory book this year, read this one.
If you are reading one book on Nash equilibrium ever, still read
this one.

## References

* Our wiki notes:
  [Game Theory - A Very Short Introduction](https://charlesreid1.com/wiki/Game_Theory_-_A_Very_Short_Introduction)
* Binmore, K. (2007). *Game Theory: A Very Short Introduction.*
  Oxford University Press.
* Shadowrun: any edition works, but we run 5E.
