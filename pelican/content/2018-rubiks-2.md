Title: 4x4 Rubik's Cube: Part 2: Permutations
Date: 2018-01-14 20:00
Category: Rubiks Cube
Tags: rubiks cube, combinatorics, permutations, python, puzzles, art of computer programming, knuth

*This is Part 2 of a 4-part blog post 
on the mathematics of the 4x4 Rubik's Cube, 
its relation to algorithms, and some 
curious properties of Rubik's Cubes.*

See Part 1 of this blog post here: [Part 1: Representations](https://charlesreid1.github.io/4x4-rubiks-cube-part-1-representations.html)

You are currently reading Part 2 of this blog post: **Part 2: Permutations**

See Part 3 of this blog post here: [Part 3: Factoring Permutations](https://charlesreid1.github.io/4x4-rubiks-cube-part-3-factoring-permutations.html)

See Part 4 of this blog post here: [Part 4: Sequence Order](#)


# Table of Contents

* [Introduction: Sequences and Permutations](#rubiks2-intro)

* [Representing Permutations: Two-Row Notation](#rubiks2-representing)
    * [Two-Row Notation](#rubiks2-representing-tworow)
    * [Two-Row Notation for Rubik's Cube](#rubiks2-representing-tworow-rubiks)

* [Sequences](#rubiks2-sequences)
    * [Review of Move/Sequence Notation](#rubiks2-sequences-review)
    * [How Moves Permute the Cube](#rubiks2-sequences-permute-cube)

* [Rotation Maps](#rubiks2-maps)
    * [U Rotation Map](#rubiks2-maps-u)
    * [D Rotation Map](#rubiks2-maps-d)
    * [L Rotation Map](#rubiks2-maps-l)
    * [R Rotation Map](#rubiks2-maps-r)
    * [F Rotation Map](#rubiks2-maps-f)
    * [B Rotation Map](#rubiks2-maps-b)
    * [How to Use Rotation Map](#rubiks2-maps-rotation)
    * [Face Map Code](#rubiks2-maps-code)

* [Tuples for Move Sequences](#rubiks2-tuples)
    * [Applying Rotation Maps for Sequences](#rubiks2-tuples-sequences)

* [Preview of Part 3](#rubiks2-preview)

* [References](#rubiks2-references)

* [Appendix: Cube with Numbered Faces](#rubiks2-appendix)


<br />
<br />
<br />


<a name="rubiks2-intro"></a>
# Introduction

In this post, we'll be connecting material from Part 1, about 
how to represent the state of the cube in a mathematical way,
to the ultimate goal of exploring properties of particular
move sequences.

In paticular, we'll expand on the tuple notation from Part 1,
and demonstrate the two-row permutation notation of Knuth.
This notation is useful for representing permutations 
in a way that makes it possible to create a system for 
describing permutations using algebra.

We will not discuss the aim of representing permutations
in this way in the present post, but this will be 
described in Part 3.

Next, we discuss move sequences on the Rubik's Cube - 
these are sequences of rotations of particular faces
on the Rubik's Cube. We discuss the application of the 
two-row permutation notation to describe moves
and to describe move sequences.

Finally, we discuss rotation maps, a useful concept
in the implementation of permutations via move sequences.



<a name="rubiks2-representing"></a>
# Representing Permutations: Two-Row Notation

We begin by expanding on and streamlining the tuple notation
introduced in Part 1 of this post so that we have a common
basis for comparing two permutations. We do this using a two-row
notation, where the first row denotes the "solved" or default 
state of the system.

In the case of the Rubik's Cube, this is equivalent to 
starting a cube in the solved state, then describing where
each face ends up, in order to completely specify 
the outcome of a move or a sequence of moves.

<a name="rubiks2-representing-tworow"></a>
## Two-Row Notation

We begin by considering a permutation of an $n$-tuple,
which, in the last post, we resolved to denote 

$$
(2 3 4 \dots n 1)
$$

Now, let us write this as two rows: the first row
consists of each element of the tuple *in ascending 
order*, while the second line will the tuple corresponding
to the order of the elements in this particular permutation:

$$
a = \bigl(\begin{smallmatrix}
  1 & 2 & 3 & \cdots & n-1 & n \\
  2 & 3 & 4 & \cdots &  n  & 1
\end{smallmatrix}\bigr)
$$

We can think of the first row as denoting the "solved", 
default configuration, and the second row denoting how 
each item is permuted.

If we had a different permutation, we would simply change
the second row:

$$
b = \bigl(\begin{smallmatrix}
  1 & 2 & 3 & \cdots & n-1 & n \\
  n & 4 & 1 & \cdots & 2   & 3
\end{smallmatrix}\bigr)
$$

<a name="rubiks2-representing-tworow-rubiks"></a>
## Two-Row Notation for Rubik's Cube

If we adopt the above two-row notation for the Rubik's Cube,
and we utilize the face numbering and tuple indexing from Part 1,
the top row consists of the integers from 1 to 96:

```
(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96)
```

Now suppose we perform a rotation of the upper row U on the cube.
Then we end up with the following tuple:

```
(13 9 5 1 14 10 6 2 15 11 7 3 16 12 8 4 33 34 35 36 21 22 23 24 25 26 27 28 29 30 31 32 49 50 51 52 37 38 39 40 41 42 43 44 45 46 47 48 65 66 67 68 53 54 55 56 57 58 59 60 61 62 63 64 17 18 19 20 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96)
```

This tuple denotes the permutation corresponding to the move U 
performed on a solved cube.



<a name="rubiks2-sequences"></a>
# Sequences

<a name="rubiks2-sequences-review"></a>
## Review of Move/Sequence Notation

Let's quickly recap what we already know from prior posts about the 
properties of move sequences on the Rubik's Cube.

There are 36 possible moves on a cube, and a series of 
moves applied in a particular order defines a sequence.
The 36 possible rotations were given in the prior blog post
and cover clockwise and counterclockwise rotations of 
each of the six faces - either the first layer, the second layer,
or both of the first two layers.

These moves are denoted with six letters (`UDLRFB`) for the upper,
downward, left, right, front, and back face of the cube, respectively.

Moves indicated should be clockwise unless they contain an apostrophe
character `'`, which indicates counterclockwise rotation.

A capital letter indicates a rotation of the first layer only 
(e.g., `U` indicates a clockwise rotation of the first layer of 
the upper face).

A lowercase letter indicates a roration of the first and second layers
(e.g., `r` indicates a clockwise rotation of the top two layers of
the right face).

A 2 before the letter indicates that the second layer should be rotated
(e.g., `2F` indicates a clockwise rotation of the second layer of the 
front face).

<a name="rubiks2-sequences-permute-cube"></a>
## How Moves Permute the Cube

This will be a little easier to understand if we consider 
a particular move sequence. We'll start simple and consider 
the move sequence `U`. This results, as we saw before, in:

```
U:
(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96)
(13 9 5 1 14 10 6 2 15 11 7 3 16 12 8 4 33 34 35 36 21 22 23 24 25 26 27 28 29 30 31 32 49 50 51 52 37 38 39 40 41 42 43 44 45 46 47 48 65 66 67 68 53 54 55 56 57 58 59 60 61 62 63 64 17 18 19 20 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96)
```

Now let's consider the move sequence `U U`, a double rotation of the 
cube's top layer:

```
U U:
(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96)
(16 15 14 13 12 11 10 9 8 7 6 5 4 3 2 1 49 50 51 52 21 22 23 24 25 26 27 28 29 30 31 32 65 66 67 68 37 38 39 40 41 42 43 44 45 46 47 48 17 18 19 20 53 54 55 56 57 58 59 60 61 62 63 64 33 34 35 36 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96)
```

Third, we consider the move sequence `U U U`, equivalent to `U'`,
a counterclockwise rotation of the top layer:

```
U U U:
(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96)
(4 8 12 16 3 7 11 15 2 6 10 14 1 5 9 13 65 66 67 68 21 22 23 24 25 26 27 28 29 30 31 32 17 18 19 20 37 38 39 40 41 42 43 44 45 46 47 48 33 34 35 36 53 54 55 56 57 58 59 60 61 62 63 64 49 50 51 52 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96)
```

The fourth application of `U`, of course, will return the cube back to its 
solved state:

```
U U U:
(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96)
(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96)
```

Now if we examine the relationship between each of these tuples, 
we see that the faces are exchanged according to specific patterns.

These groups of four numbered faces are exchanged with one another:

```
( 4, 16, 13,  1)
( 8, 15,  9,  2)
(12, 14,  5,  3)
( 7, 11, 10,  6)
(65, 49, 33, 17) 
(66, 50, 34, 18)
(67, 51, 35, 19)
(68, 52, 36, 20)
```

There are 8 total faces, composing one upper quadrant of the face
being rotated.

The remaining 64 faces do not move:

```
(21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96)
```


<a name="rubiks2-maps"></a>
# Rotation Maps

While the 96-tuple representation is useful, a better computational
representation of the tuple is a rotation map, which consists of 
2-tuples of face index numbers that are permuted. For example,
the tuple $(4,16)$ would indicate that the position at face 4
would become face 16 after the rotation.

As a reminder, here is the solved cube's face index layout:

```
             01 02 03 04
             05 06 07 08
             09 10 11 12
             13 14 15 16

17 18 19 20  33 34 35 36  49 50 51 52  65 66 67 68
21 22 23 24  37 38 39 40  53 54 55 56  69 70 71 72
25 26 27 28  41 42 43 44  57 58 59 60  73 74 75 76
29 30 31 32  45 46 47 48  61 62 63 64  77 78 79 80

             81 82 83 84
             85 86 87 88
             89 90 91 92
             93 94 95 96
```

Thus, the rotation map representation of each move would be:

<a name="rubiks2-maps-u"></a>
## U Rotation Map

Upon a U rotation, the face 1 will become face 13, indicated by (1,13).

```
U:
---------------------
[(1, 13),
 (2, 9),
 (3, 5),
 (4, 1),
 (5, 14),
 (6, 10),
 (7, 6),
 (8, 2),
 (9, 15),
 (10, 11),
 (11, 7),
 (12, 3),
 (13, 16),
 (14, 12),
 (15, 8),
 (16, 4),
 (17, 33),
 (18, 34),
 (19, 35),
 (20, 36),
 (33, 49),
 (34, 50),
 (35, 51),
 (36, 52),
 (49, 65),
 (50, 66),
 (51, 67),
 (52, 68),
 (65, 17),
 (66, 18),
 (67, 19),
 (68, 20)]
```

<a name="rubiks2-maps-d"></a>
## D Rotation Map

```
D:
----------------------------------------
[(81, 93),
 (82, 89),
 (83, 85),
 (84, 81),
 (85, 94),
 (86, 90),
 (87, 86),
 (88, 82),
 (89, 95),
 (90, 91),
 (91, 87),
 (92, 83),
 (93, 96),
 (94, 92),
 (95, 88),
 (96, 84),
 (29, 77),
 (30, 78),
 (31, 79),
 (32, 80),
 (45, 29),
 (46, 30),
 (47, 31),
 (48, 32),
 (61, 45),
 (62, 46),
 (63, 47),
 (64, 48),
 (77, 61),
 (78, 62),
 (79, 63),
 (80, 64)]
```

<a name="rubiks2-maps-l"></a>
## L Rotation Map

```
L:
----------------------------------------
[(17, 29),
 (18, 25),
 (19, 21),
 (20, 17),
 (21, 30),
 (22, 26),
 (23, 22),
 (24, 18),
 (25, 31),
 (26, 27),
 (27, 23),
 (28, 19),
 (29, 32),
 (30, 28),
 (31, 24),
 (32, 20),
 (1, 80),
 (5, 76),
 (9, 72),
 (13, 68),
 (33, 1),
 (37, 5),
 (41, 9),
 (45, 13),
 (81, 33),
 (85, 37),
 (89, 41),
 (93, 45),
 (68, 93),
 (72, 89),
 (76, 85),
 (80, 81)]
```

<a name="rubiks2-maps-r"></a>
## R Rotation Map

```
 R:
----------------------------------------
[(49, 61),
 (50, 57),
 (51, 53),
 (52, 49),
 (53, 62),
 (54, 58),
 (55, 54),
 (56, 50),
 (57, 63),
 (58, 59),
 (59, 55),
 (60, 51),
 (61, 64),
 (62, 60),
 (63, 56),
 (64, 52),
 (4, 36),
 (8, 40),
 (12, 44),
 (16, 48),
 (36, 84),
 (40, 88),
 (44, 92),
 (48, 96),
 (84, 77),
 (88, 73),
 (92, 69),
 (96, 65),
 (65, 16),
 (69, 12),
 (73, 8),
 (77, 4)]
```

<a name="rubiks2-maps-f"></a>
## F Rotation Map

```
 F:
----------------------------------------
[(33, 45),
 (34, 41),
 (35, 37),
 (36, 33),
 (37, 46),
 (38, 42),
 (39, 38),
 (40, 34),
 (41, 47),
 (42, 43),
 (43, 39),
 (44, 35),
 (45, 48),
 (46, 44),
 (47, 40),
 (48, 36),
 (13, 32),
 (14, 28),
 (15, 24),
 (16, 20),
 (20, 81),
 (24, 82),
 (28, 83),
 (32, 84),
 (81, 61),
 (82, 57),
 (83, 53),
 (84, 49),
 (49, 13),
 (53, 14),
 (57, 15),
 (61, 16)]
```

<a name="rubiks2-maps-b"></a>
## B Rotation Map

```
 B:
----------------------------------------
[(65, 77),
 (66, 73),
 (67, 69),
 (68, 65),
 (69, 78),
 (70, 74),
 (71, 70),
 (72, 66),
 (73, 79),
 (74, 75),
 (75, 71),
 (76, 67),
 (77, 80),
 (78, 76),
 (79, 72),
 (80, 68),
 (1, 52),
 (2, 56),
 (3, 60),
 (4, 64),
 (17, 4),
 (21, 3),
 (25, 2),
 (29, 1),
 (93, 17),
 (94, 21),
 (95, 25),
 (96, 29),
 (52, 96),
 (56, 95),
 (60, 94),
 (64, 93)]
```

<a name="rubiks2-maps-rotation"></a>
## How To Use Rotation Map

The rotation map enables us to represent a 4x4 Rubik's Cube
as a simple tuple, and just use a Rubik's Cube object from the 
[forked rubikscubesolver library](https://git.charlesreid1.com/charlesreid1/rubiks-cube-nnn-solver)
at git.charlesreid1.com to get the rotation maps.

```python
# Python code:
cube0 = list(range(1,96+1))
cube1 = cube0.copy()
cube_prior = cube0.copy()
r = get_cube()

for c,move in enumerate(rot.split(" ")):

    # Get the rotation map
    rotmap = r.rotation_map(move)

    # (Print the rotation map here)

    # Apply each transformation in the rotation map to the new cube
    for m in rotmap:
        # shift item at index m[0] to item at index m[1]
        cube1[cube_prior.index(m[0])] = m[1]

    cube_prior = cube1.copy()
```

<a name="rubiks2-maps-code"></a>
## Face Map Code

In this section we present a portion of the code 
that actually generates these face maps. This functionality
was not in the [original Rubik's Cube solver library](https://github.com/dwalton76/rubiks-cube-NxNxN-solver)
from [Github user @dwalton76](https://github.com/dwalton76/),
so the library was forked and the functionality added
to the [forked Rubik's Cube solver library](https://git.charlesreid1.com/charlesreid1/rubiks-cube-nnn-solver).

The actual implementation is in the `rotation_map(action)` method,
defined for the Rubik's Cube object at the same place as the 
`rotate(action)` method. This definition is in 
`rubikscubennnsolver/__init__.py` on line 581:

[link to `rubikscubennnsolver/__init__.py`](https://git.charlesreid1.com/charlesreid1/rubiks-cube-nnn-solver/src/master/rubikscubennnsolver/__init__.py#L581)

This method returns a list containing the tuples of index permutations 
(old,new) that correspond to this particular move. Call it like this:

```python
order = 'URFDLB'
cube = RubiksCube444(solved_4x4x4, order)
cube.rotation_map('U')
```



<a name="rubiks2-tuples"></a>
# Tuples for Move Sequences

So far we have shown the tuple representation for the Rubik's Cube
and how it works, and created a more convenient representation for
implementing the cube on a computer and applying rotations.

Now, we can achieve the goal of this post, which is to be able to
represent the state of a cube, after a certain number of rotations,
in a quantitative and mathematical way.

In Part 3, we'll develop an algebra of permutations to use 
and understand the tuple representations we are presenting in 
this post.

<a name="rubiks2-tuples-sequences"></a>
## Applying Rotation Maps for Sequences

The concept here is simple: we use the rotation maps that we defined
above to permute elements according to the formula prescribed for 
that particular rotation.

By applying these permutations sequentially, we can permute the 
96-tuple in a way that represents the permutations created by 
a given sequence of moves.

For example, after applying four sequence maps corresponding to 
the move sequence `U R U' R'` we get:

```
(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96)
(1 2 3 77 5 6 7 73 9 10 11 69 16 12 8 20 17 18 19 36 21 22 23 24 25 26 27 28 29 30 31 32 49 50 51 33 37 38 39 40 41 42 43 44 45 46 47 48 13 56 60 64 53 54 55 34 57 58 59 35 61 62 63 4 96 66 67 68 14 70 71 72 15 74 75 76 65 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 52)
```

<a name="rubiks2-preview"></a>
# Preview of Part 3

As a preview of where we are going with Part 3, let's 
return to the permutation corresponding to `U R U' R'`:

```
(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96)
(1 2 3 77 5 6 7 73 9 10 11 69 16 12 8 20 17 18 19 36 21 22 23 24 25 26 27 28 29 30 31 32 49 50 51 33 37 38 39 40 41 42 43 44 45 46 47 48 13 56 60 64 53 54 55 34 57 58 59 35 61 62 63 4 96 66 67 68 14 70 71 72 15 74 75 76 65 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 52)
```

It turns out that, unlike the `U` move by itself, this move sequence 
results in groups of either three or six faces exchanging places.
(In Part 3 we will cover the algorithm for finding these groups,
which, crucially, relies on the work we did in this post.)

The groups of six faces that are permuted are:

```
[77, 65, 96, 52, 64, 4]
[16, 20, 36, 33, 49, 13]
```

These two sets of six faces all live on corners of the cube, 
so this move sequence swaps six corners.

Likewise, the groups of three faces that are permuted are:

```
[73, 15, 8]
[69, 14, 12]
[50, 56, 34]
[51, 60, 35]
```

These are all faces on double edge pieces: 

* `[73, 15, 8]` and `[51, 60, 35]` are faces on right-handed double edge pieces
* `[69, 14, 12]` and `[50, 56, 34]` are faces on left-handed double edge pieces

The remaining faces do not permute:

```
[1, 2, 3, 5, 6, 7, 9, 10, 11, 17, 18, 19, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 53, 54, 55, 57, 58, 59, 61, 62, 63, 66, 67, 68, 70, 71, 72, 74, 75, 76, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95]
```

What we will discover is that the least common multiple 
of these two numbers, 6 and 3, yields the number of times
this move sequence needs to be applied to a solved cube (6) 
in order to return the cube back to its solved state.



<a name="rubiks2-references"></a>
# References

1. "Rubik's Cube". Charlesreid1.com wiki, Charles Reid. Edited 14 January 2017. Accessed 14 January 2017.
<[https://charlesreid1.com/wiki/Rubiks_Cube](https://charlesreid1.com/wiki/Rubiks_Cube)>

2. "Rubik's Revenge". Charlesreid1.com wiki, Charles Reid. Edited 14 January 2017. Accessed 14 January 2017.
<[https://charlesreid1.com/wiki/Rubiks_Revenge](https://charlesreid1.com/wiki/Rubiks_Revenge)>

3. "Rubik's Cube/Tuple". Charlesreid1.com wiki, Charles Reid. Edited 14 January 2017. Accessed 14 January 2017.
<[https://charlesreid1.com/wiki/Rubiks_Cube/Tuple](https://charlesreid1.com/wiki/Rubiks_Cube/Tuple)>

4. "Rubik's Cube/Permutations". Charlesreid1.com wiki, Charles Reid. Edited 14 January 2017. Accessed 14 January 2017.
<[https://charlesreid1.com/wiki/Rubiks_Cube/Permutations](https://charlesreid1.com/wiki/Rubiks_Cube/Permutations)>

5. "Github - dwalton76/rubiks-cube-NxNxN-solver". dwalton76, Github Repository, Github Inc. Accessed 11 January 2017.
<[https://github.com/dwalton76/rubiks-cube-NxNxN-solver](https://github.com/dwalton76/rubiks-cube-NxNxN-solver)>

6. "Rubik's Cube NxNxN Solver". Git repository, git.charlesreid1.com. Charles Reid. Updated 14 January 2017.
<[https://git.charlesreid1.com/charlesreid1/rubiks-cube-nnn-solver](https://git.charlesreid1.com/charlesreid1/rubiks-cube-nnn-solver)>

7. "Rubiks Cube Cycles". Git repository, git.charlesreid1.com. Charles Reid. Updated 14 January 2017.
<[https://git.charlesreid1.com/charlesreid1/rubiks-cube-cycles](https://git.charlesreid1.com/charlesreid1/rubiks-cube-cycles)>





<a name="rubiks2-appendix"></a>
# Appendix: Cube with Numbered Faces

```
             01 02 03 04
             05 06 07 08
             09 10 11 12
             13 14 15 16

17 18 19 20  33 34 35 36  49 50 51 52  65 66 67 68
21 22 23 24  37 38 39 40  53 54 55 56  69 70 71 72
25 26 27 28  41 42 43 44  57 58 59 60  73 74 75 76
29 30 31 32  45 46 47 48  61 62 63 64  77 78 79 80

             81 82 83 84
             85 86 87 88
             89 90 91 92
             93 94 95 96
```



