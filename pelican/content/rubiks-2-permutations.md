Title: 4x4 Rubik's Cube: Part 2: Permutations
Date: 2018-01-14 14:00
Category: Rubiks Cube
Tags: rubiks cube, combinatorics, permutations, python, puzzles, art of computer programming, knuth
Status: draft

*This is Part 2 of a 3-part blog post 
on the mathematics of the 4x4 Rubik's Cube, 
its relation to algorithms, and some 
curious properties of Rubik's Cubes.*

# Table of Contents

* [Introduction: Sequences and Permutations](#intro)

* [Representing Permutations: Two-Row Notation](#representing)

* [Sequences](#sequences)

* [Rotation Maps](#maps)



<a name="representing"></a>
# Representing Permutations: Two-Row Notation

(Write state of cube at beginning, then state of cube at end)

(Introduce two row notation)

(This is how we will denote a particular permutation)



<a name="sequences"></a>
# Sequences

Let's quickly recap what we already know from prior posts about the 
properties of move sequences on the Rubik's Cube.

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



<a name="maps"></a>
# Rotation Maps

Alternative way of representing a permutation,
list of 2-tuples that indicate which face index
goes to which new face index.

Rotation maps provide utility in actually dealing with
the cube representations and in applying rotation moves
to the cube.

