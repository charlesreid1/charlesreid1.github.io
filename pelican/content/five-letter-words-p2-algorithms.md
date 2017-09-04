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
* [Five-Letter Words with (k) Distinct Letters](#five2-distinct)
* [Lexicographic Ordering of Letters](#five2-lex)
	* [Five-Letter Words with Lexicographically Ordered Letters](#five2-lexicographic)
	* [Five-Letter Words with Lexicographically Reversed Letters](#five2-rlexicographic)

<a name="five2-intro"></a>
## Introduction

As mentioned in [Five Letter Words: Part 1](http://charlesreid1.github.io/five-letter-words-part-1-getting-familiar-with-the-list.html),
we covered Donald Knuth's list of five letter words, one of the data sets in the 
[Stanford Graph Base](http://www3.cs.stonybrook.edu/~algorith/implement/graphbase/implement.shtml)
and covered in greater detail in Knuth's coverage of graph theory in Volume 4, Facsimile 0
of his magnum opus, <u>The Art of Computer Programming</u>.

In the section where Knuth introduces the set of words, he also gives readers 
several exercises to get to know the list of five. This multi-part series of posts
is covering some of the solutions to these exercises, and expanding on them 
to illustrate some of the interesting and surprising properties of this data set.

<a name="five2-distinct"></a>
## Five-Letter Words with (k) Distinct Letters

Suppose we wish to make a list of words composed of a specific number of 
distinct letters. We can write a script that will look for words with a 
specified number of unique letters by splitting each string into characters,
adding them to a set data type (a set will discard any duplicates), 
and finally, counting the number of unique entries in the set.
This will give us the number of unique letters in a given word,
and we can then filter words based on their length to get words
with a specified length.





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








