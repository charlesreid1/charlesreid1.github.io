Title: Five Letter Words: Part 3: Letter Coverage and Dynamic Programming
Date: 2017-09-19 12:00
Category: Computer Science
Tags: dynamic programming, python, computer science, graphs, algorithms, art of computer programming

_NOTE: The code covered in this post uses Python 3. The scripts can be converted to Python 2 with minimal effort,
but the author would encourage any user of Python 2 to "put on your big kid pants" and 
make the switch to Python 3. Let's all make this painful, drawn-out switch from Python 2 
to Python 3 a thing of the past, shall we?_

## Table of Contents

* [Introduction](#five3-intro)
* [A Simple Manual Exmaple](#five3-example)
* [Pseudocode](#five3-pseudocode)
* [Python Code](#five3-python)
* [Output and Timing](#five3-output)


<a name="five3-intro"></a>
## Introduction

The letter/word coverage problem, as presented by Donald Knuth in Volume 4, Facsimile 0 
of his masterpiece <u>Art of Computer Programming</u>, is the problem of finding
the _minimum_ number of words from the collection of five letter words that 
"cover" (are drawn from) the first N letters of the alphabet.

The problem has a couple of variations:

* Provided a set of letters, search for the smallest number of words that cover those particular letters.
* Given an integer $N \leq 26$, search for the smallest number of words that cover the first N letters of the alphabet.
* The same problem as above, but drawing from the first $M$ words of the 5757 total five-letter words.

For the sake of simplicity, we will focus on the simplest problem: considering the first $N$ 
letters of the alphabet, find the shortest sequence of words that will provide coverage of the first 
$N$ letters of the alphabet.

This is an example of a dynamic programming problem: a combinatorics problem that can 
be solved by breaking the overall down into smaller sub-problems, solving the sub-problems, and 
assembling solutions to the sub-problems into an overall problem solution.

The procedure is as follows:

* For each word $w_i$, we begin by assuming this word is the best solution _on its own_. This forms the base case/starting solution.
* Next, examine all prior words $w_j, j<i$, and compare each to using the word $w_i$ by itself.
* For each pair of words, take the union (OR) of the character coverage for word $w_i$ 
and the solution bit vector for word $w_j$ (that is, using the best-covered solution so far 
for word $w_j$)
* Note: for word $w_i$, we need to store one of these unions as the best-covered solution so far for 
word $w_i$, but we aren't sure which one yet.)
* For the given pair of words $w_j$ and $w_i$, we are looking at word $w_j$ and considering the possibility 
of extending that with word $w_i$. Adding $w_i$ to the best solution so far may or may not improve the best solution,
so we need to decide whether to add $w_i$ to the best solution so far.
* Compute the number of letters covered in the union of $w_i$ and the best solution so far (by, e.g., 
summing up the 1s in the bit vector of $w_i$ added to the bit vector representing the best solution so far for word $w_j$)
* Compute the number of words in the best solution so far for word $w_j$, and add one to it (representing the new word $w_i$ being added)
* We are searching for the prior solution for word $w_j$ that will lead to the maximum number of 1s in the bit vector
* We break ties by picking the word $w_j$ that will minimize the number of total words
* Once we find the best word $w_j$, we save the union bit vector for word $w_i$ and word $w_j$ under the 
word $w_i$ combined solution bit vector; we save the length of 1s in the combined solution bit vector; and we save 
the number of words so far in that solution.

Once we have gone through every word, we are ready to find the minimum. Do this by:

* Searching through the solutions for every word, and pick out the one that maximizes the number of 1s in the solution bit vector
(or, rather, that has the correct number of 1s in the bit vector) while also minimizing the total number of words.
* To get the actual sequence of words, rather than just the minimum number of jwords, we need to save the prior word
that leads to the maximum number of 1s in the solution bit vector and minimum number of words, for each word.
Then, at the end, we can backtrack through the words that compose the solution.

This is a bit complicated to explain in words, so we'll give a small example,
then some pseudocode. Then we'll present the actual Python program that accomplishes
this task.

<a name="five3-example"></a>
## A Simple Manual Example

Let's walk through an example manually to illustrate the approach:

Suppose we are considering 2-letter words taken from a 5-letter alphabet _abcde_.
We can represent a given word as a binary string or bit vector: for example,
the two-letter word `aa` would be represented by the bit vector `10000`,
`ab` would be represented by the bit vector `11000`, etc.

Now let's consider a set of words, and step through the algorithm with them.

```
W0 = aa = 10000
W1 = ab = 11000
W2 = bc = 01100
W3 = aa = 10000
W4 = dd = 00010
W5 = de = 00011
W6 = bb = 01000
```

Now, we wish to write a dynamic program that will find the smallest set of 
words such that taking the union of each bit vector for each of the words in 
the set will yield the bit vector `11111`. At each step, we seek the words that will 
maximize the number of 1s in the union of the bit vectors, while minimizing the number
of words. We take the union of the "longest sequence of 1s" bit vector from the 
prior step, plus the bit vector from the current step.

*W0: aa*

Start with word W0: this is the only bit vector, so it sets the starting "largest sequence of 1s" bit vector. 
We wish to maximize "largest sequence of 1s" and minimize number of words.

* only W0 as solution is therefore $10000$. The number of 1s is 1. The number of words is 1. (W0 SOLUTION)

*W1: ab*

Start with word W1: this is the only bit vector, so it sets the starting "largest sequence of 1s" bit vector. 
We wish to maximize "largest sequence of 1s" and minimize number of words.

* only W1 as solution is therefore $11000$. The number of 1s is 2. The number of words is 1. (W1 SOLUTION)
* union of W0 solution and W1 $10000 \bigcup 11000 = 11000$. The number of 1s is 2. The number of words is 2.

*W2: bc*

Next is word W2: the "largest sequence of 1s" bit vector is the union of the prior step's "largest sequence of 1s" bit vector and the current word's bit vector. One option:

* only W2 as solution is $01100$. The number of 1s is 2. The number of words is 1.
* union of W0 solution and W2 $10000 \bigcup 01100 = 11100$. The number of 1s is 3. The number of words is 2. (W2 SOLUTION)
* union of W1 solution and W2 $11000 \bigcup 01100 = 11100$. The number of 1s is 3. The number of words is 2.

*W3: aa*

Next is word W3: the "largest sequence of 1s" bit vector is the union that maximizes the number of 1s and minimizes the number of words. Two options:

* only W3 as solution is $10000$. The number of 1s is 1. The number of words is 1.
* union of W0 solution and W3 $10000 \bigcup 10000 = 10000$. The number of 1s is 1. The number of words is 2.
* union of W1 solution and W3 $11000 \bigcup 10000 = 11000$. The number of 1s is 2. The number of words is 2.
* union of W2 solution and W3 $11100 \bigcup 10000 = 11100$. The number of 1s is 3. The number of words is 3. (W3 SOLUTION)

*W4: dd*

Next is word W4: the "largest sequence of 1s" bit vector is the union that maximizes the number of 1s and minimizes the number of words. Three options:

* only W4 as solution is $00010$. The number of 1s is 1. The number of words is 1.
* union of W0 solution and W4 $10000 \bigcup 00010 = 10010$. The number of 1s is 2. The number of words is 2.
* union of W1 solution and W4 $11000 \bigcup 00010 = 11010$. The number of 1s is 3. The number of words is 2.
* union of W2 solution and W4 $11100 \bigcup 00010 = 11110$. The number of 1s is 4. The number of words is 3. (W4 SOLUTION)
* union of W3 solution and W4 $11100 \bigcup 00010 = 11110$. The number of 1s is 4. The number of words is 4.

*W5: de*

Next is word W5: the "largest sequence of 1s" bit vector is the union maximizing number of 1s and minimizing number of words. Four options:

* only W5 as solution is $00011$. The number of 1s is 2. The number of words is 1.
* union of W0 solution and W5 $10000 \bigcup 00010 = 10010$. The number of 1s is 2. The number of words is 2.
* union of W1 solution and W5 $11000 \bigcup 00011 = 11011$. The number of 1s is 4. The number of words is 2.
* union of W2 solution and W5 $11100 \bigcup 00011 = 11111$. The number of 1s is 5. The number of words is 3. (W5 SOLUTION)
* union of W3 solution and W5 $11100 \bigcup 00011 = 11111$. The number of 1s is 5. The number of words is 4.
* union of W4 solution and W5 $11110 \bigcup 00111 = 11111$. The number of 1s is 5. The number of words is 4.

*W6:*

Next is word W6: the "largest sequence of 1s" bit vector is the union maximizing number of 1s and minimizing number of words. Five options:

* only W6 as solution is $01000$. The number of 1s is 1. The number of words is 1.
* union of W0 solution and W6 $10000 \bigcup 01000 = 11000$. The number of 1s is 2. The number of words is 2.
* union of W1 solution and W6 $11000 \bigcup 01000 = 11000$. The number of 1s is 2. The number of words is 2.
* union of W2 solution and W6 $11100 \bigcup 01000 = 11100$. The number of 1s is 3. The number of words is 3.
* union of W3 solution and W6 $11100 \bigcup 01000 = 11100$. The number of 1s is 3. The number of words is 4.
* union of W4 solution and W6 $11110 \bigcup 01000 = 11110$. The number of 1s is 4. The number of words is 4.
* union of W5 solution and W6 $11111 \bigcup 01000 = 11111$. The number of 1s is 5. The number of words is 4. (W6 SOLUTION)

(NOTE: We don't need to consider every possible combination of W1, W2, W3, W4, W5, and W6; we only need to consider each word once, because each word's current solution can be written in terms of the prior word's solution, so we only need to consider solutions for each word. We've already considered the non-solutions and can therefore ignore them because they don't maximize number of 1s and minimize number of words.)

Thus far, we have found a ''local'' solution for each word. We can now compare all of these ''local'' solutions to find a ''global'' solution. The global solution will maximize the number of 1s found (meaning we can toss out any solutions that have less than 5 1s), and minimizes the total number of words (meaning, our W5 solution gives us the global optimum).

Therefore our global solution is the W5 solution: 5 1s, and 3 words. Thus, backtracking, we see that the words W1, W2, W5 cover all of the first five letters, with the minimum number of total words.

```
W0 = aa = 10000
W2 = bc = 01100
W5 = de = 00011
```


<a name="five3-pseudocode"></a>
## Pseudocode

Here is the pseudocode for the program. We utilize one function to compute
the letter coverage bit vector for a single word, and the rest of the 
functionality will go in the main method:

```plain
function word2bitvector(word):
	initialize 26-element bit vector with 0s (one 0 per letter)
	for each letter in word:
		turn the bit for this letter to 1
	return bit vector

fuction main():
	
	// initialization step:
	initialize best coverage bit vector
	initialize maximum number of 1s (the number of letters N we wish to cover)
	initialize number of words in current solution
	initialize backtracking array (for constructing final solution)

	// outer loop fencepost step:
	set things up for word 0 (base case)

	// loop through each word
	for each word in words:
		// skip word 0 (base case)

		// inner loop fencepost step:
		initialize things for word (i-1)

		for each prior word j < i:
			compute the new potential best coverage bitvector
			compute the number of 1s in the bnew potential best coverage bit vector
			compute numbr of words in new potential best solution
			if this solution is better than current best solution:
				overwrite best solution with current solution

	// get solution:
	find maximum indices of vector of number of 1s 
	// (this is potentially multiple indices, representing multiple 
	//  solutions that satisfy the coverage we want)
	find minimum number of words corresponding to each of the coverage indices
	backtrack through solution indices
```

<a name="five3-python"></a>
## Python Code

The code for this solution can be found here: [letter_coverage.py](https://git.charlesreid1.com/cs/five-letter-words/src/master/letter_coverage.py)

This code is as follows:

Start with the word-to-bit vector function:

```python
def word2bitvector(word,N):
    """
    Turns a five-letter word into a bit vector representing character coverage.
    Uses 26 letters by default.
    """
    bit_vector = [False,]*N
    for c in word:
        i = ord(c)-ord('a')
        try:
            bit_vector[i] = True
        except IndexError:
            pass
    return np.array(bit_vector)
```

We also implement a few helper methods: the first turns a boolean bit vector into 
a pretty string of 0s and 1s:

```python
def printbv(bv):
    result = ""
    for bit in bv:
        if bit:
            result += "1"
        else:
            result += "0"
    return result
```

The second method is our all-important backtracking to obtain the actual sequence of words
that leads to the minimum coverage, instead of just getting a count of the minimum number 
of words that it takes to cover the first $N$ letters:

```python
def btsolution(min_key, min_val, words, bt):
    """
    Reconstruct the sequence of words that gives maximum coverage and minimum word count.

    Input: minimum word key (last word), minimum value (number of words), backtrack (prior word)

    Output: list of words
    """
    solution = []
    solution.append(words[min_key])
    prior_key = bt[min_key]
    while prior_key != -1:
        solution.append(words[prior_key])
        prior_key = bt[prior_key]
    return reversed(solution)
```

Finally, we get to the meat of the method: the dynamic program.
Start with some initialization. This is where we set the number of letters
we want to cover, and limit the "vocabulary" if desired: 

```python
if __name__=="__main__":

    # Searching for words covering first N letters
    N = 13

    words = get_words()

	# If we want to restrict our search to the first M letters,
    #words = words[:1000]
```

We begin with the initialization step:

```python
    # Initialization:
    # ----------------

    # Store best coverage bitvectors for each word
    bestcoverage_bv = [np.array([False]*N) for k in range(len(words))]

    # Store number of 1s for best coverage vector for each word
    ones_bv = [-1]*len(words)

    # Store number of words in best solution for each word
    ws = [0]*len(words)

    # Store prior word for backtracking
    bt = [-1]*len(words)
```

Next comes the fencepost initialization step, where we intiialize the solution
for word 0:

```python
    # Fencepost: Initial Step
    # Word 0
    # ----------------

    i = 0

    # Start with word 0
    wi = words[i]

    # Best letter coverage bit vector
    bestcoverage_bv[i] = word2bitvector(words[i],N)

    # Length of 1s
    ones_bv[i] = sum(bestcoverage_bv[i])

    # Number of words in best solution:
    ws[i] = 1

    # Backtracking: first word has no prior word
    bt[i] = -1
```

Next, we loop over each word $w_i, i>0$: 

```python
    # Start by assuming the word by itself, 
    # and then examine each possible pairing
    for i in range(1,len(words)):
        wi = words[i]

        # Start with bitvector of word i's coverage
        wi_bv = word2bitvector(wi,N)

        # Fencepost: initial step
        # Word i by itself
        # Assume word i is the first word in the solution,
        # and if we find a better combination with prior word,
        # overwrite this solution.
        # ------------------------

        # Best coverage so far (first guess) is word i by itself
        bestcoverage_bv[i] = wi_bv

        # Count ones in (first guess) best bitvector
        ones_bv[i] = sum(bestcoverage_bv[i])

        # Number of words in new best solution:
        ws[i] = 1

        # Backtracking
        bt[i] = -1

        # Boolean: is this the first word in the sequence of solutions?
        first = True
```

We started by assuming that each word $w_i$ provides a best solution by itself;
the next step is to consider each pairing of $w_i$ with prior words $w_j$,
and update our current solution if we find a better one: 

```python
        # Now loop over the rest of the words,
        # and look for a better solution.
        for j in reversed(range(0,i)):

            # Get the prior word
            wj = words[j]

            # Get best coverage bitvector 
            wj_bv = bestcoverage_bv[j]

            # (potential) new combined coverage vector
            bestcoverage_bv_i = np.logical_or(wi_bv, wj_bv)

            # Number of ones in (potential) new combined coverage vector
            ones_bv_i = sum(bestcoverage_bv_i)

            # Number of words in (potential) new best solution
            ws_i = ws[j]+1

            # If this solution is better than our current one,
            # overwrite the current solution.
            # (Better means, "more ones", or "same ones and fewer words".)

            #import pdb; pdb.set_trace();

            if( (ones_bv_i > ones_bv[i]) or (ones_bv_i==ones_bv[i] and ws_i < ws[i]) ):
                bestcoverage_bv[i] = bestcoverage_bv_i
                ones_bv[i] = ones_bv_i
                ws[i] = ws_i
                bt[i] = j

                # This word now follows another word in the sequence of solutions
                first = False

            # It's tempting to stop early,
            # but what if we find the perfect 
            # solution right at the end?!?
```

Now that we have found the coverage for each word, and the corresponding number of words 
in that coverage solution, we find the solution that achieves the desired coverage 
while minimizing the number of words, so that we can construct the actual solution:

```python
    # Okay, now actually get the solution.
    # The solution is the maximum of ones_bv and the minimum of ws
    # 
    # Start by finding the maximum(s) of ones_bv
    # Then check each corresponding index of ws
    ones_bv_indices = [k for k,v in enumerate(ones_bv) if v==max(ones_bv)]

    min_key = ones_bv_indices[0]
    min_val = ones_bv[ones_bv_indices[0]]
    for ix in reversed(ones_bv_indices[1:]):
        if(ones_bv[ix] < min_key):
            min_key = ix
            min_val = ones_bv[ix]



    print("Min key: word "+str(min_key)+" = "+words[min_key])
    print("Min val: "+str(min_val)+" words to cover "+str(N)+" letters")

    pprint(list(btsolution(min_key, min_val, words, bt)))

```

<a name="output"></a>
## Output and Timing

Let's take a look at some example output from the program. 
This program only considers the first 1,000 words in the five-letter word list:

```
$ time py letter_coverage.py
Takes 9 words to cover 15 letters
['which',
 'their',
 'about',
 'could',
 'after',
 'right',
 'think',
 'major',
 'level']

real    0m17.226s
user    0m17.090s
sys	    0m0.087s
```

Here's the same program, considering all 5,757 words:

```
$ time py letter_coverage.py
akes 9 words to cover 15 letters
['which',
 'their',
 'about',
 'could',
 'after',
 'right',
 'think',
 'major',
 'level']

real	9m29.619s
user	9m24.360s
sys	0m1.958s
```

Note that the algorithm is $O(N^2)$, since it iterates over each word, and for each word,
it examines each possible pairing with a preceding word. Thus, if we increase the number of words
by a factor of 6, we expect the runtime to increase by a factor of 36, for an estimated runtime of 
$36 \times 17 \mbox{ seconds} \approx 10 \mbox{ minutes}$, which is pretty close to what we see above.


