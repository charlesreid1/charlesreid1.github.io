Title: 4x4 Rubik's Cube: Part 1: Representation
Date: 2018-01-11 10:00
Category: Rubiks Cube
Tags: rubiks cube, combinatorics, permutations, python, puzzles, art of computer programming, knuth

# Table of Contents

* [Introduction: Why the Rubik's Cube](#intro)
    * [Why the 4x4 Rubik's Cube](#intro-why)

* [How the Rubik's Cube Works](#how)
    * [The Pieces](#how-pieces)
    * [Face Notation](#how-face)
    * [Color Notation](#how-color)
    * [Move Notation](#how-move)
        * [Regular Face Rotations](#how-move-regular)
        * [Reverse Face Rotations](#how-move-reverse)
        * [Double Face Rotations](#how-move-double)
        * [Second Layer Face Rotations](#how-move-second)

* [Computer Representation of a Rubik's Cube](#computer)
    * [Operations an Functionality](#computer-operations)
    * [Face Numbering](#computer-face)

* [Tuple](#tuple)
    * [Tuple Representation Requirements](#tuple-requirements)
    * [Tuple Representation](#tuple-representation)

* [Preview of Part 2](#preview-part-2)



<a name="intro"></a>
# Introduction: Why The Rubik's Cube

* Rubiks' Cube interesting mathematical system
* Exhibits symmetry found in real systems
* Applied combinatorics, group theory
* Algorithms

<a name="intro-why"></a>
## Why The 4x4 Rubik's Cube

The 4x4 Rubik's cube, also known as the Rubik's Revenge cube, 
is larger than the standard 3x3 Rubik's Cube. The 4x4 cube 
exhibits some particularly interesting properties as a result
of having an even number of squares on each edge. 

I'm also interested in the 4x4 because I enjoy solving it!
I can solve the cube in 4 to 4.5 minutes.

<a name="how"></a>
# How the Rubik's Cube Works

Let's start with a discussion of cube mechanics, since this 
is important to coming up with an accurate mathematical model
of the cube.

<a name="how-pieces"></a>
## The Pieces

The 4x4 Rubik's Cube consists of six faces of sixteen squares 
each, for a total of 96 face squares. These face squares are 
not completely interchangeable, however - the 4x4 cube is actually
composed of three types of pieces, called "cubies".

<img src="images/cube1.jpg" width="300"/>
**Figure 1: Corner pieces are green.**

The first type of piece is a **corner piece**, which contains 
3 faces. Note that it is impossible for the corner pieces
to change their chirality (direction of rotation).
There are 8 corner pieces, each of which can be oriented
in 3 different ways. 

<img src="images/cube2.jpg" width="300"/>
**Figure 2: Double edge pieces are blue.**

The second type of piece is a **double edge (dedge) piece**.
Each edge is composed of two double edges. There are 
24 total double edge pieces, which can be further classified
into 12 left-handed and 12 right-handed dedge pieces.

<img src="images/cube3.jpg" width="300"/>
**Figure 3: Center pieces are blue.**

Lastly, there are 4 **center pieces** in the center of each
face, for a total of 24 center pieces. Note that each of the 
center pieces of a givne color are interchangeable, unlike 
the double edge pieces or corners.

<a name="how-face"></a>
## Face Notation

To refer to particular faces on the cube, we use six
letters to indicate different faces:

`U` - upper face (the top of the cube)

`D` - downward face (the bottom of the cube0

`F` - front face (the front of the cube)

`B` - back face (the back side of the cube)

`L` - left face of the cube (on the left side when facing the front F face)

`R` - right face of the cube

This will help refer to how we will roate the cube.

<a name="how-color"></a>
## Color Notation

In the solved state, each cube face has one of six colors.
The orientation of these colors relative to one another
is always fixed; the red and orange colored faces, for example,
are never adjacent. This is due to the nature of the mechanical
pieces that compose the Rubik's Cube.

The standard orientation of colors to refer to the soled cube
is as follows:

* `U` = White
* `D` = Yellow
* `F` = Green
* `B` = Blue (Back-Blue)
* `L` = Orange
* `R` = Red (Red-Right)

Note that on a 3x3 cube, we can always determine the
final color a face will have, because the six center pieces
on each side of a 3x3 cube always remain fixed.

On a 4x4 cube, however, all four center squares can rotate 
and move, meaning all 24 center squares are totally 
interchangeable, and there is no link between the 
center colors on a 4x4 cube and the final color
that will be on that face when the cube is solved.

<a name="how-move"></a>
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

<a name="how-move-regular"></a>
### Regular Face Rotations

The regular face turns are denoted with capital letters:
`L R U D B F` refer to a single clockwise rotation of the 
respective face. Here, "clockwise" means *the direction
that is clockwise when facing the given face head-on.*

<a name="how-move-reverse"></a>
### Reverse Face Rotations

The `'` apostrophe following moves, as in `L' R' U' D' B' F'`,
indicates that the move shoud be a *counter-clockwise* 
rotation of the given face, instead of clockwise.

<a name="how-move-double"></a>
### Double Face Rotations

Rotations that are indicated using a lowercase letter
refer to two-layer rotations: `l r u d b f`.

<img src="images/cube4.jpg" width="300"/>
**Figure 4: Cube state after move `u`.**

That is, the lowercase `u` refers to the *clockwise* 
rotation of the top two layers of the cube; 
the lowercase `r` refers to the *clockwise* 
rotation of the rightmost two
layers of the cube; and so on.

The apostrophe also serves to indicate a 
*counter-clockwise* rotation: `'l r' u' d' b' f'`
indicate counter clockwise rotations of the two
left, two right, two upper, two bottom, two back,
and two front layers, respectively.

We have covered the first 24 moves - 
clockwise and counter-clockwise rotations
of single and double layers.

<a name="how-move-second"></a>
### Second Layer Face Rotations

<img src="images/cube5.jpg" width="300"/>
**Figure 5: Cube state after move `2U`.**

The `2` notation indicates a rotation of the second layer only. 
For example, `2U` refers to the clockwise rotation of the second 
layer from the top. This is equivalent to the move sequence 
`u U'`.

Likewise, the apostrophe indicates a counterclockwise rotation.

<a name="computer"></a>
# Computer Representation of a Rubik's Cube

The computer representation we are using is the 
[rubiks-cube-NxNxN-solver](https://github.com/dwalton76/rubiks-cube-NxNxN-solver)
library by Github user [@dwalton](https://github.com/dwalton76/).

We have modified this library to provide additional
functionality needed in the project; the fork used 
in this project is available at git.charlesreid1.com:
[rubiks-cube-nnn-solver](https://charlesreid1.com:3000/charlesreid1/rubiks-cube-nnn-solver)

Using this library, here's how we create a 4x4
Rubik's Revenge cube:

```
In [1]: from rubikscubennnsolver.RubiksCube444 import RubiksCube444, solved_4x4x4

In [2]: order = 'URFDLB'

In [3]: cube = RubiksCube444(solved_4x4x4, order)

In [4]: cube.print_cube()
         U U U U
         U U U U
         U U U U
         U U U U

L L L L  F F F F  R R R R  B B B B
L L L L  F F F F  R R R R  B B B B
L L L L  F F F F  R R R R  B B B B
L L L L  F F F F  R R R R  B B B B

         D D D D
         D D D D
         D D D D
         D D D D
```

<a name="computer-operations"></a>
## Operations and Functionality

Some important functionality:
* Obtaining each side
* Applying rotation
* Applying sequence of rotations
* Each side
* Side face numberings, centers, edges

To obtain each side, use the `sides` attribute:

```
In [8]: print(cube.sides)
OrderedDict([('U', <rubikscubennnsolver.RubiksSide.Side object at 0x11172d358>), 
             ('L', <rubikscubennnsolver.RubiksSide.Side object at 0x11172d240>), 
             ('F', <rubikscubennnsolver.RubiksSide.Side object at 0x11172d5c0>), 
             ('R', <rubikscubennnsolver.RubiksSide.Side object at 0x11172d5f8>), 
             ('B', <rubikscubennnsolver.RubiksSide.Side object at 0x11172d518>), 
             ('D', <rubikscubennnsolver.RubiksSide.Side object at 0x11172d390>)])
```

To apply a rotation of a single face, 
use the `rotate()` method:

```
In [10]: cube.rotate("U")

In [11]: cube.print_cube()
         U U U U
         U U U U
         U U U U
         U U U U

F F F F  R R R R  B B B B  L L L L
L L L L  F F F F  R R R R  B B B B
L L L L  F F F F  R R R R  B B B B
L L L L  F F F F  R R R R  B B B B

         D D D D
         D D D D
         D D D D
         D D D D
```

Unfortunately, the rotate method does not 
take sequences of moves, but this is easily
resolved:

```
In [12]: cube = RubiksCube444(solved_4x4x4, order)

In [13]: sequence = "U L U' L'"

In [14]: for move in sequence.split():
    ...:     cube.rotate(move)
    ...:

In [15]: cube.print_cube()
         L U U U
         U U U U
         U U U U
         U B B L

D F F F  R L L F  U R R R  B B B B
L L L L  F F F F  R R R R  B B B U
L L L L  F F F F  R R R R  B B B U
L L L L  F F F F  R R R R  B B B U

         D D D D
         D D D D
         D D D D
         B D D D
```

<a name="computer-face"></a>
## Face Numbering

Here is the numerical representation of the faces,
which we will make extensive use of:

```
In [6]: cube.print_cube_layout()
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



<a name="tuple"></a>
# Tuple Representation

Goal is to come up with a tuple representation of a 
unique cube state.

Goal is not to come up with minimal representation,
but to come up with unique repesentation.

Use a 96-tuple to represent location of each face.

<a name="tuple-requirements"></a>
## Tuple Representation Requirements

What tuple representation will look like
* Why can't just label faces/colors
* Not a multiset problem WWWWBBBBRRRR etc
* Numerical labeling of each face

<a name="tuple-representation"></a>
## Tuple Representation 

Tuple representation:
* 96 integers
* Caveat: 4 are interchangeable.
* Two approaches: one more complicated, one less complicated.
* More complicated: duplicates in 96-tuple
* Less complicated: 96 separate faces, but build in accounting for fact that four faces are interchangeable


<a name="preview-part-2"></a>
# Preview of Part 2

* Rotations and move sequences
* Create maps for rotations: where does each index go?

