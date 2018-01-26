Title: 4x4 Rubik's Cube: Part 4: Sequence Order
Date: 2018-01-25 10:00
Category: Rubiks Cube
Tags: rubiks cube, combinatorics, permutations, python, puzzles, art of computer programming, knuth

*This is Part 4 of a 4-part blog post 
on the mathematics of the 4x4 Rubik's Cube, 
its relation to algorithms, and some 
curious properties of Rubik's Cubes.*

See Part 1 of this blog post here: [Part 1: Representations](https://charlesreid1.github.io/4x4-rubiks-cube-part-1-representations.html)

See Part 2 of this blog post here: [Part 2: Permutations](https://charlesreid1.github.io/4x4-rubiks-cube-part-2-permutations.html)

See Part 3 of this blog post here: [Part 3: Factoring Permutations](https://charlesreid1.github.io/4x4-rubiks-cube-part-3-factoring-permutations.html)

You are currently reading Part 4 of this blog post: **Part 4: Sequence Order**

# Table of Contents

* [Introduction](#rubiks4-intro)

* [Factoring Rubik's Cube Permutations](#rubiks4-factoring)
    * [Factoring Permutations: A Review](#rubiks4-factoring-review)
    * [Factoring Rubik's Cube Permutations](#rubiks4-factoring-cube)
    * [Computing the Order of Sequence R](#rubiks4-factoring-R)
    * [Computing the Order of Sequence U R U' R'](#rubiks4-factoring-URUpRp)
    * [Computing the Order of Sequence U R](#rubiks4-factoring-UR)

* [Code](#rubiks4-code)

* [Project Conclusions](#rubiks4-conclusions)

* [References](#rubiks4-references)

* [Appendix](#rubiks4-appendix)


<br />
<br />
<br />


<a name="rubiks4-intro"></a>
# Introduction

<a name="rubiks4-intro-order"></a>
## Order of a Sequence

As a reminder of our overarching goal: starting with a 
4x4 Rubik's Revenge cube, an arbitrary sequence of moves
will scramble the faces of the cube; but if that move sequence 
is repeatedly applied, eventually the cube will return to its
solved state. 

The simplest example is rotating a single face: after applying
the rotation move four times to any face of a solved cube,
the cube will return back to the solved state.

This is also true of more complicated move sequences, such as
`U R U' R'`, which returns the cube back to its original state
after 6 applications, or the move sequence `U R`, which
must be applied 105 times before the cube returns back to
its original solved state.

Our goal is to predict this number: given a move sequence,
how many times must that move sequence be applied to a solved 
cube to return the cube back to its solved state?

This number is called the *order* of a sequence.

<a name="rubiks4-intro-sofar"></a>
## What We Have Covered So Far

In prior posts, we have covered a number of key topics 
that this post will synthesize.

We started [Part 1](https://charlesreid1.github.io/4x4-rubiks-cube-part-1-representations.html) by discussing ways of representing 
the Rubik's Revenge cube, and we settled on a 96-tuple
representation indicating which faces had moved to what 
locations.

That led us to [Part 2](https://charlesreid1.github.io/4x4-rubiks-cube-part-2-permutations.html), in which we discussed the two-row
notation for the 96-tuple representing the cube, and 
demonstrated the utility of this representation by 
showing how moves and move sequences would lead to 
permutations that could be written as 96-tuples using
the two-row notation.

In [Part 3](https://charlesreid1.github.io/4x4-rubiks-cube-part-3-factoring-permutations.html), we covered some key theoretical results following
Donald Knuth's <u>Art of Computer Programming</u> which allowed
us to develop a permutation algebra to describe the effects 
moves have on the cube. We concluded the previous post 
with an algorithm for factoring permutations into their
intercalation products, and hinted that these permutation
factors were central 

<a name="rubiks4-factoring"></a>
# Factoring Rubik's Cube Permutations

<a name="rubiks4-factoring-review"></a>
## Factoring Permutations: A Review

In [Part 3](https://charlesreid1.github.io/4x4-rubiks-cube-part-3-factoring-permutations.html) of this series of blog posts, we looked at 
an example multiset permutation of characters. Here it is
written using the two-row notation:

$$
\pi = \bigl(\begin{smallmatrix}
    a & a & b & b & b & b & b & c & c & c & d & d & d & d & d \\
    d & b & c & b & c & a & c & d & a & d & d & b & b & b & d
\end{smallmatrix}\bigr)
$$

We covered a technique for factoring this permutation
into independent cycles of faces,

$$
\pi = \alpha \top \beta \top \dots \top \gamma
$$

and shared Python code to perform this operation. The resulting
factored permutation was:

$$
\pi = \bigl( \begin{smallmatrix}
    a & d & d & b & c & d & b & b & c \\
    d & d & b & c & d & b & b & c & a
\end{smallmatrix} \bigr)
\top
\bigl( \begin{smallmatrix}
    a & b \\
    b & a 
\end{smallmatrix} \bigr)
\top 
\bigl( \begin{smallmatrix}
    b & c & d  \\
    c & d & b
\end{smallmatrix} \bigr)
\top 
\bigl( \begin{smallmatrix}
    d \\
    d
\end{smallmatrix} \bigr)
$$

<a name="rubiks4-factoring-cube"></a>
## Factoring Rubik's Cube Permutations

To factor a Rubik's Cube permutation, we apply
Algorithm A from the prior post to the two-row
96-tuple representation of the Rubik's Cube 
after it has had the move sequence applied once.

(Note that we only need to apply the sequence
to the cube *once*, even if the order of that 
sequence is in the tens of thousands.)

Let's look at a few move sequences for 
some examples:

<a name="rubiks4-factoring-R"></a>
## Computing the Order of Sequence R

We begin with the solved state, and apply the 
move R to the cube. The result is the 
two-line representation:

```
(01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96)
(01 02 03 36 05 06 07 40 09 10 11 44 13 14 15 48 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 84 37 38 39 88 41 42 43 92 45 46 47 96 61 57 53 49 62 58 54 50 63 59 55 51 64 60 56 52 16 66 67 68 12 70 71 72 08 74 75 76 04 78 79 80 81 82 83 77 85 86 87 73 89 90 91 69 93 94 95 65)
```

Now, we can carry out the Algorithm A procedure on
this two-row representation. When we do that, we will
find that there are a large number of one-element 
independent factors; these are the faces that do not 
move during the move sequence R. 

Here is a list of factors that are found by Algorithm A:

```
Factor sizes: {1, 4}
Factors:
[36, 84, 77, 4]
[40, 88, 73, 8]
[44, 92, 69, 12]
[48, 96, 65, 16]
[61, 64, 52, 49]
[57, 63, 56, 50]
[53, 62, 60, 51]
[58, 59, 55, 54]
Independent Faces: [1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 37, 38, 39, 41, 42, 43, 45, 46, 47, 66, 67, 68, 70, 71, 72, 74, 75, 76, 78, 79, 80, 81, 82, 83, 85, 86, 87, 89, 90, 91, 93, 94, 95]
Least common multiple: 4
```

The largest set of faces that are exchanged is 4, and 
the smallest is 1. No other groups of faces being 
exchanged have any other sizes. This means that if 
we apply the sequence 4 times, each of those groups 
of faces being interchanged will have returned to their 
original state.

This tells us what we already knew: that if we apply the 
sequence "R", it rotates groups of pieces in a sequence 
of 4 moves each, so overall the order of this permutation 
is 4 - if we apply the sequence R to a solved 4x4 Rubik's 
Revenge cube 4 times, the cube will return to the solved 
state.

To formalize this, if we have cycles with arbitrary lengths, 
we must apply the sequence a number of times equal to the 
least common multiple of each factor's size. (For example, 
if we had a cycle of length 3 above, the cycle order would 
have been 12 - because the sequence must be applied 12 times 
before the 4-cycle face exchanges "sync up" with the 3-cycle 
face exchanges.)

Let's look at a slightly more complicated move sequence
to illustrate this point.

<a name="rubiks4-factoring-URUpRp"></a>
### Computing the Order of Sequence U R U' R'

As before, we begin by applying the move sequence
once to a solved cube to generate the two-row
n-tuple representation:

```
(01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96)
(01 02 03 77 05 06 07 73 09 10 11 69 16 12 08 20 17 18 19 36 21 22 23 24 25 26 27 28 29 30 31 32 49 50 51 33 37 38 39 40 41 42 43 44 45 46 47 48 13 56 60 64 53 54 55 34 57 58 59 35 61 62 63 04 96 66 67 68 14 70 71 72 15 74 75 76 65 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 52)
```

Next, we factor this permutation using Algorithm A:

```
Factor sizes: {1, 3, 6}
Factors:
[77, 65, 96, 52, 64, 4]
[73, 15, 8]
[69, 14, 12]
[16, 20, 36, 33, 49, 13]
[50, 56, 34]
[51, 60, 35]
Independent Faces: [1, 2, 3, 5, 6, 7, 9, 10, 11, 17, 18, 19, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 53, 54, 55, 57, 58, 59, 61, 62, 63, 66, 67, 68, 70, 71, 72, 74, 75, 76, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95]
Least common multiple: 6
```

This time, we get a couple of cycles with different lengths.
We have four cycles of length 3, and two cycles of length 6,
plus many cycles of length 1 (the unpermuted faces).

The LCM of 3 and 6 is 6, so the overall order of the 
move sequence `U R U' R'` is 6.

<a name="rubiks4-factoring-UR"></a>
### Computing the Order of Sequence U R

The last sequence we'll look at is the move sequence UR.

This particular permutation represents an 
interesting corner case: in [Part 1](https://charlesreid1.github.io/4x4-rubiks-cube-part-1-representations.html) of this post,
when we came up with our tuple representation
for the cube, we treated each face as being
non-interchangeable, by giving each face a 
unique number. This means that, for example,
we cannot swap two arbitrary red faces, since
they are attached to other faces via a double edge
or a corner piece.

This assumption does *not* hold for faces 
in the center of the cube. Because center faces
are not attached to any other faces (mechanically 
speaking), the four distinct integers representing
four colored faces can actually be interchanged.

This plays out with the sequence `U R` as follows:

We start with the two-line representation of the 
n-tuple:

```
(01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96)
(13 09 05 01 14 10 06 02 15 11 07 03 48 44 40 36 33 34 35 84 21 22 23 24 25 26 27 28 29 30 31 32 61 57 53 49 37 38 39 88 41 42 43 92 45 46 47 96 16 66 67 68 62 58 54 50 63 59 55 51 64 60 56 52 17 18 19 20 12 70 71 72 08 74 75 76 04 78 79 80 81 82 83 77 85 86 87 73 89 90 91 69 93 94 95 65)
```


We can factor this tuple as follows:

```
Factor sizes: {1, 3, 4, 7, 15}
Factors:
[13, 48, 96, 65, 17, 33, 61, 64, 52, 68, 20, 84, 77, 4, 1]
[9, 15, 40, 88, 73, 8, 2]
[5, 14, 44, 92, 69, 12, 3]
[10, 11, 7, 6]
[36, 49, 16]
[34, 57, 63, 56, 50, 66, 18]
[35, 53, 62, 60, 51, 67, 19]
[58, 59, 55, 54]
Independent Faces: [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 37, 38, 39, 41, 42, 43, 45, 46, 47, 70, 71, 72, 74, 75, 76, 78, 79, 80, 81, 82, 83, 85, 86, 87, 89, 90, 91, 93, 94, 95]
Least common multiple: 420
```

However, the adventurous cuber will find, when actually 
carrying out this move sequence, that the order is in fact 
105, and not 420.

The reason the predicted cube order is 4 times larger than
expected is because, after 105 applications of the move 
sequence, the cube has not actually returned to its original
state, but the only remaining faces that are scrambled
are center faces, which are in fact interchangeable.

Note this group of 4 faces that are permuted:

```
[10, 11, 7, 6]
```

These are the four center squares from the `U` face. 
If we exclude this group (treating 10, 11, 7, and 6 as 
perfectly interchangeable), the length of all factors
no longer contains 4:

```
Factor sizes: {1, 3, 7, 15}
```

Including the 4, we had

LCM(1,3,4,7,15) = 420

but excluding the 4, we get:

LCM(1,3,7,15) = 105

Systematically, we can search for any groups that contain
*only*  faces from the center, and treat 1 such group of 
length n as n groups of length 1 (not contributing to the 
order of the move sequence).

This provides an interesting contrast between the 4x4 Rubik's 
Revenge cube, in which any center faces may be interchanged with 
any other center faces, and the 3x3 Rubik's Cube, in which
the center faces always remain fixed in relation to one another.

<a name="rubiks4-factoring-UwRw"></a>
### Computing the Order of Sequence Uw Rw

We mentioned in [Part 1](https://charlesreid1.github.io/4x4-rubiks-cube-part-1-representations.html) 
that the move notation `Uw` or `Dw` indicates a 
quarter clockwise turn of two layers of a face,
not one. We can write the permutation that results
from the move sequence `Uw Rw` as:

```
(01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96)
(13 09 05 01 14 10 06 02 47 43 39 35 48 44 40 36 33 34 83 84 37 38 87 88 25 26 27 28 29 30 31 32 61 57 53 49 62 58 54 50 41 42 91 92 45 46 95 96 16 15 67 68 12 11 71 72 63 59 55 51 64 60 56 52 17 18 19 20 21 22 23 24 08 07 75 76 04 03 79 80 81 82 78 77 85 86 74 73 89 90 70 69 93 94 66 65)
```

Factoring this permutation, we get:

```
Factor sizes: {1, 3, 15}
Factors:
[13, 48, 96, 65, 17, 33, 61, 64, 52, 68, 20, 84, 77, 4, 1]
[9, 47, 95, 66, 18, 34, 57, 63, 56, 72, 24, 88, 73, 8, 2]
[5, 14, 44, 92, 69, 21, 37, 62, 60, 51, 67, 19, 83, 78, 3]
[10, 43, 91, 70, 22, 38, 58, 59, 55, 71, 23, 87, 74, 7, 6]
[39, 54, 11]
[35, 53, 12]
[40, 50, 15]
[36, 49, 16]
Independent Faces: [25, 26, 27, 28, 29, 30, 31, 32, 41, 42, 45, 46, 75, 76, 79, 80, 81, 82, 85, 86, 89, 90, 93, 94]
Least common multiple: 15
```

Several groups of 3 faces and of 15 faces, respectively, are permuted,
giving an LCM of 15. Thus, the order of move sequence `Uw Rw` is 15.

We'll look at the factoring of one last sequence: `U Rw`.

<a name="rubiks4-factoring-URw"></a>
### Computing the Order of Sequence U Rw

Here is the permutation representing the 
permutation resulting from the sequence U Rw:

```
(01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96)
(13 09 05 01 14 10 06 02 47 43 39 35 48 44 40 36 33 34 83 84 21 22 23 24 25 26 27 28 29 30 31 32 61 57 53 49 37 38 87 88 41 42 91 92 45 46 95 96 16 15 67 68 62 58 54 50 63 59 55 51 64 60 56 52 17 18 19 20 12 11 71 72 08 07 75 76 04 03 79 80 81 82 78 77 85 86 74 73 89 90 70 69 93 94 66 65)
```

Factoring this permutation, we get:

```
Factor sizes: {1, 3, 4, 10, 15, 16}
Factors:
[13, 48, 96, 65, 17, 33, 61, 64, 52, 68, 20, 84, 77, 4, 1]
[9, 47, 95, 66, 18, 34, 57, 63, 56, 50, 15, 40, 88, 73, 8, 2]
[5, 14, 44, 92, 69, 12, 35, 53, 62, 60, 51, 67, 19, 83, 78, 3]
[10, 43, 91, 70, 11, 39, 87, 74, 7, 6]
[36, 49, 16]
[58, 59, 55, 54]
Independent Faces: [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 37, 38, 41, 42, 45, 46, 71, 72, 75, 76, 79, 80, 81, 82, 85, 86, 89, 90, 93, 94]
Least common multiple: 240
```

The order of the move sequence `U Rw` is 240.

<a name="rubiks4-code"></a>
# Code

The code that forms the permutation tuple for a given move sequence
and performs the factoring of that tuple is in [sequence_order.py](https://charlesreid1.com:3000/charlesreid1/rubiks-cube-cycles/src/master/sequence_order.py).

The `sequence_order.py` file utilizes the 
[dwalton76/rubiks-cube-NxNxN-solver](https://github.com/dwalton76/rubiks-cube-NxNxN-solver)
library from Github to apply the move sequence once to a cube
to determine the resulting permutation tuple. It then factors 
this tuple into products and finds the LCM of their lengths.

The code in `sequence_order.py` is grouped into functions,
with the key funtion being `factor_permutation(top, bottom)`, which 
takes the top and bottom rows of the two-row representation
of a move sequence's permutation.

The method then performs the factoring procedure covered in
[Part 3](https://charlesreid1.github.io/4x4-rubiks-cube-part-3-factoring-permutations.html).

Here is the body of the method:

```python
def factor_permutation(perm_top,perm_bot):
    """
    Factor a permutation into its lowest terms
    """
    MAX = 96
    
    # Need a way to also mark them as used... bit vector
    used_vector = [0,]*len(perm_top)

    i = 0
    start = perm_top[0]
    used_vector[0] = 1
    factors = []

    # If we still have values to pick out:
    while(0 in used_vector):

        factor = []

        while(True):
            used_vector[i] = 1
            leader = perm_top[i]
            follower = perm_bot[i]

            i = perm_top.index(follower)
            while(used_vector[i]==1):
                i += 1
                if(i>=MAX):
                    break

            if(i>=MAX):
                break
            elif(follower==start):
                break
            else:
                factor.append(follower)

        # add start to end
        factor.append(start)

        factors.append(factor)
        try:
            #import pdb; pdb.set_trace()
            i = used_vector.index(0)
            start = perm_top[i]
        except ValueError:
            break

    return factors
```

This was called by the method applying move sequences
to the Rubik's Cube to obtain the two-row permutation
corresponding to the move sequence of interest.

<a name="rubiks4-conclusions"></a>
# Project Conclusions

In addition to being interesting, this project led to 
some deep insights into the workings of the Rubik's Cube
and ways to think about move sequences.

More than that, the Rubik's Cube is a toy that provides 
real insight into combinatorics and group theory. The 
concept of order, and the process of thinking through 
different representations of the cube and their consequences
for the implemetation of the final algorithm, provide 
good practice for problems in other, related domains.

This project began with a simple question. 
While playing with the Rubik's Cube,
we discovered this property of cycles 
(it is actually difficult to miss,
even when learning the beginner method,
as many of the move sequences involved in the 
beginner method have small orders, so it is 
easy to see them repeat.)
The question we set out to answer was,
given an arbitrary sequence, can we determine
the order of that sequence? 

The key to answering this question ultimately
lies in the representation of the permutations;
the right representation makes finding the 
order possible. but it took some trial 
and error with different representations 
before discovering the right approach.

To anyone who has played with the Rubik's Cube
before, it seems natural that there would be 
*some* way to represent moves applied to the cube
in some kind of algebraic terms.
The intercalation product was the key concept
for developing a permutation algebra.
Knuth's Algorithm A was the key concept 
for factoring permutations into their 
respective independent cycles.

Once an algorithm to factor permutations was developed,
the rest was a straightforward calculation of the LCM
of the lengths of each factor.

The project was computationally challenging;
recursion was required to implement Algorithm A,
the Rubik's Cube solver had to be modified,
and there were many bugs along the way.

The procedure we used here can be applied to other problems.
Our procedure was:

* Find a proper, convenient representation for the system state
* Break down the variations of the system into simple cases or steps
* Move away from the specific system, 
    and keep the approach mathematially general. **This is by far the the most 
    important step!**
* Study the literature and solutions to problems, to become familiar
    with different ways of representing a problem. Different problems
    lend themselves well to different representations, so the more familiar
    you are with different representations, the more problems you'll be able
    to tackle.
* The only way to get familiar with different problem-solving approaches 
    is through practice. It helps to start with easier problems, both because
    you can score some quick points and feel more confident, and also because
    combinatorics and group theory problems often tend to appear simple,
    but deceptively so. The devil is in the details.

<a name="rubiks4-references"></a>
# References

1. "Rubik's Cube". Charlesreid1.com wiki, Charles Reid. Edited 25 January 2017. Accessed 25 January 2017.
<[https://charlesreid1.com/wiki/Rubiks_Cube](https://charlesreid1.com/wiki/Rubiks_Cube)>

2. "Rubik's Revenge". Charlesreid1.com wiki, Charles Reid. Edited 25 January 2017. Accessed 25 January 2017.
<[https://charlesreid1.com/wiki/Rubiks_Revenge](https://charlesreid1.com/wiki/Rubiks_Revenge)>

3. "Rubik's Cube/Tuple". Charlesreid1.com wiki, Charles Reid. Edited 25 January 2017. Accessed 25 January 2017.
<[https://charlesreid1.com/wiki/Rubiks_Cube/Tuple](https://charlesreid1.com/wiki/Rubiks_Cube/Tuple)>

4. "Rubik's Cube/Permutations". Charlesreid1.com wiki, Charles Reid. Edited 25 January 2017. Accessed 25 January 2017.
<[https://charlesreid1.com/wiki/Rubiks_Cube/Permutations](https://charlesreid1.com/wiki/Rubiks_Cube/Permutations)>

5. "Github - dwalton76/rubiks-cube-NxNxN-solver". dwalton76, Github Repository, Github Inc. Accessed 11 January 2017.
<[https://github.com/dwalton76/rubiks-cube-NxNxN-solver](https://github.com/dwalton76/rubiks-cube-NxNxN-solver)>

6. "Rubik's Cube NxNxN Solver". Git repository, git.charlesreid1.com. Charles Reid. Updated 25 January 2017.
<[https://charlesreid1.com:3000/charlesreid1/rubiks-cube-nnn-solver](https://charlesreid1.com:3000/charlesreid1/rubiks-cube-nnn-solver)>

7. "Rubiks Cube Cycles". Git repository, git.charlesreid1.com. Charles Reid. Updated 25 January 2017.
<[https://charlesreid1.com:3000/charlesreid1/rubiks-cube-cycles](https://charlesreid1.com:3000/charlesreid1/rubiks-cube-cycles)>


<a name="rubiks4-appendix"></a>
# Appendix

That concludes our discussion of computing the order of move sequences
on a Rubik's Cube. There are many move sequences, and many orders, 
ranging from 1 or 2 up to nearly 100,000. We plan to assemble a 
web site to help readers explore some move sequences and their 
orders - so check back soon...

