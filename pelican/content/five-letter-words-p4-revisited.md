Title: Five Letter Words: Part 1: Getting Familiar With The List
Date: 2019-03-10 10:00
Category: Computer Science
Tags: python, computer science, graphs, algorithms, art of computer programming, knuth, five letter words

## Table of Contents

* [Five Letter Words, Revisited](#five4-about)
* [Different By One, Revisited](#five4-different-by-one)
* [Different By N, Revisited](#five4-different-by-one)

<a name="five4-about"></a>
## About the Five-Letter Words

In Volume 4, Facsimile 0 of Donald Knuth's <u>Art of Computer Programming</u>, 
in which Knuth covers graph theory, he introduces a list of five-letter words
as part of a data set useful in exploring graph theory and graph algorithms.

The [list of words](https://github.com/charlesreid1/five-letter-words/blob/master/sgb-words.txt) 
is part of the [Stanford Graph Base](http://www3.cs.stonybrook.edu/~algorith/implement/graphbase/implement.shtml), 
a set of data sets that are useful for studying graph theory and networks.

See [Five Letter Words](https://charlesreid1.com/wiki/Five_Letter_Words)
on the charlesreid1.com wiki for details.


<a name="five4-diff-by-one"></a>
## Different by 1, Revisited

This post is revisiting an exercise from the above volume,
Exercise 28:

> Find pairs of SGB word vectors that differ by
> +/- 1 in each component.

In a prior blog post ([Part 1](#)),
we had inerpreted the question as finding
word vectors whose Euclidean distance differed
by 1 total, which is the same as a Hamming
distance of 1.

However, on revisiting the (more interesting)
question actually being posed by the author,
we find a different and more difficult problem.

As an example of what Knuth is asking for:

```
rover -> spuds
```

Each letter of the words are within an edit
distance of 1, at each position.

There are 38 such pairs:

```
$ python diff_by_one_fixed.py
abaft babes
absit baths
adder beefs
ambit blahs
anger boffs
anode boned
bider chefs
bidet chefs
biffs cheer
ghost hints
hobos inapt
holds inker
honed inode
hoods inner
hoofs inner
hoots input
hoped inode
ingot johns
needs odder
needs offer
rider sheds
rifer sheds
rinds shoer
robed spade
robot snaps
robot spans
rover spuds
ruffs steer
runts stout
rusts strut
sheer tiffs
sheet tiffs
shout tints
sides theft
sneer toffs
splat tombs
spuds toter
stuns tutor
Found 38 pairs of words that differ by +/-1 in each component.
```

The approach we used was as follows:

- Iterate over each word in the wordlist
  (use the first 1,000 words to keep it
  shorter for testing)
- For each word:
  - Generate all variations that are within +/-1 
    using recursive backtracking (could also use
    algorithm to generate all 32 binary codes of 
    length 5, where 0 = -1, 1 = +1)
  - For each of the 32 variations,
    - Check if the word is in the wordset
      (O(1) cost if using a hash table/set)
    - If so, add ordered pair (word1,word2)
      to a set of solutions (to avoid dupes)

We went back and modified the code to take a
distance parameter d, but storage and compute
cost, as well as the sparsity of the graph of
shared bigrams and trigrams among these 5,000
words, means the number of pairs increases 
exponentially.

| Distance  | Number of pairs   | Walltime      |
|-----------|-------------------|---------------|
| 1         | 38                |     0.26 s    |
| 2         | 525               |     5.26 s    |
| 3         | 4982              |    38.87 s    |
| 4         | ???               |  10 min (est) |

You can find the `diff_by_n.py` script here:
<https://git.charlesreid1.com/cs/five-letter-words/>

The output:

```
$ python diff_by_n.py
abaft babes
absit baths
adder beefs
ambit blahs
anger boffs
anode boned
bider chefs
bidet chefs
biffs cheer
ghost hints
..
Found 38 pairs of words that differ by +/-1 in each component.
Time: 0.2673 s

aback babel
aback cabal
abaft babes
abash cacti
abide baked
abide caged
abide caked
abler bands
abler bangs
abode caned
...
Found 525 pairs of words that differ by +/-2 in each component.
Time: 5.2617 s

abaca ceded
abaci babel
abaci cabal
abaci decaf
abaci decal
aback babel
aback cabal
aback decal
abaft babes
abaft bedew
...
Found 4982 pairs of words that differ by +/-3 in each component.
Time: 38.8743 s
```


