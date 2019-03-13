Title: Some Unsettling Puzzles
Date: 2019-03-13 18:00
Category: Computer Science
Tags: graphs, puzzles, knuth, algorithms
Status: draft

# Table of Contents

* [The First Unsettling Puzzle](#the-first-unsettling-puzzle)
  * [Tired: The Evil King](#tired-the-evil-king)
  * [Wired: Find the Counterfeit](#wired-find-the-counterfeit)
* [The Second Unsettling Puzzle](#the-second-unsettling-puzzle)
  * [Tired: The Josephus Problem](#tired-the-josephus-problem)
  * [Wired: Girls Playing Ball](#wired-girls-playing-ball)
* [Puzzling Conclusions](#puzzling-conclusions)

Recently I ran across two rather unsettling puzzles that were
worded so poorly, and were so distasteful in their presentation,
that I wanted to call them out as needing to be cast aside
and replaced with better and more palatable versions - 
which are _readily available_ in the form of _existing problems_.

# The First Unsettling Puzzle

## Tired: The Evil King

This question comes to us from Goodrich et al, "Data Structures and Algorithms in Python":

> An evil king has $n$ bottles of wine, and a spy has just
> poisoned one of them. Unforutnately, they do not know which
> one it is. The poison is very deadly; just one drop diluted
> even a billion to one wil still kill. Even so, it takes
> a full month for the poison to take effect. Design a scheme
> for determining exactly which one of the wine bottles was 
> poisoned in just one month's time while expending $O(\log n)$
> taste testers.

Can we all agree, that if the premise of an end-of-the-chapter
exercise involves actively helping an evil king save $n-1$ 
bottles of wine by murdering $n$ innocent people, that textbook
_may have an ethics issue_?

Actively teaching students to abstract away distasteful actions into
mathematical problems is a terrible idea. You wouldn't introduce students
to machine learning algorithms by having them write software for
a drone with a machine gun to recognize and target humans. That would
be a stupid skill to teach. 

Why, just imagine, for a moment, if you can, how dire the situation would
be, if tech companies were filled with brilliant problem 
solvers who were also very good at abstracting away worrisome 
details about the personal data they were operating on, the privacy
they were violating, or the end uses of their systems.


### Solving the Real Problem

Let's all agree that the real problem here is the king, so the optimal
way of solving this problem is to expend exactly $1$ taste tester
(the king) by having him drink one glass of wine formed from a drop
of all $n$ bottles.

The less optimal and rather greusome solution involves creating a binary tree
where each leaf node is a glass of wine, and each parent node combines the two 
wines below it. A slightly less optimal solution than "expending" $1$ taste 
tester (above) is to carry out this plan, but seat the king at the root of the 
tree, which accomplishes the same thing as the $O(1)$ deaths solution (above).


## Wired: Find the Counterfeit

A better verison of this problem usually follows a template like this:

> You are given $n$ coins, of which $n-1$ coins are gold and $1$ coin is
> counterfeit lead (heavier). You also have a fair scale.  Determine, with only
> $w$ weighings using the scale, which coin is the counterfeit.

The reason this problem is better (besides no deaths) is that $w$
is an integer that is smaller than $\log_{2}{n}$, which is where you
have to be creative and think beyond the binary tree. (It is in fact
$\log_{3}{n}$, since all coins have an identical weight, and therefore
if two groups are weighed against each other, the heavier contains the
counterfeit. If the weights are the same, the counterfeit is in the
third group. 


# The Second Unsettling Puzzle

## Tired: The Josephus Problem

The second of our twounsettling puzzles has the excuse of being
both 40 years old (it truly was a different time in computer science)
and being rooted in a historically greusome puzzle about mass execution.

Let's jump in!

This problem comes to us from Donald Knuth's <u>The Art of Computer Programming</u>
(TAOCP) Volume 1, which covers some basic (ha ha, not really) mathematics
and introduces some fundamental algorithms and data structures.

In Section 1.3.2 (which introduces the MIX assembly language,
then presents a set of exercises that are essentially recreational
puzzles that are well-suited to being solved with a computer),
Knuth poses the following problem (Exercise 22, rated a "31" on
Knuth's 0-to-50 scale):

> (The Josephus Problem.) There are $n$ men arranged in a circle. Begining at a
> particular position, we count around the circle and brutally execute every
> $m^{th}$ man (the circle closing as men are decapitated). For example, the
> execution ordr when $n=8, m=4$ is $54613872$: the first man is fifth to go,
> the second man is fourth, etc.
>
> Write a complete MIX program which prints out the order of execution when
> $n=24, m=11$. Try to design a clever algorithm which works at high speed when
> $n$ and $m$ are large (it may save your life).


### Solving the Real Problem

Note that we're not going to go through the solution to this Josephus problem
here - that will come in a later blog post. Plus there are a number of exercises
in TAOCP that build on the solution to the above problem, so we will cover those
as well.


## Wired: Girls Playing Ball

Boris Kordemsky, a famous Russian puzzle master (think of him as a Russian
equivalent of Martin Gardner), posed the following puzzle, which is included
in <u>The Moscow Puzzles</u> (published by Dover), called "Girls Playing Ball"
(Puzzle 23). 

While different from the Josephus problem, it's a more tasteful
version of a related problem:

> **Twelve girls** in a circle began to toss a ball, each girl to her neighbor on the left.
> When the ball had completed the circle, it was tossed in the opposite direction.
> 
> After a while one of the girls said: "Let's skip 1 girl as we toss the ball."
> 
> "But since there are 12 of us, half the girls will not be playing," Natasha objected.
> 
> "Well, let's skip 2 girls!"
>
> "This would be even worse - only 4 would be playing. We should skip 4 girls -
> the fifth would catch it. There is no other combination."
> 
> "And if we skip 6?"
> 
> "It is the same as skipping 4, only the ball goes in the opposite direction,"
> Natasha answered.
>
> "And if we skip 10 girls each time, so that the eleventh girl catches it?"
>
> "But we have already played that way," said Natasha.
>
> They began to draw diagrams of every such way to toss the ball, and were
> soon convinced that Nattasha was right. Besides skipping none, only skipping
> 4 (or its mirror image 6) let all the girls participate.
> 
> If there had been 13 girls, the ball could have been tossed skipping 1 girl,
> or 2 girls, or 3 girls, or 4 girls, without leaving any girls out. How 
> about 5 and 6?

The thing I like about this presentation of the problem, besides the fact that it
is free of death and decapitation, is that it explains the problem, giving 
multiple examples in the form of the conversation that takes place. This
gives the reader a jump start in their thinking about the problem.

This problem is different from (simpler than?) the Josephus problem, 
and deals with small values of $m$ and $n$, but I like the spirit 
of the question and its presentation, and it could be easily adapted.


## Wired: Sushi Boats

An alternative presentation of the problem:

> You are the only customer at a sushi restaurant
> with $n$ small boats carrying trays of sushi
> going past you.
> 
> To occupy yourself while you eat, you devise
> the following scheme: beginning with a particular
> boat, you consume the sushi on that boat.
> You then count $m$ boats carrying sushi,
> eating the sushi that the $m^{th}$ boat is
> carrying. (Empty boats don't count.)J
> 
> For example, if there are $n = 8$ sushi boats and
> you eat from every $4^{th}$ boat with sushi,
> the order in which each boat is consumed is
> given by $54613872$: the first sushi boat
> is consumed first, the second sushi boat
> is consumed fourth, and so on.
> 
> Write a program to print out the order in which
> sushi boats are consumed for $n = 24$ and $m = 11$.
> Try to design a clever algorithm to work at
> high speed when $n, m$ are large (and use it to
> figure out which boat will be eaten last).


# Puzzling Conclusions

When writing puzzles or exercises, don't resort to the appeal of violence
and murder to get readers interested in your problem. The mathematics is
the point. Problems should age well, so leave out the politics,
sexism, racism, and any other isms. And above all - stop teaching people 
to suspend their ethics as the first step in problem-solving.


