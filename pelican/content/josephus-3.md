Title: The Josephus Problem: Part 3: Solving the Two Step Case
Date: 2019-03-19 14:00
Category: Computer Science
Tags: graphs, puzzles, algorithms, josephus, latex
Status: draft


* Solving the Double Step Case
    * Solution technique: step thru, 
      label n+1 starting point for each 
      person skipped
    * Repeat until all even, then k/2
    * knuth solution: doubling permutation, reverse, etc.

## Solving the Double Step Case

The Josephus Problem for a step size of $m = 2$
can be solved two ways:

- Label Skipped Nodes Algorithm (Algorithm S)
- Doubling Permutation Algorithm (Algorithm D)


## Algorithm S: Label Skipped Nodes

Step through circle

Each person that is skipped, label $n+1$

Repeat until all even

Removal index is k/2

## Algorithm D: Using Doubling Permutation

In Exercise 29, Knuth asks:

> Prove: the cycle form of the Josephus permutation
> when $m = 2$ can be obtained by expressing 
> the "doubling permutation" of $\{1, 2, \dots, 2n\}$,
> which takes $j$ into $(2j) \mod (2n+1)$ into
> cycle form, then **reversing** L and R, 
> and erasing all numbers larger than $n$.

### Write the Doubling Permutation

Start by writing down the first few terms of the 
doubling permutation:

$$
\left( 1 \, 2 \, 4 \, 8 \, 16 \, 32 \, \dots \right)
$$

When a number is greater than $2n+1 = 23$, it is
reduced $\mod (2n+1)$, so the next few terms of the
doubling permutation written out are:

$$
\left( 1 \, 2 \, 4 \, 8 \, 16 \, 32 \, 64 \, 128 \, 256 \, 512 \, 1024 \right)
$$

which reduces to:

$$
\left( 1 \, 2 \, 4 \, 8 \, 16 \, 9  \, 18 \,  13 \,   3 \, 6\, 12 \, 1 \right)
$$

At this point we reach 1, the starting value, so further 
doublings will result in repetition of the elements we have
so far. 

Next, continue the process with the remaining elements.
Start with the smallest element not included in the 
cycle found above, which is 5. Doing this results in
the terms:

$$
\left( 5 \, 10 \, 20 \, 40 \, 80 \, \dots \right)
$$

which reduces to:

$$
\left( 5 \, 10 \, 20 \, 17 \, 11 \, \dots \right)
$$

Repeating this until the first element repeats
yields all of the remaining elements:

$$
\left( 5 \, 10 \, 20 \, 17 \, 11 \, 22 \, 21 \, 19 \, 15 \, 7 \, 14 \right)
$$

Now the final doubling permutation can be written as the 
product of the two cycles:

$$
\left( 1 \, 2 \, 4 \, 8 \, 16 \, 9  \, 18 \,  13 \,   3 \, 6\, 12 \, 1 \right)
\left( 5 \, 10 \, 20 \, 17 \, 11 \, 22 \, 21 \, 19 \, 15 \, 7 \, 14 \right)
$$


### Reverse the Doubling Permutation

The next step is to reverse the permutation from left to right,
which means we step through all cycles from left to right,
and step through each cycle from left to right.

Starting with the doubling permutation:

$$
\left( 1 \, 2 \, 4 \, 8 \, 16 \, 9  \, 18 \,  13 \,   3 \, 6\, 12 \, 1 \right)
\left( 5 \, 10 \, 20 \, 17 \, 11 \, 22 \, 21 \, 19 \, 15 \, 7 \, 14 \right)
$$

We obtain the reverse:

$$
\left( 14 \, 7 \, 15 \, 19 \, 21 \, 22 \, 11 \, 17 \, 20 \, 10 \, 5 \right)
\left( 12 \, 6 \, 3 \, 13 \, 18 \, 9 \, 16 \, 8 \, 4 \, 2 \, 1 \right)
$$


### Trim the Reversed Doubling Permutation

Now we eliminate any numbers from the reversed doubling permutation
that are larger than $n = 11$, to get the trimmed permutation:

$$
\left( 7 \, 11 \, 10 \, 5 \right)
\left( 6 \, 3 \, 9 \, 8 \, 4 \, 2 \, 1 \right)
$$

This is the final Josephus permutation. The one remaining step is to
rewrite the cycles in standard "sorted" order:

$$
\left( 1 \, 6 \, 3 \, 9 \, 8 \, 4 \, 2 \right)
\left( 5 \, 7 \, 11 \, 10 \right)
$$

Congratulations! You just solved the problem.

### Why Does Algorithm D Work?

To understand why Algorith D works, it is instructive
to consider a case where $n$ is a power of two. Let us
consider $n = 8, m = 2$.

```
 j   |  2j  |  2j mod 2n+1
-----|------|---------------
  1  |   2  |        2
  2  |   4  |        4
  3  |   6  |        6
  4  |   8  |        8
  5  |  10  |       10
  6  |  12  |       12
  7  |  14  |       14
  8  |  16  |       16
- - - - - - - - - - - - - - -
  9  |  18  |        1
 10  |  20  |        3
 11  |  22  |        5
 12  |  24  |        7
 13  |  26  |        9
 14  |  28  |       11
 15  |  30  |       13
 16  |  32  |       15
```

Creating a table of values $j, 2j, (2j) \mod (2n+1)$
for $j = 1 dots 2j$ uncovers structure: of the $2j$ entries,
the first $j$ result in an even value of $(2j) \mod (2n + 1)$ 
while the remaining $j$ result in an odd value of 
$(2j) \mod (2n+1)$.











