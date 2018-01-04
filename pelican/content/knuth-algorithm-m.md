Title: Let's Generate Some Tuples!
Date: 2018-01-02 18:00
Category: Computer Science
Tags: combinatorics, permutations, python, computer science, algorithms, art of computer programming, knuth

# Generating Permutations

In today's post we're going to discuss the generation of permutations.

Often, in combinatorics problems, we are interested in *how many* different
instances or configurations of a particular thing we can have (what we'll call
"enumeration" or "counting"). However, that is different from wanting to 
actually see all of those configurations. Indeed, if we are counting 
something with an astronomical number of configurations, we don't want 
to try to list all of them.

However, as usual, Donald Knuth, who covers the topic of permutation 
generation in Volume 4A of his classic work, 
<u>The Art of Computer Programming</u>,
uncovers a problem that is much more complicated and subtle
than it initially appears.



## Background: Radix Method for Generating Permutations

In Volume 4A of his classic work, <u>The Art of Computer Programming</u>, 
Donald Knuth turns to the question of generating permutations for a given
combinatoric system. The book opens with Knuth jumping immediately into 
the problem of generating permutations.

Algorith M is the first algorithm Knuth presents to generate all unique tuples.
To pose the problem a little more clearly, consider a combinatoric system that
has $n$ independent parts, each part having a number of possible states.
We can completely specify the state of the combinatoric system by specifying
an $n$-tuple:

$$
(a_1, a_2, \dots, a_n)
$$

where each independent variable takes on one of its possible values $0 \leq a_i \leq m_i$.

Knuth's Algorithm M starts by setting all a's to 0, and incrementing 
the right-most entry of the tuple (carrying if necessary). 

This is equivalent to counting in binary from 0 to $N-1$,
or to labeling every possible outcome with a number between 0 and $N-1$.

This becomes more clear if we consider the $n$-tuple to be 
a number in a variable-radix system:

The number is $\left[ a_1, a_2, \dots, a_n \right]$

The radix is $\left[ m_1, m_2, \dots, m_n \right]$

By repeatedly adding 1 to the number $\left[ a_1, a_2, \dots, a_n \right]$, 
we iterate through every possible tuple $(a_1, a_2, \dots, a_n)$ and 
therefore through every possible combination of the independent variables.



## Knuth's Algorithm M

**Algorithm M** *(Mixed-radix generation)*. This algorithm visits all $n$-tuples that satisfy the number/radix expressions above, by repeatedly adding 1 to the mixed-radix number until overflow occurs. (Aux. variables $a_0$ and $m_0$ introduced for convenience only.)

**M1.** [Initialize.] Set $a_j \rightarrow 0$ for $0 \leq j \leq n$, set $m_0 \rightarrow 2$.

**M2.** [Visit.] Visit the $n$-tuple $(a_1, \dots, a_n)$. (The program that wants to examine all $n$-tulpes now does its thing.)

**M3.** [Prepare to add one.] Set $j \rightarrow n$.

**M4.** [Carry if necessary.] If $a_j = m_j - 1$, set $a_j \rightarrow 0, j \rightarrow j-1$ and repeat this step.

**M5.** [Increase, unless done.] If $j=0$, terminate algorithm. Otherwise set $a_j = a_j + 1$ and go back to step $M2$.



## Implementing Algorithm M

Unfortunately, this pseudocode takes some work to translate. Fortunately, that's already done in the method below.

The method below implements Algorithm M in Python to generate random sequences on a 4x4 Rubik's Cube (called the Rubik's Revenge, or RR for short). The RR cube has six faces that can each be rotated clockwise or counterclockwise by a single layer, denoted by the uppercase letters U, D, B, F, L, R (up, down, back, front, left, right, respectively) for clockwise rotations and U', D', B', F', L', R' for counterclockwise rotations, for 12 total moves.

However, on a 4x4 cube, we can also rotate *two* layers at a time. (That's the limit; moving three layers at a time is equivalent to a reversed rotation of the remaining single layer.) This type of rotation is denoted with a "w".

Thus, rotating the top two layers of each of the six faces clockwise is denoted Uw, Dw, Bw, Fw, Lw, Rw, and counterclockwise rotations are denoted Uw', Dw', Bw', Fw', Lw', Rw', for 12 additional moves.

We have one more type of move, which is where the second layer only is removed. This type of move is denoted with 2, and the face whose second layer is being rotated, for six moves: 2U, 2D, 2B, 2F, 2L, 2R. The prime notation denotes again a counterclockwise rotation, for an additional six moves: 2U', 2D', 2B', 2F', 2L', 2R'. This yields another 12 moves.

There are 36 total moves that can be executed on the 4x4 Rubik's Revenge cube.

```python
def algorithm_m(n):
    """
    Knuth's Algorithm M for permutation generation,
    via AOCP Volume 4 Fascile 2.
    This is a generator that returns permtuations 
    generated using the variable-radix method. 

    This generates ALL permutations.
    Many of these are rotations of one another,
    so use the get_rotations() function
    (defined later) to eliminate redundant sequences.
    """
    moves = ['A','B','C','D']

    # M1 - Initialize
    a = [0,]*n
    m = [len(moves),]*n

    j = n-1

    nvisits = 0
    while True:

        # M2 - visit
        move_sequence = " ".join([ moves[int(aj)] for aj in a])
        yield move_sequence 

        nvisits += 1

        # M3 - prepare to +1
        j = n-1

        # M4 - carry
        while( a[j] == m[j]-1):
            a[j] = 0
            j = j-1
        
        # M5 - increase unless done
        if(j<0):
            break
        else:
            a[j] = a[j] + 1
```



## Test Drive

Let's take a look at how Algorithm M looks when it is applied. 
No surprises here: Algorithm M generates each of the possible 
permutations in sequence.

```python
from pprint import pprint

# (Algorithm M goes here) 

if __name__=="__main__":
    pprint(list(algorithm_m(3)))
```

and the result:

```
    ['A A A',
     'A A B',
     'A A C',
     'A A D',
     'A B A',
     'A B B',
     'A B C',
     'A B D',
     'A C A',
     'A C B',
     'A C C',
     'A C D',
     'A D A',
     'A D B',
     'A D C',
     'A D D',
     'B A A',
     'B A B',
     'B A C',
     'B A D',
     'B B A',
     'B B B',
     'B B C',
     'B B D',
     'B C A',
     'B C B',
     'B C C',
     'B C D',
     'B D A',
     'B D B',
     'B D C',
     'B D D',
     'C A A',
     'C A B',
     'C A C',
     'C A D',
     'C B A',
     'C B B',
     'C B C',
     'C B D',
     'C C A',
     'C C B',
     'C C C',
     'C C D',
     'C D A',
     'C D B',
     'C D C',
     'C D D',
     'D A A',
     'D A B',
     'D A C',
     'D A D',
     'D B A',
     'D B B',
     'D B C',
     'D B D',
     'D C A',
     'D C B',
     'D C C',
     'D C D',
     'D D A',
     'D D B',
     'D D C',
     'D D D']
```



## What Other Ways Are There?

All of this may seem obvious or uninteresting,
if you don't realize there are other ways of 
generating all possible $n$-tuples.

It's a bit easier to think about for binary 
numbers. Imagine you're trying to generate 
every possible 10-digit binary number.
This means generating all binary numbers
between $0$ and $2^{10}-1$. 

Algorithm M, as we saw above, just counts 
from 0 to $2^{10}-1$. But this can involve
changing a large number of bits (for example,
adding 1 to 001111111 results in 010000000,
changing 8 digits. Knuth presents an
alternative algorithm that only requires
changing *one* bit to generate the next
permutation, making the algorithm much 
faster.

More on that algorithm in a future blog post...

