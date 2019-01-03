Title: Mad Combinatoric Castles
Date: 2017-07-25 18:00
Category: Mathematics
Tags: computer science, mathematics, factors, sequences, project euler

# Table of Contents

* [Overview: The Problem](#castles-problem)
* [Polyominoes](#polyominoes)
    * [Castle Rules for Polynominoes](#castle-rules)
* [
* Problem 502 Solution Approaches


<a name="castles-problem"></a>
# Overview: The Problem

In an earlier post, I mentioned [my efforts on Project Euler problems](https://charlesreid1.com/wiki/Project_Euler)
and the wide variety of problems there that can offer some profound mathematical insights.

Given that the first post covered Project Euler problem 1, I thought it would be nice
if the next problem cranked up the difficulty factor by an order of magnitude.
[Project Euler Problem 502](https://projecteuler.net/problem=502) is a very hairy combinatorics problem that required me to learn about 
a wide variety of combinatorial enumeration techniques.

Let's start with the problem statement.

## Building Castles

Problem 502 is about building castles. The problem gives an $M \times N$ rectangular grid,
and asks us to count how many "castles" can be built on the rectangular grid, given its maximum
height. 

Here is how the game works:

First, start by defining a block as a rectangle of height 1, and an integer-valued length.
A castle is a configuation of stacked blocks.

For a game grid of size $M \times N$, we can construct castles according to
the following rules:

* Blocks can be placed on top of other blocks, but no sticking out past edge
* All blocks aligned to grid
* Two neighboring blocks must have 1 unit of space between them
* Maximum achieved height of castle is EXACTLY M
* Castle is made from even number of blocks

Here is an example W = 8, H = 5 castle given in more compact notation:

```
  #   # 
  #   ##
 ## # ##
##### ##
########
```

We can also build more complicated castles, like this 10 by 100 castle:

```
X       X      XX    X     XX   XX X X                          X XX          XX   XX  X     X   XXX
X       X      XX    X     XX X XX X X     X     X             XX XX          XX   XX  X     X   XXX
X      XX      XX    X     XX X XXXX X     X     X             XX XX          XX   XX  X     X   XXX
X      XX      XX    X     XX X XXXX X     X     X XXX         XX XX          XX X XX  X     X   XXX
X      XX     XXX    X     XX X XXXX X  X  X     X XXX X X     XX XX          XX X XX  X  X  X   XXX
X      XX  X  XXX  X X     XXXX XXXX X  XX X    XX XXX X X   X XX XX          XX XXXX  X XX XX  XXXX
X  XX  XX  X  XXX  X X     XXXX XXXX XX XX XX XXXX XXX X XXX X XX XX    X     XX XXXXX X XX XX XXXXX
X  XX  XXX X  XXX  X X   X XXXX XXXX XX XX XX XXXX XXXXX XXX XXXX XX  X X     XX XXXXX X XX XXXXXXXX
X XXXXXXXX X XXXXXXX X XXXXXXXX XXXXXXX XX XX XXXXXXXXXXXXXX XXXX XX XX X  XX XX XXXXXXXXXX XXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

Our objective in this problem is to enumerate all possible castles. Let $F(x,y)$ denote the number of 
unique castles with a width of x and a height of exactly y. The problem gives use the trivial number
$F(4,2) = 10$. The problem also gives $F(13,10)$ and $F(10,13)$, both of which are absolutely enormous numbers.

This should be your first giant red flag that manual enumeration through a traversal of combinatoric space 
is absolutely, positively out of the question. We'll explain why in more detail below, but suffice to say,
there is a combinatoric explosion that occurs for castles larger than 10, so castles with a width of 
1 trillion are going to get STUPID big.

Then we're given $F(100,100)$, which is so enormous it has to be reported mod 1,000,000,007.

Finally, the problem asks us the following whopper of a question:

What is $F(10^{12},100) + F(10^4, 10^4) + F(100,10^{12}) mod 1,000,000,007$? 

Whew.

## The Scale of the Problem

For solving this problem it is important to take a step back and think through
the size of the combinatoric space being searched, and what methods we have for 
carving out that space.

As already mentioned, the size of this problem - the actual number of 
castles - is surely larger than the [Eddington numer](https://charlesreid1.com/wiki/Eddington_Number),
the number of protons in the known universe. The numbers of combinations are 
STUPID big. There's no way for the mind to fully wrap itself around the concept.

The huge numbers involved means, we must have a closed-form expression for $F(x,y)$ that we can
evaluate once to get each of the $F(10^{12},100), F(10^4,10^4), F(100,10^{12})$ required by the answer.
Doing so much as counting to 1 trillion takes minutes on modern computers, so if you're doing anything else
1 trillion times, you'll end up waiting a loooong time.

## Generating Functions

As it turns out, there is indeed a combinatorial enumeration method that does
not require explicitly finding or generating each permutation in order to count
all permutations.  I have covered [generating
functions](https://charlesreid1.com/wiki/Generating_Functions) on the
charlesreid1.com wiki.  The principal idea behind generating functions is the
observation that we can rearrange the infinite series:

$$
G(z) = 1 + z + z^2 + z^3 + \dots
$$

into the equation 

$$
G(z) = \dfrac{1}{1-z}
$$

This single identity leads to a whole family of solution techniques for generating functions.
The basic idea is to start by writing the rules of your system (see above), 
then write a generating function that varies with characteristic variables of the problem 
(width and height in this case, possibly others),
and last, combine the generating functions of different rules or objects into a single generating function.

<a name="polyominoes"></a>
# Overview of Polyominoes

Let us begin by considering a two-dimensional grid $\pi$ of points at positive integer coordinates,
$\pi = \mathbb{N} \times \mathbb{N}$. 

Let a polyomino denote a two-dimensional shape formed by connecting contiguous unit square tiles
together, all of which align to the 2D grid of integers $\pi$. 

(Granted, this definition sounds a bit pedantic, as we're just describing stackable squares,
but we need to keep the definition general because there are many kinds of polyomonioes,
and many rules that we can set for how we arrange them.)

If you have played [Tetris](https://en.wikipedia.org/wiki/Tetris) before, or 
John Conway's [Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life), you will recognize
polyominoes from those contexts.

Now, we set up our generating function in terms of characteristics of the problem.

It is very important to note that, while most of the rules are fairly straightforward to translate into
a polyomonio type of framework, Rule 6 is not. In fact, it is probably Rule 6 that makes Problem 502
so challenging. Were it not for Rule 6, this would be a nearly-trivial problem.

Let's review our castle construction rules and translate them into polyomino equivalents.

<a name="castle-rules"></a>
## Castle Rules for Polyominoes

### Generating Function Variables

We want to construct a multivariate ordinary generating function for our castles, since we have 
several variables we want to change, and get back a total count of castles.

The two most obvious variable choices for our generating function independent variables 
are width $x$ and height $y$. Surely, these must be in the final generating function.

However, this still doesn't give us enough information about the construction process 
from step to step. Imagine that we place the first block on row 1.

Then we may place as many blocks as we would like along row 2, wherever we would like 
(level 2 is the least restricted layer of the castle).

Now, when we get to row 3, we are only allowed to keep building where there is already 
an existing tower from the prior row. This means, we have to pass along information 
from the prior row - where the bricks are located and how many - so that we know where
the next level may build towers.

This will remain an open question until we cover a few other representations of 
Problem 502 and ways of modeling it. Then we will cover what additional
variables our generating function might need.

### Rule 1: No Overhangs

Rule 1 stipulates that blocks can be placed on top of
other blocks as long as nothing sticks out past the end
or hags out.

This ensures that the resulting polyomino is column
convex. Column convexity is the property that we can
draw a vertical line through any column of the
polyomino, and we only intersect the polyomino in two
places. (No internal breaks.)

This rule stipulates what kind of polyomino
constructions are allowed.

### Rule 2: Snap to Grid

This rule is just saying that the unit squares in the
castle problem match the unit squares of polyominoes,
ensuring the problems are interchangeable.

### Rule 3: Neighbor Blocks Need Space

Rule 3 is crucial for being able to count blocks. If two
side-by-side contiguous unit squares could be either one
or two blocks, this would make the final count of
solutions much, much, much, much, much bigger than it
should be.

### Rule 4: Bottom Row is One Block

This is more of an accounting-based rule, but we define
our castle construction process such that it begins with
a completed row. This means that the number of blocks
that we add on top of that single block must be odd
overall.

### Rule 5: Maximum Height is Exactly H

As it turns out, the last two rules are the toughest -
in a sense, because they are **global** conditions on
the combinatoric solution that is being counted.  In
other words, we will use generating functions to
"construct" our combinatoric objects in a methodical
way, and the challenge is on setting global conditions
on the generating function's counted solutions.

### Rule 6: Even Number of Blocks

Rule 6 is definitely what makes this problem difficult. 

Our approach is going to involve coming up with a 
counting function - but this rule tells us that the
counting function will need to have some way of
accounting for the total number of blocks, and
divide by or subtract a factor that accounts for
castles with an odd number of blocks.

<a name="castles-problem"></a>
## Don't Generate - Enumerate!

We mentioned above that the number of possibilities
here is huge, so this combinatorics problem falls 
squarely in the realm of enumerating, not generating.

That being said, and keeping in mind that the problem
size blows up rapidly, it can still be useful to write
an algorithm to generate castles for small values of
width and height, to test formulas for these small
values (and uncover corner cases!).

See [Project Euler/502](https://charlesreid1.com/wiki/Project_Euler/502)
on the charlesreid1.com wiki for continued work on
this problem. 
