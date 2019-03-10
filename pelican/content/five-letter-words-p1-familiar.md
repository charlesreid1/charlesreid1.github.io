Title: Five Letter Words: Part 1: Getting Familiar With The List
Date: 2017-09-01 21:00
Category: Computer Science
Tags: python, computer science, graphs, algorithms, art of computer programming, knuth, five letter words

_NOTE: The code covered in this post uses Python 3. The scripts can be converted to Python 2 with minimal effort,
but the author would encourage any user of Python 2 to "put on your big kid pants" and 
make the switch to Python 3. Let's all make this painful, drawn-out switch from Python 2 
to Python 3 a thing of the past, shall we?_

## Table of Contents

* [About the Five Letter Words](#five1-about)
* [The Usefulness of Five Letter Words](#five1-usefulness)
* [Warm-Up Exercises](#five1-warmup)
* [Get Words Function](#five1-get)
* [Euclidean Distance](#five1-euclidean)
	* [Euclidean Distance Code](#five1-euclidean-code)
	* [Examples](#five1-euclidean-examples)
	* [Different-by-N Code](#five1-euclidean-n)
* [Mo Words, Mo Problems](#five1-moproblems)
* [References](#five1-refs)

<a name="five1-about"></a>
## About the Five-Letter Words

In Volume 4, Facsimile 0 of Donald Knuth's <u>Art of Computer Programming</u>, 
in which Knuth covers graph theory, he introduces a list of five-letter words
as part of a data set useful in exploring graph theory and graph algorithms.

The [list of words](https://github.com/charlesreid1/five-letter-words/blob/master/sgb-words.txt) 
is part of the [Stanford Graph Base](http://www3.cs.stonybrook.edu/~algorith/implement/graphbase/implement.shtml), 
a set of data sets that are useful for studying graph theory and networks.

The first few words in the list are:

* which
* there
* their
* about
* would
* these
* other
* words
* could
* write
* first
* water
* after

and so on. There are 5,757 total words in the data set, including some common words
(as the first few listed), as well as some less common words:

* osier
* roble
* rumba
* biffy
* pupal

This post is an introduction to the five letter words, and will give a few 
useful algorithms for analyzing the set of words. 

<a name="five1-usefulness"></a>
## The Usefulness of Five Letter Words

We are surrounded, always and everywhere, by language - the principal mechanism of 
thought, communication, and expression. Our latent familiarity with language 
makes data sets involving language extremely useful - unlike a data set about 
football scores, property crime, or human fatalities, we don't expend
much effort understanding the nature of the data. Studying language also gives us 
a deeper understanding and appreciation for the complexity of language, for through
our very familiarity with language, it can come to seem deceptively simple.

Five letter words, in particular, are short enough that they are familiar, 
and surround us, and yet long enough to have variety and lead to some 
very interesting properties. Five also happens to be a computationally 
convenient length.

<a name="five1-warmup"></a>
## Warm-Up Exercises

In Knuth's AOCP, he presents the reader with several warm-up exercises to 
get familiar with the list of words. We cover solutions to several of these 
exercises. Many of these exercises are creating algorithms that, while not 
utilizing graph theory themselves, can be utilized to construct interesting 
graphs. These exercises are written in Python.

Let us begin.

<a name="five1-get"></a>
## Get Words Function

Before starting any analysis of the five letter words, it is a good idea to 
create a function that will load the data set form a text file and load the result
as a Python list. This function is given below:

[get_words.py](https://github.com/charlesreid1/five-letter-words/blob/master/get_words.py)

```
"""
get_words.py

Utility method to load the SBG words
and retun them as a list of strings.
"""

def get_words():
    # Load the file.
    with open('sgb-words.txt','r') as f:
        ## This includes \n at the end of each line:
        #words = f.readlines()
    
        # This drops the \n at the end of each line:
        words = f.read().splitlines()

    return words
```

This is a straightforward use of the `read()` and `splitlines()` functions in Python.

<a name="five1-euclidean"></a>
## Euclidean Distance

We begin with a calculation of the Eulcidean distance between words.
We define the distance between two words, commonly called the "edit distance,"
based on the notion of a unit change, which is incrementing or decrementing a letter 
by one. Thus, the edit distance between "a" and "b" is 1, the edit distance 
between "e" and "g" is 2, and so on.

<a name="five1-euclidean-code"></a>
### Euclidean Distance Code

Let's start with the code that does the calculation of the edit distance between
two words:

[euclidean_distance.py](https://github.com/charlesreid1/five-letter-words/blob/master/euclidean_distance.py)

```
import random, math, operator
from pprint import pprint
from get_words import get_words

random.seed(1337)

"""
euclidean_dist.py

Compute euclidean distance between 5-letter words.
"""

def euclidean_distance(word1, word2):
    v1 = word2vec(word1)
    v2 = word2vec(word2)
    return l2norm(v1,v2)

def l2norm(vec1, vec2):
    radicand = [(v2-v1)*(v2-v1) for (v1,v2) in zip(vec1,vec2)]
    return math.sqrt(sum(radicand))

def word2vec(word):
    charvec = []
    vec = []
    for c in word:
        charvec.append(c)
        vec.append(ord(c)-ord('a'))
    return vec

def print_tuple(e):
    print("Distance between {0:s} and {1:s} = {2:f}".format(*e))

if __name__=="__main__":

    words = get_words()

    eds = []
    for i in range(100):
        w1 = words[random.randint(1,5757)]
        w2 = words[random.randint(1,5757)]
        ed = euclidean_distance(w1,w2)
        eds.append((w1,w2,ed))

    sorted_eds = sorted(eds, key=operator.itemgetter(2))

    for e in reversed(sorted_eds):
        print_tuple(e)
```

Note that this script shares much in common with codes to create 
Caesar ciphers, Affine ciphers, and the like - the heart of the script is 
the `word2vec()` function, which converts a five-letter word into a five-component
vector of numbers from 0 to 25. This is done using Python's `ord()` function,
which returns the *ordinal* value of a character. The letter 'a' is 0, 'b' is 1, 'c' is 2,
and so on.

The code also implements an L2 norm calculation, which is the mathematical
term for a Euclidean distance calculation. It computes the square root of the 
sum of the squares of the differences between each component of the vector.
This is the standard distance formula from your high school algebra class,
extended to higher dimensions:

$$
d = \sqrt{ (x_2 - x_1)^2 + (y_2 - y_1)^2}
$$

Or, for the physicists out there, the dot product of two vectors.
The L2 norm between two vectors $\mathbf{v}_1$ and $\mathbf{v}_2$ is 
commonly denoted:

$$
|| \mathbf{v}_2 - \mathbf{v}_1 ||_2
$$

<a name="five1-euclidean-examples"></a>
### Examples

To better illustrate what the Euclidean distance calculation looks like,
let's look at some concrete examples of words that have an edit distance of 1:

```
there, these
right, sight
sound, round
might, night
might, light
along, among
```

In each case, we increment or decrement a single letter by 1, 
and the result is another five-letter word in the list.
Perhaps the most surprising result is how *many* pairs of 
common words have an edit distance of 1:

```
$ python diff_by_one.py
1075 words have a Euclidean distance of +/-1.
```

That means nearly 20% of the words are within a single edit
of another word.



If we look at words that have an edit distance of more than 1,
we can see that some pairs of words have a single letter that changes 
by 2 units, while other pairs have two letters that differ by a single 
unit: 

```
would, wound
right, tight
years, wears
never, lever
along, alone
night, light
paper, oboes
```

The last pair is an example of the latter. 

Here are more examples of pairs of words with larger edit distances:

```
----------------------------------------
Distance of 3
there, where
would, world
words, woods
sound, pound
those, whose
house, horse
----------------------------------------
Distance of 4
about, cents
after, birds
right, night
think, thing
sound, wound
small, smell
----------------------------------------
Distance of 5
which, weigh
there, theme
other, steer
right, might
years, tears
place, space
place, piece
```

<a name="five1-euclidean-n"></a>
### Different-by-N Code

_**IMPORTANT NOTE:** On 2019-03-09 we revisited the problem set and solution,
and discovered that we had misinterpreted the (much more interesting) original
problem posed by Knuth. Ths will be rectified in a follow-up blog post!_

_Briefly, the mistake we made here was to interpret this problem as asking for
pairs of words "different by +/-1" to mean, find pairs with a total Hamming
distance (or Euclidean distance) of exactly +/-1 total. This would produce
pairs like "might" and "night"._

_In fact, the problem Knuth posed asks for pairs of words
in the SGB that are "different by +/-1 **at each position,**"
meaning each letter must be different by one and exactly one.
An example of such a pair would be "rover" and "spuds"._

The code that performs the above calculations includes 
`diff_by_one.py` and `diff_by_n.py`. Here is the former:

diff_by_one.py

```
"""
diff_by_one.py

Donald Knuth, Art of Computer Programming, Volume 4 Facsimile 0
Exercise #28

Find pairs of SGB word vectors that differ by +/-1.

(See IMPORTANT NOTE here: https://charlesreid1.github.io/five-letter-words-part-1-getting-familiar-with-the-list.html)
"""
from get_words import get_words
from euclidean_distance import euclidean_distance

if __name__=="__main__":
    words = get_words()

	## To limit the output:
    #words = words[:1000]

    k = 0
    off_by_one = []
    for i in range(len(words)):
        for j in range(i,len(words)):
            d = euclidean_distance(words[i],words[j])
            if(abs(d)==1):
                k += 1
                off_by_one.append((words[i],words[j]))
                print("{0:s}, {1:s}".format(words[i],words[j]))

    print("{0:d} words have a Euclidean distance of +/-1.".format(k))
```

This is a nested for loop that examines all pairs of words. Note that 
we want to avoid the pair (B,A) if we have already found/printed the pair 
(A,B), so we use a nested for loop where the inner index starts at the 
outer index. The core of the script is the `euclidean_distance()` function,
covered above.

This algorithm takes $O(N^2)$ time due to the nested for loops.

Likewise, here is code to generate pairs that differ by some amount $n$.
This code will only print 10 pairs for each $n$, to cut down on running time.

diff_by_n.py

```
"""
diff_by_n.py

Donald Knuth, Art of Computer Programming, Volume 4 Facsimile 0
Variation on Exercise #28

Find pairs of SGB word vectors that differ by +/-n.

(See IMPORTANT NOTE here: https://charlesreid1.github.io/five-letter-words-part-1-getting-familiar-with-the-list.html)
"""
from get_words import get_words
from euclidean_distance import euclidean_distance

def diff_by_n(n):
    k = 0
    off_by_one = []
    for i in range(len(words)):
        for j in range(i,len(words)):
            d = euclidean_distance(words[i],words[j])
            if(abs(d)==n):
                k += 1
                off_by_one.append((words[i],words[j]))
                print("{0:s}, {1:s}".format(words[i],words[j]))
        if k>10:
            break

    print("{0:d} words have a Euclidean distance of +/-{0:d}.".format(k,n))


if __name__=="__main__":
    words = get_words()

    for n in [2,3,4,5]:
        print("-"*40)
        print("Distance of {0:d}".format(n))
        diff_by_n(n)
```

<a name="five1-moproblems"></a>
## Mo Words, Mo Problems

We have a number of other interesting problems and codes to cover, including:

* Palindromes
* Number of unique words
* Word/letter statistics 
* Words consisting of lexicographically sorted letters
* Words consisting of distinct letters

Each of these will be covered in a series of posts to follow.
Then we'll move on to the business of graph theory, implementation of 
these five letter words as graphs, and utilization of software libraries 
designed for graphs and networks (expect some code in Java using Google's
excellent Guava library).

You can follow all of this in my [five-letter-words](https://github.com/charlesreid1/five-letter-words) 
repository on Github, and/or in the [five-letter-words](https://git.charlesreid1.com/cs/five-letter-words) 
repository on git.charlesreid1.com.

We have also provided additional information on the charlesreid1 wiki,
at [Five Letter Words](http://charlesreid1.com/wiki/Five_Letter_Words),
along with a whole bundle of notes from working through Donald Knuth's 
<u>Art of Computer Programming</u> at the [Art of Computer Programming](https://charlesreid1.com/wiki/AOCP)
page of the wiki.

Expect more soon!

<a name="five1-refs"></a>
## References

1. Knuth, Donald. <u>The Art of Computer Programming</u>. Upper Saddle River, NJ: Addison-Wesley, 2008.

2. Knuth, Donald. <u>The Stanford GraphBase: A Platform for Combinatorial Computing</u>. New York: ACM Press, 1994. 
<[http://www-cs-faculty.stanford.edu/~knuth/sgb.html](http://www-cs-faculty.stanford.edu/~knuth/sgb.html)>

3. "Five Letter Words." Git repository, git.charlesreid1.com. Charles Reid. Updated 1 September 2017.
<[http://git.charlesreid1.com/cs/five-letter-words](http://git.charlesreid1.com/cs/five-letter-words)>

