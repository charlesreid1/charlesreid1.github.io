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
proceeds in two steps:

Step 1 is to assemble a tree, from the top down,
by searching the entire space of $456,977$ nodes
and marking particular nodes and paths on this tree
as candidates for the final perfect binary trie.

Step 2 is to revisit the candidate branches,
proceeding from the bottom up, and determine
if the candidate branches do, in fact, have
enough sibling nodes and word matches to form
a complete branch in a perfect binary trie.

We start Step 1 at the root node (the starting
letter) and proceed from the root down, going
level by level.


### Checking for Minimum Number of Matching Words

Step 1 proceeds from the top down and marks
branches that are candidates to end up in the
final perfect binary trie.

At each level of the trie, we count
the number of words in the overall word set 
that have a prefix matching the prefix
corresponding to that node.

For example, the trie node `b` on the path
`s-a-b` would yield four words:

```
saber
sable
sabre
sabra
```

If enough words match, that branch of the trie
is a possible candidate to end up in the perfect
binary trie (but may be trimmed in Step 2).

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
`sabra` and `sabre`). For Step 1, we keep `s-a-b-r`
as a candidate branch. (We will see in Step 2
that this branch will get trimmed.)

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
public method that starts a recursive call to a private
method `_assemble()`.

We are given a starting letter (in the example given
by the author, the starting letter is "s").
We explore every possible prefix that starts with the
root letter, "sa", "sb", "sc", "sd", and so on.

For each of those possible prefixes, we explore every possible
third letter, "saa", "sab", and so on, and then once more
in a fourth step, "saaa", "saab", ..., for a total of 
$26^4 = 456,976$ iterations (checks for existence
of words starting with a given substring).

A substantial number of these checks will do nothing - 
from the fact that

$\frac{5757}{456976} \sim 5e3/5e5 \sim 0.01$ 

we know that the maximum number of loops that would actually
lead to a branch being added will be 1% of that $26^4$ total.

We also know that any efforts to speed up this program
should focus on the way we are checking the number of
words that start with a given substring - since that's
where we'll spend most of our time.

The recursive assembly method takes a prefix string input
(which maps to a location in the tree), and it explores
all 26 possible children of that prefix (location in the trie).

When a leaf node is reached, at the fourth level, it represents
the longest prefix in our trie. This is the base case of the
recursive assembly function; the recursive function terminates
at a fixed depth of 4.


### Verifying Branches and Bubbling Up Counts

However, as we noted, the counts we are using above in Step 1
are just approximations (checking there are a _minimum_ number of
words with a given prefix). There is no way to guarantee that a 
trie branch can be used in the final complete perfect binary trie
until all child leaf nodes have been visited.

This is where Step 2 comes in. In Step 2 we perform a pre-order
depth-first traversal of the tree, visiting the leaf nodes first
and proceeding from the bottom up. The number of words matching
the prefix of each leaf node must be 2, to keep the leaf node.

We then proceed up the tree, level by level, and at each level
we require that each node have at least 2 "large" children.
This is a recursive definition - for a child to be "large", it
must itself have 2 "large" children, or (if it is a leaf node)
it must have at least 2 words that match the 4-letter prefix.

In our TryTrieTree, a complete binary trie is 
only possible if each node at each level has
_two or more_ children that are "large enough",
where "large enough" means that either (a) both child
nodes have _two or more_ children that are
"large enough", or (b) if we are at a leaf node
(representing 4 characters), and there are
_two or more_ words that begin with the 4 characters
corresponding to this trie node.

Let's go through an example.

Continuing with the example above for `s`, we
assembled the branch `s-a-b-r`, which contains
the minimum two words required. However, `s-a-b`
is not a common enough prefix! The only child
of `s-a-b` with two or more words matching
is `s-a-b-r`, which means we can't form a complete
binary trie using this `s-a-b` branch.

We call this procedure a "bubble up" procedure,
since it is _bottom-up_.

### Bubble Up Method

See the [Try Trie Tree Code](#try-trie-tree-code) section 
for the code for the public and private bubble up methods.

Similar to the assembly method, our bubble up method
is also a recursive method, performing a depth-first
pre-order traversal. This ensures we reach leaf nodes
before beginning our task, and that counts proceed
from bottom-up.

## Try Trie Tree Code

Below we go through some of the code
for the Try Trie Tree problem.

### Try Trie Trie Class

When dealing with trees, it's always a safe bet
that we'll need a Node class, so we start with
a utility class for tree nodes:

```python
class Node(object):
    def __init__(self, letter, count=0):
        self.letter = letter
        self.count = count
        self.children = []
        self.parent = None
```

The TryTrieTree class has a constructor that 
starts with an empty root. The tree
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
and the corresponding string prefixes. These two
methods convert between string prefixes (like
`s-a-b-r`) and locations in the trie (like the
`r` trie node at the end of the path `s-a-b-r`):

- `get_prefix_from_node()` (utility method): given a
  Node in the trie, return the string prefix that would
  lead to that Node.

- `get_node_from_prefix()` (utility method): given a
  string prefix, return the Node in the trie that 
  corresponds to the given string prefix.
  Return None if no such Node exists.

These methods are given below.

First, to convert a particular node location to a string
prefix, we use the parent pointer of each node to traverse
up the tree and assemble the corresponding prefix string
from the path (so that traversing from `b` to `a` to the 
root `s` would yield `sab`):

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

and the reverse, to convert a string prefix
into a location in the trie:

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
the minimum number of words required.

At the start of each assemble method, we whittle the set
of words down to only the words that start with the prefix
for the given node. This trick uses a little extra space
but the payoff is avoiding searching the entire word set
for each node to count the number of words matching a given
prefix. If a node's parent is `s-a-b` and we have already done
the work of filtering all words starting with `sab`, 
there is no need to repeat that work when finding 
and filtering all words that start with `sabr`.

```python
    def _assemble(self,prefix,candidate,words):
        """Recursive private method called by assemble().
        """
        prefix_depth = len(prefix)
        candidate_depth = prefix_depth+1

        ppc = prefix+candidate
        words_with_candidate = [w for w in words if w[:candidate_depth]==ppc]
```

Next lines are the checks to ensure we have the minimum
number of words required to form a candidate branch in
the trie.

If we do, we will create a new child node for that 
branch and recurse by calling assemble on it.

Of course, we have to check for the base case, which in
this scenario checks when we have reached the fixed
trie depth of 4.

```python
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

