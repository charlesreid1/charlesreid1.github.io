Title: 4x4 Rubik's Cube: Part 1: Representation
Date: 2018-01-11 10:00
Category: Rubiks Cube
Tags: rubiks cube, combinatorics, permutations, python, puzzles, art of computer programming, knuth
Status: draft

# Introduction: Why The Rubik's Cube

* Rubiks' Cube interesting mathematical system
* Exhibits symmetry found in real systems
* Applied combinatorics, group theory
* Algorithms

## Why The 4x4 Rubik's Cube

The 4x4 Rubik's cube, also known as the Rubik's Revenge cube, 
is larger than the standard 3x3 Rubik's Cube. The 4x4 cube 
exhibits some particularly interesting properties as a result
of having an even number of squares on each edge. 

I'm also interested in the 4x4 because I enjoy solving it!
I can solve the cube in 4 to 4.5 minutes.

# How the Rubik's Cube Works

Let's start with a discussion of cube mechanics, since this 
is important to coming up with an accurate mathematical model
of the cube.

## The Pieces

The 4x4 Rubik's Cube consists of six faces of sixteen squares 
each, for a total of 96 face squares. These face squares are 
not completely interchangeable, however - the 4x4 cube is actually
composed of three types of pieces, called "cubies".

The first type of piece is a **corner piece**, which contains 
3 faces. Note that it is impossible for the corner pieces
to change their chirality (direction of rotation).
There are 8 corner pieces, each of which can be oriented
in 3 different ways. 

The second type of piece is a **double edge (dedge) piece**.
Each edge is composed of two double edges. There are 
24 total double edge pieces, which can be further classified
into 12 left-handed and 12 right-handed dedge pieces.

Lastly, there are 4 **center pieces** in the center of each
face, for a total of 24 center pieces. Note that each of the 
center pieces of a givne color are interchangeable, unlike 
the double edge pieces or corners.

## Face Notation

To refer to particular faces on the cube, we use six
letters to indicate different faces:

U - upper face (the top of the cube)

D - downward face (the bottom of the cube0

F - front face (the front of the cube)

B - back face (the back side of the cube)

L - left face of the cube (on the left side when facing the front F face)

R - right face of the cube

This will help refer to how we will roate the cube.

## Color Notation

In the solved state, each cube face has one of six colors.
The orientation of these colors relative to one another
is always fixed; the red and orange colored faces, for example,
are never adjacent. This is due to the nature of the mechanical
pieces that compose the Rubik's Cube.

The standard orientation of colors to refer to the soled cube
is as follows:

* U = White
* D = Yellow
* F = Green
* B = Blue (Back-Blue)
* L = Orange
* R = Red (Red-Right)

Note that on a 3x3 cube, we can always determine the
final color a face will have, because the six center pieces
on each side of a 3x3 cube always remain fixed.

On a 4x4 cube, however, all four center squares can rotate 
and move, meaning all 24 center squares are totally 
interchangeable, and there is no link between the 
center colors on a 4x4 cube and the final color
that will be on that face when the cube is solved.

## Move Notation

using the face notation explained above, we can denote 
multiple types of moves on the Rubik's Cube.

We have 36 total moves that we can make on the Rubik's Cube,
easy to remember using the following groups of 12:

```
L l r R
U u d D
B b f F

L' l' r' R'
U' u' d' D'
B' b' f' F'

2L 2L' 2R 2R'
2U 2U' 2D 2D'
2B 2B' 2F 2F'
```

Let's go through those a little more slowly.

### Regular Face Rotations

The regular face turns are denoted with capital letters:
L R U D B F refer to a single clockwise rotation of the 
respective face. Here, "clockwise" means *the direction
that is clockwise when facing the given face head-on.*

### Reverse Rotations

The `'` apostrophe following moves indicates that 
the move shoud be a *counter-clockwise* rotation 
of the given face, instead of clockwise.

### Double Face Rotations

Rotations that are indicated using a lowercase letter
refer to two-layer rotations. That is, the lowercase 
`u` refers to the *clockwise* rotation of the top 
two layers of the cube; the lowercase `r` refers
to the *clockwise* rotation of the rightmost two
layers of the cube; and so on.

We have covered the first 24 moves - 
clockwise and counter-clockwise rotations
of single and double layers.

### Second Layer Face Rotations

The `2` notation indicates a rotation of the second layer only. 
For example, `2U` refers to the clockwise rotation of the second 
layer from the top. This is equivalent to the move sequence 
`u U'`.

# Computer Representation of a Rubik's Cube

* Open-source NxNxN Rubik's Cube solver library.
* Modifications necessary.
* Here's how you make a cube.

Operations and functionality
* Here are the important operations and functionality.

Numbering of faces
* Here is the numerical representation of the faces.

What tuple representation will look like
* Why can't just label faces/colors
* Not a multiset problem WWWWBBBBRRRR etc
* Numerical labeling of each face

Tuple representation:
* 96 integers
* Caveat: 4 are interchangeable.
* Two approaches: one more complicated, one less complicated.
* More complicated: duplicates in 96-tuple
* Less complicated: 96 separate faces, but build in accounting for fact that four faces are interchangeable

Next post:
* Rotation index shifts






















