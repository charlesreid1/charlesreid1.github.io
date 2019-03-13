Title: Five Letter Words: Part 5: The Try Trie Tree
Date: 2019-03-11 18:00
Category: Computer Science
Tags: python, computer science, graphs, algorithms, art of computer programming, knuth, five letter words, tries, trees

## Table of Contents

* [Table of Contents](#table-of-contents)
* [About the Five\-Letter Words](#about-the-five-letter-words)
* [Introduction to the Try Trie Tree Problem](#introduction-to-the-try-trie-tree-problem)
* [The Try Trie Tree](#the-try-trie-tree)
* [Constructing the Try Trie Tree](#constructing-the-try-trie-tree)
    * [Checking for Minimum Number of Matching Words](#checking-for-minimum-number-of-matching-words)
    * [Assemble Method](#assemble-method)
    * [Verifying Branches and Bubbling Up Counts](#verifying-branches-and-bubbling-up-counts)
    * [Bubble Up Method](#bubble-up-method)
* [Try Trie Tree Code](#try-trie-tree-code)
    * [Try Trie Trie Class](#try-trie-trie-class)
    * [Code for Assembling the Tree](#code-for-assembling-the-tree)
    * [Code for Bubbling Up Large Children Counts](#code-for-bubbling-up-large-children-counts)
* [Wrap it in a Bow](#wrap-it-in-a-bow)
* [Output](#output)

## About the Five-Letter Words

In Volume 4 Fascicle 0 of Donald Knuth's <u>Art of Computer Programming</u>, 
Knuth introduces a tool for exploring concepts in graph theory: the five-letter
words. This is a collection of 5,757 five-letter words compiled by Knuth
and useful in exploring ways of constructing efficient algorithms.

The word list is large enough that an $O(N^2)$ algorithm will take a solid
chunk of CPU time, so there's a definite incentive to think carefully about
implementation.

Knuth introduces a list of five-letter words, as well as associated exercises
utilizing techniques from dynamic programming and graph theory, among other 
topics.

We have covered this topic before in prior blog posts:

- [Five Letter Words: Part 1: Getting Familiar With The List](https://charlesreid1.github.io/five-letter-words-part-1-getting-familiar-with-the-list.html)
- [Five Letter Words: Part 2: More Five-Word Algorithms](https://charlesreid1.github.io/five-letter-words-part-2-more-five-word-algorithms.html)
- [Five Letter Words: Part 3: Letter Coverage and Dynamic Programming](https://charlesreid1.github.io/five-letter-words-part-3-letter-coverage-and-dynamic-programming.html)

and a recent addendum to Part 1:

- [Five Letter Words: Part 4: Revisiting Diff by One](https://charlesreid1.github.io/five-letter-words-part-4-revisiting-diff-by-one.html)

We continue our coverage in this blog post with a newer problem,
one that is rated by Knuth at 26, on his scale of 0 to 50:

```plain
00  Immediate
10  Simple (1 minute)
20  Medium (quarter hour)
30  Moderately hard
40  Term project
50  Research problem
```

(from Volume 1, Notes on the Exercises.)

Here's the [list of words](https://github.com/charlesreid1/five-letter-words/blob/master/sgb-words.txt)
if you want to play along.

Link to the [Stanford Graph Base](http://www3.cs.stonybrook.edu/~algorith/implement/graphbase/implement.shtml).

Visit [Five Letter Words](https://charlesreid1.com/wiki/Five_Letter_Words)
on the charlesreid1.com wiki for details.

## Introduction to the Try Trie Tree Problem

In this blog post, we'll cover Exercise 35 of Volume 4, Fascicle 
of Donald Knuth's <u>Art of Computer Programming</u>.

The problem is as follows:

> Sixteen well-chosen elements of `WORDS(1000)` lead to the 
> branching pattern (figure), which is a complete binary 
> trie of words that begin with the letter `s`.
> But there's no such pattern of words beginning with `a`,
> even if we consider the full collection `WORDS(5757)`.
>
> What letters of the alphabet can be used as the starting
> letter of sixteen words that form a complete binary trie
> within `WORDS(n)`, given n?

For the benefit of those without the book, here is an attempt
to represent the trie that Knuth includes in the exercise:

```plain
                     s

            h                 t

        e       o         a       e

      e   l   r   w     l   r   a   e

      sheep             stalk
      sheet             stall
                             
          shelf             stars
          shell             start
                             
              shore             steal
              short             steam
                             
                  shown             steel
                  shows             steep
```

To answer the question, of whether a complete binary
trie can be completed for a given letter, given a
set of n words, we construct a "try trie tree,"
which is a tree data structure that greedily builds
a trie with as many branches as possible.

The full trie of $26^4+1 = 456,977$ nodes
would be expensive to assemble in full, for each
starting letter. Instead we use the word list 
to build up a tree of possible candidate branches
for the trie. Once we've constructed all possible
branches using the faster but less precise method,
we verify that each candidate branch we have
constructed either meets our criteria (can be
included as a branch in a complete binary trie),
or is pruned.

## The Try Trie Tree

To solve this problem, we define a TryTrieTree
class that holds the nodes and links that make
up our tree. We define some methods for it
to perform the assembly and verification operations
described below, then assemble one try trie tree
for each letter of the alphabet to come up with 
an answer to the exercise.


## Constructing the Try Trie Tree

The construction procedure for the try trie tree
is top-down.

We construct the trie starting at the root (the 
starting letter) and go level by level.

### Checking for Minimum Number of Matching Words

At each level of the trie, we count
the number of words in `WORDS(n)` whose prefix 
matches the prefix at that trie location.
If enough words match, that branch of the trie
is possibly (but not definitely) complete.

**Example:** If we are attempting to assemble
a complete trie for the letter `z` using `WORDS(1000)`,
we can stop at the very first level, because 
we already know there are not enough words 
starting with the letter z to make a complete
binary trie. (If a complete binary trie requires
16 words, and only 10 start with z, we don't need
to go any further.)

**Example:** If we are assembling the complete
trie for `s` given by the author in the exercise,
we can verify that there are at least 16 words that
begin with the letter `s`. We would then verify that
there are at least 8 words that begin with `sa`,
which there are. Then we would verify that there
are at least 4 words that begin with `saa`, which
there are not, so we would move on to verifying
that there are at least 4 words that begin with
`sab`, which there are. We would proceed in this
fashion until we had assembled a candidate trie
branch, `s-a-b-r` (which contains two words,
`sabra` and `sabre`). So far, so good.

At each level of the trie, we apply the procedure:
- At level 1, we require a minimum of $2^{5-1} = 16$ words.
- At level 2, we require a minimum of $2^{5-2} = 8$ words.
- At level 3, we require a minimum of $2^{5-3} = 4$ words.
- At level 4, we require a minimum of $2^{5-4} = 2$ words.

**NOTE:** We are not explicitly constructing the trie,
so we don't need to assemble the word leaves.

### Assemble Method

See the [Try Trie Tree Code](#try-trie-tree-code) section 
for the code for the public and private assembly methods.

To peform the assembly of all possible branches of the
try trie, we use the `assemble()` method. This is a 
public method that initializes a call to a private
recursive assembly method.

We explore every possible prefix starting with the
root letter, so "sa", "sb", "sc", "sd", and so on.
Within each of those, we try each letter another 
level further, "saa", "sab", and so on, and then
we try each letter in a final step, for a total
of $26^4 = 456,976$ iterations (checks for existence
of words starting with a given substring).

**NOTE:** If we want to speed up our program,
we would be wise to start by speeding up
the way we check the number of words that
start with a given substring.

The recursive assembly method therefore takes
a prefix string (location in the tree), and
explores each possible child in the trie,
counting how many words occur at that possible
child. If enough of them exist, the branch
is added to the TryTrieTree.

### Verifying Branches and Bubbling Up Counts

However, the above counts are just the _minimum_ required,
and do not guarantee that a trie branch can be used in
a complete binary trie. That requires checking the entire
trie. We will end up pruning some of the branches of the
try trie we assembled above.

Continuing with the example above for `s`, we
assembled the branch `s-a-b-r`, which contains
the minimum two words required. However, `s-a-b`
is not a common enough prefix! The only child
of `s-a-b` with two or more words matching
is `s-a-b-r`, which means we can't form a complete
binary trie using this `s-a-b` branch.

Importantly, this procedure is _bottom-up_.

We perform a pre-traversal depth-first search
of the entire tree, ensuring that we visit
each of the leaves of the tree _first_, and
to ensure that we have always visited every child
of a node before we visit the node itself.

This is important because we will "bubble up"
the count of valid branches. 

In our TryTrieTree, a complete binary trie is 
only possible if each node at each level has
_two or more_ children that are "large enough",
where "large enough" means that either (a) both child
nodes have _two or more_ children that are
"large enough", or (b) if we are at a leaf node
(representing 4 characters), and there are
_two or more_ words that begin with the 4 characters
corresponding to this trie node.

### Bubble Up Method

See the [Try Trie Tree Code](#try-trie-tree-code) section 
for the code for the public and private bubble up methods.

Similar to the assembly method, our bubble up method
is also a recursive method, performing a depth-first
pre-order traversal. This ensures we reach leaf nodes
before beginning our task, and that counts proceed
from bottom-up.

## Try Trie Tree Code

### Try Trie Trie Class

Before we define the TryTrieTree class,
we start with a utility tree node class:

```python
class Node(object):
    def __init__(self, letter, count=0):
        self.letter = letter
        self.count = count
        self.children = []
        self.parent = None
```

The TryTrieTree class has a constructor that 
initializes the root node to None. The tree
should also contain a pointer to the original
word set, so that we can reference it in later
methods where needed.

```python
class TryTrieTree(object):
    def __init__(self,words):
        self.root = None
        self.words = words
```

In the final class we defined a `__str__()`
method to create a string representation
of the TryTrieTree, but we will skip that
for now.

Next we have a method to set the root to
a given Node:

```python
    def set_root(self,root_letter):
        self.root = Node(root_letter)
```

Additionally, we have two utility methods that 
help us navigate between locations in the tree 
and the corresponding string prefixes:

- `get_prefix_from_node()` (utility method): given a
  Node in the trie, return the string prefix that would
  lead to that Node.

- `get_node_from_prefix()` (utility method): given a
  string prefix, return the Node in the trie that 
  corresponds to the given string prefix.
  Return None if no such Node exists.

These methods are given below:

```python
    def get_prefix_from_node(self,node):
        """Given a node in the trie,
        return the string prefix that
        would lead to that node.
        """
        if node==None:
            return ""
        elif node==self.root:
            return ""
        else:
            prefix = ""
            while node.parent != None:
                node = node.parent
                prefix = node.letter + prefix
            return prefix
```

and the reverse:

```python
    def get_node_from_prefix(self,prefix):
        """Given a string prefix,
        return the node that represents
        the tail end of that sequence
        of letters in this trie. Return
        None if the path does not exist.
        """
        assert self.root!=None

        if prefix=='':
            return None

        assert prefix[0]==self.root.letter

        # Base case
        if len(prefix)==1:
            return self.root

        # Recursive case
        parent_prefix, suffix = prefix[:len(prefix)-1],prefix[len(prefix)-1]
        parent = self.get_node_from_prefix(parent_prefix)
        for child in parent.children:
            if child.letter == suffix:
                return child

        # We know this will end because we handle
        # the base case of prefix="", and prefix
        # is cut down by one letter each iteration.
```

### Code for Assembling the Tree

We assemble the tree using a private recursive
method. Here is how that looks (again, these
methods are defined on the `TryTrieTree`
class):

```python
    def assemble(self):
        """Assemble the trie from the set of words
        passed to the constructor.
        """
        assert self.root!=None

        words = self.words

        # start with an empty prefix
        prefix = ''
        candidate = self.root.letter
        self._assemble(prefix,candidate,words)
```

In the private recursive method, we assemble the branches
of the tree, only checking to make sure each branch has
the minimum number of words required. In a later method

```python
    def _assemble(self,prefix,candidate,words):
        """Recursive private method called by assemble().
        """
        prefix_depth = len(prefix)
        candidate_depth = prefix_depth+1

        ppc = prefix+candidate
        words_with_candidate = [w for w in words if w[:candidate_depth]==ppc]

        min_branches_req = int(math.pow(2,5-candidate_depth))
        max_number_branches = len(words_with_candidate)

        # If we exceed the minimum number of 
        # branches required, add candidate
        # as a new node on the trie.
        if max_number_branches >= min_branches_req:

            parent = self.get_node_from_prefix(prefix)
            
            # If we are looking at the root node,
            if prefix=='':
                # parent will be None.
                # In this case don't worry about
                # creating new child or introducing
                # parent and child, b/c the "new child"
                # is the root (already exists).
                pass

            else:
                # Otherwise, create the new child,
                # and introduce the parent & child.
                new_child = Node(candidate)
                new_child.parent = parent
                parent.children.append(new_child)

            # Base case
            if candidate_depth==4:
                new_child.count = max_number_branches
                return

            # Recursive case
            for new_candidate in ALPHABET:
                new_prefix = prefix + candidate
                self._assemble(new_prefix,new_candidate,words_with_candidate)

        # otherwise, we don't have enough
        # branches to continue downward,
        # so stop here and do nothing.
        return
```

### Code for Bubbling Up Large Children Counts

These are a little shorter and simpler than the
assembly method above:

```python
    def bubble_up(self):
        """Do a depth-first traversal of the
        entire trytrietree, pruning as we go.
        This is a pre-order traversal,
        meaning we traverse children first,
        then the parents, so we always 
        know the counts of children
        (or we are on a leaf node).
        """
        self._bubble_up(self.root)


    def _bubble_up(self,node):
        """Pre-order depth-first traversal
        starting at the leaf nodes and proceeding
        upwards.
        """
        if len(node.children)==0:
            # Base case
            # Leaf nodes already have counts          
            # Do nothing
            return

        else:
            # Recursive case
            # Pre-order traversal: visit/bubble up children first
            for child in node.children:
                self._bubble_up(child)

            # Now that we've completed leaf node counts, we can do interior node counts.
            # Interior node counts are equal to number of large (>=2) children.
            large_children = [child for child in node.children if child.count >= 2]
            node.count = len(large_children)
```

You can see how we converted the definition of
"large children" into a rule above - we use the
recursive case of the "large children" definition
in the recursive case, and we use the base case
of the "large children definition" (for leaf nodes)
when we are on the base case.

Also note that each leaf node was initialized with
the number of words that start with the corresponding
4-letter prefix (that was done in the assembly method),
but we could just as easily do it in the base case,
as the leaf nodes are the base case.


## Wrap it in a Bow

We can add some extra wrapping around our class,
and call each of the methods in order for the
various letters of the alphabet.

Below, we process an input argument n (which is
the size of the wordlist, 5757, if the user does
not specify n). It then creates a TryTrieTree
for each letter, and determines if a complete
binary trie can be constructed. Finally, it prints
a summary of the results.

```python
#!/usr/bin/env python
from get_words import get_words
import sys
import math

"""
tries.py

Donald Knuth, Art of Computer Programming, Volume 4 Fascicle 0
Exercise #35

Problem:
What letters of the alphabet can be used
as the starting letter of sixteen words that
form a complete binary trie within
WORDS(n), given n?
"""

ALPHABET = "abcdefghijklmnopqrstuvwxyz"
FIVE = 5


class Node(object):
    ...


class TryTrieTree(object):
    ...

def trie_search(n, verbose=False):

    words = get_words()
    words = words[:n]

    perfect_count = 0
    imperfect_count = 0
    for letter in ALPHABET:

        tree = TryTrieTree(words)
        tree.set_root(letter)
        tree.assemble()
        tree.bubble_up()
        #print(tree)

        if tree.root.count >= 2:

            if verbose:
                print("The letter {0:s} has a perfect binary trie in WORDS({1:d}).".format(
                    letter, n))
            perfect_count += 1

        else:

            if verbose:
                print("The letter {0:s} has no perfect binary trie in WORDS({1:d}).".format(
                    letter, n))
            imperfect_count += 1

    if verbose:
        print("")
        print("Perfect count: {:d}".format(perfect_count))
        print("Imperfect count: {:d}".format(imperfect_count))

    return perfect_count, imperfect_count



def trie_table():
    """Compute and print a table of
    number of words n versus number of
    perfect tries formed.
    """
    print("%8s\t%8s"%("n","perfect tries"))

    ns = range(1000,5757,500)
    for n in ns:
        p,i = trie_search(n)
        print("%8d\t%8d"%(n,p))

    n = 5757
    p,i = trie_search(n)
    print("%8d\t%8d"%(n,p))


if __name__=="__main__":
    if len(sys.argv)<2:
        n = 5757
    else:
        n = int(sys.argv[1])
        if n > 5757:
            n = 5757

    _,_ = trie_search(n, verbose=True)

    #trie_table()
```

## Output

When we run with n = 1000, we can see that `s` is the only letter
that forms a perfect binary trie for that value of n:

```plain
$ python tries.py 1000
The letter a has no perfect binary trie in WORDS(1000).
The letter b has no perfect binary trie in WORDS(1000).
The letter c has no perfect binary trie in WORDS(1000).
The letter d has no perfect binary trie in WORDS(1000).
The letter e has no perfect binary trie in WORDS(1000).
The letter f has no perfect binary trie in WORDS(1000).
The letter g has no perfect binary trie in WORDS(1000).
The letter h has no perfect binary trie in WORDS(1000).
The letter i has no perfect binary trie in WORDS(1000).
The letter j has no perfect binary trie in WORDS(1000).
The letter k has no perfect binary trie in WORDS(1000).
The letter l has no perfect binary trie in WORDS(1000).
The letter m has no perfect binary trie in WORDS(1000).
The letter n has no perfect binary trie in WORDS(1000).
The letter o has no perfect binary trie in WORDS(1000).
The letter p has no perfect binary trie in WORDS(1000).
The letter q has no perfect binary trie in WORDS(1000).
The letter r has no perfect binary trie in WORDS(1000).
The letter s has a perfect binary trie in WORDS(1000).
The letter t has no perfect binary trie in WORDS(1000).
The letter u has no perfect binary trie in WORDS(1000).
The letter v has no perfect binary trie in WORDS(1000).
The letter w has no perfect binary trie in WORDS(1000).
The letter x has no perfect binary trie in WORDS(1000).
The letter y has no perfect binary trie in WORDS(1000).
The letter z has no perfect binary trie in WORDS(1000).

Perfect count: 1
Imperfect count: 25
```

In fact, 978 is the smallest number of words to find any perfect tries:

```
$ python tries.py 978
The letter a has no perfect binary trie in WORDS(978).
The letter b has no perfect binary trie in WORDS(978).
The letter c has no perfect binary trie in WORDS(978).
The letter d has no perfect binary trie in WORDS(978).
The letter e has no perfect binary trie in WORDS(978).
The letter f has no perfect binary trie in WORDS(978).
The letter g has no perfect binary trie in WORDS(978).
The letter h has no perfect binary trie in WORDS(978).
The letter i has no perfect binary trie in WORDS(978).
The letter j has no perfect binary trie in WORDS(978).
The letter k has no perfect binary trie in WORDS(978).
The letter l has no perfect binary trie in WORDS(978).
The letter m has no perfect binary trie in WORDS(978).
The letter n has no perfect binary trie in WORDS(978).
The letter o has no perfect binary trie in WORDS(978).
The letter p has no perfect binary trie in WORDS(978).
The letter q has no perfect binary trie in WORDS(978).
The letter r has no perfect binary trie in WORDS(978).
The letter s has a perfect binary trie in WORDS(978).
The letter t has no perfect binary trie in WORDS(978).
The letter u has no perfect binary trie in WORDS(978).
The letter v has no perfect binary trie in WORDS(978).
The letter w has no perfect binary trie in WORDS(978).
The letter x has no perfect binary trie in WORDS(978).
The letter y has no perfect binary trie in WORDS(978).
The letter z has no perfect binary trie in WORDS(978).

Perfect count: 1
Imperfect count: 25
```

Running with the full 5757 words leads to 11 more perfect tries:

```plain
$ python tries.py 5757
The letter a has no perfect binary trie in WORDS(5757).
The letter b has a perfect binary trie in WORDS(5757).
The letter c has a perfect binary trie in WORDS(5757).
The letter d has a perfect binary trie in WORDS(5757).
The letter e has no perfect binary trie in WORDS(5757).
The letter f has a perfect binary trie in WORDS(5757).
The letter g has no perfect binary trie in WORDS(5757).
The letter h has a perfect binary trie in WORDS(5757).
The letter i has no perfect binary trie in WORDS(5757).
The letter j has no perfect binary trie in WORDS(5757).
The letter k has no perfect binary trie in WORDS(5757).
The letter l has a perfect binary trie in WORDS(5757).
The letter m has a perfect binary trie in WORDS(5757).
The letter n has no perfect binary trie in WORDS(5757).
The letter o has no perfect binary trie in WORDS(5757).
The letter p has a perfect binary trie in WORDS(5757).
The letter q has no perfect binary trie in WORDS(5757).
The letter r has a perfect binary trie in WORDS(5757).
The letter s has a perfect binary trie in WORDS(5757).
The letter t has a perfect binary trie in WORDS(5757).
The letter u has no perfect binary trie in WORDS(5757).
The letter v has no perfect binary trie in WORDS(5757).
The letter w has a perfect binary trie in WORDS(5757).
The letter x has no perfect binary trie in WORDS(5757).
The letter y has no perfect binary trie in WORDS(5757).
The letter z has no perfect binary trie in WORDS(5757).

Perfect count: 12
Imperfect count: 14
```

If we assemble a table of number of five letter words n
versus number of perfect tries formed, nearly half show up
only after we include 4,500 words.

```
       n	perfect tries
    1000	       1
    1500	       1
    2000	       1
    2500	       1
    3000	       3
    3500	       3
    4000	       4
    4500	       6
    5000	      11
    5500	      12
    5757	      12
```

