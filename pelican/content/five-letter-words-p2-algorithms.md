Title: Five Letter Words: Part 2: More Five-Word Algorithms
Date: 2017-09-01 21:00
Category: Computer Science
Tags: python, computer science, graphs, algorithms, art of computer programming, knuth, language
Status: draft

_NOTE: The code covered in this post uses Python 3. The scripts can be converted to Python 2 with minimal effort,
but the author would encourage any user of Python 2 to "put on your big kid pants" and 
make the switch to Python 3. Let's all make this painful, drawn-out switch from Python 2 
to Python 3 a thing of the past, shall we?_

## Table of Contents

* [Introduction](#five2-intro)
* [Five-Letter Words with k Distinct Letters](#five2-distinct)
	* [Examining a Variation](#five2-variation)
* [Lexicographic Ordering of Letters](#five2-lex)
	* [Five-Letter Words with Lexicographically Ordered Letters](#five2-lexicographic)
	* [Five-Letter Words with Lexicographically Reversed Letters](#five2-rlexicographic)
* [Finding Palindromes](#five2-findpalindromes)
	* [Palindromes](#five2-palindromes)
	* [Palindrome Pairs](#five2-palindromepairs)
	* [Near Palindromes](#five2-nearpalindromes)

<a name="five2-intro"></a>
## Introduction

As mentioned in [Five Letter Words: Part 1](http://charlesreid1.github.io/five-letter-words-part-1-getting-familiar-with-the-list.html),
we covered Donald Knuth's list of five letter words, one of the data sets in the 
[Stanford Graph Base](http://www3.cs.stonybrook.edu/~algorith/implement/graphbase/implement.shtml)
that is covered in greater detail in Knuth's coverage of graph theory in Volume 4, Facsimile 0
of his magnum opus, <u>The Art of Computer Programming</u>.

In the section where Knuth introduces the set of words, he also gives readers 
several exercises to get to know the list of words. This multi-part series of posts
(also see [Five Letter Words: Part 1](http://charlesreid1.github.io/five-letter-words-part-1-getting-familiar-with-the-list.html))
is covering some of the solutions to these exercises, and expanding on them 
to illustrate some of the interesting and surprising properties of this data set.

<a name="five2-distinct"></a>
## Five-Letter Words with k Distinct Letters

In Exercise 27, Knuth asks the reader to make a list of words composed of 
a specific number of distinct letters (1, 2, 3, 4, or 5). 

In the list of five-letter words, there are 0 words composed of a single letter,
4 words with two distinct letters (0.07%), 
163 words with three distinct letters (2.8%), 
1756 words with four distinct letters (30.5%), 
and 3834 words with five distinct letters (66.5%).

Here are a few examples:
* Two distinct letters: mamma, ahhhh, esses, ohhhh
* Three distinct letters: added, seems, sense, level, teeth
* Four distinct letters: which, there, these, where, three
* Five distinct letters: their, about, would, other, words

To find these, we can design an algorithm that does the following:
split each string into characters,
add them to a set data type (a set discards any duplicates), 
and get the size of the set. 
This will give us the number of unique letters in a given word,
and we can use a list of lists to store all words with 
a specified number of unique letters. 

Once again, we're using our `get_words` function,
which we covered in [Part 1](http://charlesreid1.github.io/five-letter-words-part-1-getting-familiar-with-the-list.html).
See [get_words.py](https://github.com/charlesreid1/five-letter-words/blob/master/get_words.py)
for that script.

[distinct.py](https://github.com/charlesreid1/five-letter-words/blob/master/distinct.py)

```
"""
distinct.py

Donald Knuth, Art of Computer Programming, Volume 4 Facsimile 0
Exercise #27

How many SGB words contain exactly k distinct letters, for 1 <= k <= 5?
"""
from pprint import pprint
from get_words import get_words

if __name__=="__main__":
    words = get_words()

    lengths = [[] for i in range(5+1)]

    for word in words:
        k = len(set(word))
        lengths[k].append(word)

    for i in range(1,5+1):
        print("-"*40)
        print("Number of words with {0:d} letters: {1:d}".format(i, len(lengths[i])))
        print(", ".join(lengths[i][0:5]))
```

The principal operation here is the statement that gets the length, k:

```
k = len(set(word))
lengths[k].append(word)
```

The operation of turning a word into a set is $O(M)$, where M is the number of 
letters in the word, and the algorithm performs this operation on each word in sequence,
so overall, the algorithm is $O(N)$, where N is the number of words.

The storage space used by the algorithm is also $O(N)$, since for each word,
the number of distinct letters $k \in \{ 0 \dots 5 \}$.

If we were dealing with a lot of words, and needed to save some space,
we could represent the list of words with $k$ distinct letters using five bit vectors,
where each bit vector represents the words that are composed of $k$ distinct 
letters, and has a length of $N$, the number of words. A 0 would indicate the word is 
not in the set (is not composed of $k$ letters), and a 1 would indicate the opposite.

But here, we keep it simple, since we have a small, known set of words.

<a name="first2-variation"></a>
### Examining a Variation

While that's essentially all there is to this algorithm, 
and it takes all of 10 seconds to come up with the idea,
there are some nuances and some bookkeeping details, 
as there are with the design of any algorithm.

For example, compare the following two approaches;
Approach 1 is used in the program, Approach 2 is a less efficient approach:

```
	# Approach 1:
    for word in words:
        k = len(set(word))
        lengths[k].append(word)


	# Approach 2:
	for k in range(1,5+1):
		if(len(set(word))==k):
			lengths[k].append(word)
```

While these are both $O(N)$ runtime, the latter approach is inefficient:
we loop over each word five times, and each time we perform the same operation
(turning the letters of a word into a set). 

Is there ever a case where we would want an approach like #2?

The short answer is, never.

To give a longer answer, let's consider a case where approach #2 might provide an advantage.
Suppose we were considering a case where $k$ could be larger - 
a list of 15-letter words, for example, so k could be up to 15 - 
and we were only interested in a particular value, or small set of values, of $k$, like 3 and 4.  
Approach 1 would store unnecessary intermediate results (the values of k for all words)
and therefore use extra space, compared with approach #2 where we could change the 
for loop to `for k in [3,4]:`.

Even here, though, approach #2 results in unnecessary work, because approach #1
is still computationally more efficient by looping over the list of words only once,
compared with approach #2, which would loop over the list of words twice.

We may further consider a case where approach #2 would give us an advantage,
and that is the case where we are copying data into the list `lengths`, instead of 
just storing a reference to a string. 
Because we only deal with references in Python, we aren't making copies in the 
code given above. But because strings are immutable, we could conceivably be 
making copies if we stored `word.upper()` instead of `word`.
Approach #2 would use less space, because it only considers the values of k 
that are of interest.

But even here, approach #1 requires only a small modification to wipe out
the space advantage of approach #2: add an if statement before calling the 
append function: `if k in [3,4]`. Now the calculation of turning a word
into a set of characters is performed only once for approach #1, 
and we don't end up storing unnecessary intermediate results.

The take-home lesson: even if the core idea behind an algorithm is
straightforward, there are still many ways to do it better or worse. 

<a name="five2-lex"></a>
## Lexicographic Ordering of Letters

Knuth points out that the word "first" contains letters that occur
in lexicograhpic order. Exercise #30 of [AOCP](https://charlesreid1.com/wiki/AOCP)
Volume 4 Facsimile 0 asks us to find the first and last such word that occurs 
in Knuth's set of five letter words.

To do this, we'll take each word and turn it into a list of characters.
We'll then sort the characters, and turn the sorted list of characters 
back into a string. If the string constructed from sorted characters
equals the original string, we have our word, formed from lexicographically 
ordered letters.

We can also perform the reverse - search for words whose letters are 
in reverse lexicographic order. One such word is "spied". 
Implementing this task requires a bit more care, 
because of the fact that Python 3 returns generators where Python 2 
would return lists, but we can get around this with the `list()` function, 
as we shall see shortly.

<a name="five2-lexicographic"></a>
### Five-Letter Words with Lexicographically Ordered Letters

Exercise 30 asks us to find the first and last word in the set of 
five letter words whose letters occur in sorted lexicographic order.
We begin by sorting all of the words, and we find the first such word
is "abbey", while the last such word is "pssst".

There are 105 total words that fit this description. 
As we might expect, a majority of them begin with 
letters at the beginning of the alphabet:

```
----------------------------------------
ALL lexicographically sorted words:
abbey
abbot
abhor
abort
abuzz
achoo
adder
adept
adios
adopt
aegis
affix
afoot
aglow
ahhhh
allot
allow
alloy
ammos
annoy
beefs
beefy
beeps
beers
beery
befit
begin
begot
bells
belly
below
berry
bills
billy
bitty
blowy
boors
boost
booty
bossy
ceils
cello
cells
```

The full output is here:

[lexico output](https://github.com/charlesreid1/five-letter-words/blob/master/output/lexico)

The code to find these words is given below:

[lexico.py](https://github.com/charlesreid1/five-letter-words/blob/master/lexico.py)

```
"""
lexico.py

Donald Knuth, Art of Computer Programming, Volume 4 Facsimile 0
Exercise #30

Each letter of the word "first" appears in correct lexicographic order.
Find the first and last such words in the SGB words.
"""
from get_words import get_words

def in_sorted_order(word):
    chars = list(word)
    if(str(chars)==str(sorted(chars))):
        return True
    else:
        return False

if __name__=="__main__":

    words = get_words()
    words = sorted(words)

    count = 0
    print("-"*40)
    print("ALL lexicographically sorted words:")
    for word in words:
        if(in_sorted_order(word)):
            print(word)
            count += 1
    print("{0:d} total.".format(count))

    print("-"*40)
    for word in words:
        if(in_sorted_order(word)):
            print("First lexicographically sorted word:")
            print(word)
            break

    words.reverse()

    print("-"*40)
    for word in words:
        if(in_sorted_order(word)):
            print("Last lexicographically sorted word:")
            print(word)
            break
```

The heart of the method here is the `in_sorted_order()` method:
this performs the task, as described above. We take the word 
passed to the function (a string), and turn it into a list 
using the `list()` function. We then turn this list 
back into a string (which is the same as the variable `word`),
and compare it to the _sorted_ list of characters, turned back 
into a string, using the call `str(sorted(chars))`.

If the two match, we have not affected the order of characters
by sorting them in lexicographic (alphabetic) order,
and therefore the original string was in sorted order,
and we return True. Otherwise, we return False.

Here's that method one more time:

```
def in_sorted_order(word):
    chars = list(word)
    if(str(chars)==str(sorted(chars))):
        return True
    else:
        return False
```

<a name="five2-lexicographic"></a>
### Five-Letter Words with Lexicographically Reversed Letters

There are significantly fewer five-letter words whose letters are in 
*reverse* lexicographic order - 37, compared to the 105 in sorted order.
Here is the full list:

```
----------------------------------------
ALL lexicographically reversed words:
mecca
offed
ohhhh
plied
poked
poled
polka
skied
skiff
sniff
soled
solid
sonic
speed
spied
spiff
spoke
spoof
spook
spool
spoon
toked
toned
tonic
treed
tried
troll
unfed
upped
urged
vroom
wheee
wooed
wrong
yoked
yucca
zoned
37 total.
```

The code to do this requires only minor modifications to the original, sorted order code.

To reverse the procedure, we just need to modify the `in_sorted_order()` function
to reverse the sorted list of characters before we reassemble it into a string.
We can feed the output of the call to `sorted()` to the `reversed()` function.
However, in Python 3, this returns a generator object, which is lazy - 
it does not automatically enumerate every character. Unless, of course, 
we force it to.

That's where the call to `list()` comes in handy - by passing a generator 
to `list()`, we force Python to enumerate the output of the reversed, sorted list 
generator. Then we turn the reversed, sorted list into a reversed, sorted string:

```
def in_reverse_sorted_order(word):
    chars = list(word)
    # Note: reversed returns a generator,
    # so we have to pass it to list()
    # to explicitly enumerate the reversed results.
    if(str(chars)==str(list(reversed(sorted(chars))))):
        return True
    else:
        return False
```

Meanwhile, the rest of the script can stay virtually the same.

[reverse_lexico.py](https://github.com/charlesreid1/five-letter-words/blob/master/reverse_lexico.py)

```
"""
reverse_lexico.py

Donald Knuth, Art of Computer Programming, Volume 4 Facsimile 0
Variation on Exercise #30

Each letter of the word "spied" appears in reversed lexicographic order.
Find more words whose letters appear in reverse lexicographic order.
"""
from get_words import get_words

def in_reverse_sorted_order(word):
    chars = list(word)
    # Note: reversed returns a generator, 
    # so we have to pass it to list() 
    # to explicitly enumerate the reversed results.
    if(str(chars)==str(list(reversed(sorted(chars))))):
        return True
    else:
        return False

if __name__=="__main__":

    words = get_words()
    words = sorted(words)

    count = 0
    print("-"*40)
    print("ALL lexicographically reversed words:")
    for word in words:
        if(in_reverse_sorted_order(word)):
            print(word)
            count += 1
    print("{0:d} total.".format(count))

    print("-"*40)
    for word in words:
        if(in_reverse_sorted_order(word)):
            print("First reverse lexicographically sorted word:")
            print(word)
            break

    words.reverse()

    print("-"*40)
    for word in words:
        if(in_reverse_sorted_order(word)):
            print("Last lexicographically sorted word:")
            print(word)
            break
```


<a name="five2-findpalindromes"></a>
## Finding Palindromes

Palindromes are words or sets of words that have a reflective property,
namely, they spell the same thing forward and reverse (e.g., "race car",
or "Ere I was able, I saw Malta", or "Doc, note I dissent - a fast never prevents a fatness. I diet on cod.").

In Exercise 29, Knuth asks the reader to perform a straightforward task - 
find the palindromes in the list of five letter words. (An example of one such
word is "kayak".) But Knuth goes further, and points out that palindromes 
can *also* be formed from pairs of words.  He gives the example "regal lager".
He asks the reader to find all palindrome pairs as well.

When working on these exercises, we became curious about palindromic near-misses.
How many words are *almost* palindromes? (Example: "going" is very close to a 
palindrome, if we just changed the n to an o or vice-versa.)
In fact, we already have all the tools we need at our disposal,
as we already covered a script to perform a Euclidean distance calculation.

We will cover Python code to find words that fit into each of these categories,
and provide some interesting examples. (One of the most surprising things
to us was just how many words meet these criteria!)

<a name="five2-palindromes"></a>
### Palindromes

The first task is finding palindromes in the set of five letter words.
There are 18 such words. They are given below:

* level
* refer
* radar
* madam
* rotor
* civic
* sexes
* solos
* sagas
* kayak
* minim
* tenet
* shahs
* stats
* stets
* kaiak
* finif
* dewed 


<a name="five2-palindromepairs"></a>
### Palindrome Pairs

There are 34 palindromic pairs, if we disallow palindromes from being
considered palindromic pairs with themselves.


<a name="five2-nearpalindromes"></a>
### Near Palindromes






