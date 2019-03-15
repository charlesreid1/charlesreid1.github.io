Title: An Unsettling Puzzle
Date: 2019-03-13 18:00
Category: Computer Science
Tags: graphs, puzzles, algorithms
Status: draft

## Table of Contents

* [An Unsettling Puzzle](#an-unsettling-puzzle)
* [Tired: The Evil King](#tired-the-evil-king)
* [Solving the Real Problem](#solving-the-real-problem)
* [Wired: Find the Counterfeit](#wired-find-the-counterfeit)
* [Puzzling Conclusions](#puzzling-conclusions)


## An Unsettling Puzzle

Recently I ran across a rather unsettling puzzle question -
one that was worded so distastefully and presented so
thoughtlessly that I wanted to call it out, and show
how easy it would be to come up with a better and more
palatable version of the problem, simply by adapting
_an already-written and well-known problem_.


## Tired: The Evil King

This question comes to us from Goodrich et al's textbook,
"Data Structures and Algorithms in Python":

> An evil king has $n$ bottles of wine, and a spy has just
> poisoned one of them. Unforutnately, they do not know which
> one it is. The poison is very deadly; just one drop diluted
> even a billion to one wil still kill. Even so, it takes
> a full month for the poison to take effect. Design a scheme
> for determining exactly which one of the wine bottles was 
> poisoned in just one month's time while expending $O(\log n)$
> taste testers.

Can we all agree that giving computer science students
problems requiring them to help evil kings create 
clever schemes to carry out unspeakable deeds is probably
_a really stupid idea_?

Textbooks are supposed to be teaching critical thinking.
They're not supposed to be reinforcing the suspension of
ethical misgivings.

You don't see machine learning textbooks introducing
computer vision algorithms by asking students to design
targeting systems for military drones.

Just imagine, for a moment, what a dismal world it
would be if tech companies were filled with 
brilliant problem solvers who were also very 
good at abstracting away worrisome details 
about whose privacy they were violating or whose
personal data they were using without permission.


## Solving the Real Problem

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
$\log_{3}{n}$ (rounded up), since all coins have an identical weight, 
and therefore if two groups are weighed against each other, the heavier
contains the counterfeit. If the weights are the same, the counterfeit 
is in the third group. 


# Puzzling Conclusions

It is already a well-known problem that tech
companies have a basket of ethical issues,
and that many of these issues stem from a
lack of diversity and an overabundance of 
privilege.

Those are hard problems to solve, and they
won't be solved easily. But you know what's
not a hard problem to solve? Figuring out
whether you should actively encourage 
computer science students (who, after 
all, represent the future of tech companies)
to suspend their ethics to as the first step
of their problem-solving procedure.


