Title: 4x4 Rubik's Cube: Part 3: Cycles
Date: 2018-01-17 14:00
Category: Rubiks Cube
Tags: rubiks cube, combinatorics, permutations, python, puzzles, art of computer programming, knuth
Status: draft

*This is Part 3 of a 3-part blog post 
on the mathematics of the 4x4 Rubik's Cube, 
its relation to algorithms, and some 
curious properties of Rubik's Cubes.*

# Table of Contents

* [Introduction: Cycles, Sequences, and Order](#intro)
    * [Cycles](#intro-cycles)
    * [Sequences](#intro-sequences)
    * [Order](#intro-order)

* [Intercalation Product](#intercalation)

* [Factoring Permutations Using Theorem A](#factoring)

* [Factoring Rubik's Cube Permutations](#rubiks)

* [Least Common Multiple and Cycle Order](#lcmorder)

* [Caveats](#caveats)



<a name="intro"></a>
# Introduction

So far we have been discussing representations of the Rubik's Cube,
with the ultimate intention of investigating some of its properties.

In this post, we define and explore the properties we are interested
in studying.

<a name="intro-cycles"></a>
## Cycles

(Definition of cycle)

We use the two-line notation introduced in the last blog post,
so a permutation of a 5-tuple might look like this:

$$
a = \bigl(\begin{smallmatrix}
  a & b & c & d & e \\
  b & a & e & c & d 
\end{smallmatrix}\bigr)
$$

In this permutation, we see that $a$ and $b$ swap places,
and $c$, $d$, and $e$ exchange places as well. These two
groups form two cycles. 

Think of the cycles as the particular way that pieces 
of the permutation are exchanged with one another.

<a name="intro-sequences"></a>
## Sequences

We are interested in studying the properties of the cube,
but in particular we are interested in the properties of 
move sequences applied to the cube.

There are 36 possible moves on a cube, and a series of 
moves applied in a particular order defines a sequence.
The 36 possible rotations were given in the prior blog post
and cover clockwise and counterclockwise rotations of 
each of the six faces - either the first layer, the second layer,
or both of the first two layers.

These moves are denoted with six letters (UDLRFB) for the upper,
downward, left, right, front, and back face of the cube, respectively.

Moves indicated should be clockwise unless they contain an apostrophe
character `'`, which indicates counterclockwise rotation.

A capital letter indicates a rotation of the first layer only 
(e.g., U indicates a clockwise rotation of the first layer of 
the upper face).

A lowercase letter indicates a roration of the first and second layers
(e.g., r indicates a clockwise rotation of the top two layers of
the right face).

A 2 before the letter indicates that the second layer should be rotated
(e.g., 2F indicates a clockwise rotation of the second layer of the 
front face).

Each move sequence can be translated into a tuple representation
(see Part 1 blog post). Once we have the tuple representation of a 
permutation, we can do several things, beginning with finding
the cycles that compose the moves of the sequence.

<a name="intro-order"></a>
## Order

The quantity we are truly interested in is the order of a given cycle.

(What is the order applying a sequence)

We begin with the move sequence, which applies a particular permutation
to the cube, exchanging particular pieces in a particular order.
Once we have the tuple representation of a permutation, we can 
factor it into independent cycles using the techniques covered in 
this blog post. 

The factoring a permutation into cycles will yield the order; 
the order is the least common multiple of the lengths of eacch
cycle that is a factor.

Using this, we can investigate the properties of the order 
of different move sequences.

<a name="intercalation"></a>
# Intercalation Product

(In prior blog post covered tuple representation)

(Two-row notation, more formal introduction)

(Now cover intercalation product, way of combining permutations)

(Intercalation product allows us to start to define permutation algebra)

<a name="factoring"></a>
# Factoring Permutations Using Theorem A

(In this section, discuss and develop a tuple algebra)

## Products of Permutations

(Desirable to perform the reverse of the intercalation product process)

## Factoring Permutations

(Want to factor a given permutation into its intercalation product factors)

## Knuth's Algorithm A

(This is what Knuth's Algorithm A accomplishes)

## Pseudocode 

(Pseudocode for Algorithm A)

## Python Code

(Code for Algorithm A)

<a name="rubiks"></a>
# Factoring Rubik's Cube Permutations

(Example walkthrough for a cube)

<a name="lcmorder"></a>
# Least Common Multiple and Cycle Order

(Explain the logic here)


