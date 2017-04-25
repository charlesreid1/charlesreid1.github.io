Title: The Z-Machine: A Simple Turing Machine
Status: draft
Date: 2017-04-24 20:00
Category: Computer Science
Tags: turing machine, computer science, computer engineering, circuit

## TOC 

* [Background](#background)
* [The Z-Machine: Setup](#setup)
* [The Z-Machine: Instructions](#instructions)
* [Simple Example: Loop](#loop)
* [Implementing an Addition Operator on the Z-Machine](#addition)
	* [The Solution Approach (The Maths)](#solution-approach)
	* [Solution 1: Positive Integers Only](#addition1)
	* [Solution 2: Dealing with Zeros](#addition2)
* [Implementing a Decrement Operator on the Z-Machine](#subtraction)
* [Implementing a Less Than Operator on the Z-Machine](#lessthan)
* [Okay, Great. Who Cares?](#whocares)
* [References](#refs)


<a name="bkg"></a>
## Background

Recently I discovered the wonderful blog of [John Graham-Cumming](http://blog.jgc.org/2013/05/the-two-problems-i-had-to-solve-in-my.html).
One of hist posts, from 2013, details a question that he had to answer for the Oxford University Department of Computer Science's "interviews" 
(which, I believe, are a kind of final examination "interview" to graduate, not an interview for admittance to the program).
Graham-Cumming describes one of the quetions he was presented with during his interview.

<a name="setup"></a>
## The Z-Machine: Setup

Here is the problem setup:

Suppose you have a computer with a very simple memory layout. 
The memory consists of a series of numbered locations, each of which can store numbers. 
These numbers are positive or negative integers. Here is an illustration of an example of this memory layout:

![Z Machine Memory Layout](https://charlesreid1.com/w/images/2/22/Z-Machine1.png)

<a name="instructions"></a>
## The Z-Machine: Instructions

Z-Machine Instructions

The machine can only perform three instructions: Zero (Z), Increment (I), and Jump (J).

The **Z operator** zeros out a location in memory. The operation specifies which index should be zeroed out. For example, Z4 will zero out index 4 (which is the 5th item in memory, since indexing starts at 0).

The **I operator** increments the value at a location in memory by 1. The operation specifies which index should be incremented. For example, I6 will increment index 6 (the 7th item in memory) by 1.

The **J operator** compares two locations in memory. If the values are different, the jump operator will branch (that is, jump to a different location in the code). The two locations are specified when calling the operator, and an arrow (or operation number) indicates where the operator should branch TO if the values are not the same. If the values are the same, the code continues.

The program stops when it reaches the end of the instruction list.

<a name="loop"></a>
## Simple Example: Loop

Here is an example of a loop program. This program sets memory index 4 to zero, 
then increments it until it is equal to the value in memory index 20:

```
001   Z4
002   I4
003   J4,20 --> 002
```

The instruction `J4,20 --> 002` indicates that the values in cell 4 and cell 20 
should be compared, and if they are not equal, the machine should jump to instruction `002`.

<a name="addition"></a>
## Implementing an Addition Operation on the Z-Machine

Graham-Cumming includes the following programming challenge in his [blog post](http://blog.jgc.org/2013/05/the-two-problems-i-had-to-solve-in-my.html):

Suppose a machine has two numbers in the first two locations in memory. Utilize these three operations to add the two numbers together and put the result into the third location in memory.

Under what circumstances does the program fail?

<a name="solution-approach"></a>
### The Solution Approach (The Maths)

To approach the solution, start with the maths. What we're doing is trying to define a "complex" arithmetical operation (addition) from simpler "unit" operations (increment by one), so it will be helpful to wipe our mental slate clean and start at the very beginning of the problem.

When I teach a math class, whether it be a developmental math class, an algebra class, or a calculus class, I always spend the first "full" lecture by guiding the students through this very procedure. Here's how I set the tone: "Imagine that you are stranded on a desert island, with no calculators, no math books, nothing but your fingers and toes. Now suppose you are tasked with reinventing all of mathematics, entirely from scratch. How would you do it?"

This is a challenging task - and part of the challenge is just knowing where to begin (just how clean should you wipe the mental slate?). The Z-Machine problem formulation resolves that problem by explicitly enumerating valid operations. But let's continue with the desert island analogy for a bit.

If we begin at what is truly the beginning, we can start with a single unit, the number 1. (If we want to fast forward through thousands of years of human history, we can instead start with the number 0 in addition to the number 1.) Having only a single number is boring, because we can't count anything. We need a way to generate more numbers. So, we begin by defining an increment operation. We begin with the unit, 1. We declare that we can combine 1 with any other number. When we combine 1 with another 1, we get a new, larger number - which we arbitrarily call two, and represent using this funny squiggle: 2.

Now that we have defined the increment operation, adding a unit, we can begin to generate new numbers. We start with 1+1, which gives 2. The next number can be found by adding 1 to 2, which gives us a new number that we arbitrarily call three, and represent with a funny squiggle: 3.

We continue in this manner, until we reach 9, and run out of squiggles to write. The next number we will get is a special number, because it is equal to the total number of fingers. When we get to 9, and add one more, we get "two hands", which we arbitrarily call ten. If we want to keep counting beyond ten, we're stuck, because we've run out of fingers. But we can take a shortcut - we can let one toe represent "two hands". So, we hold up one toe, to represent ten. To write ten, we can let the first digit represent how many toes we are holding up, and the second digit represent how many fingers we are holding up. That means we can write our "two hands" quantity as 10 - one toe, no fingers.

We can keep on incrementing by 1, and using this system we can count all the way up to 99, at which point we will need another pair of hands or feet to keep generating new numbers, or we can suppose that after counting to 99, we are able to hold numbers in our head.

But once again, we're generating numbers slowly. We want a way to generate more numbers, faster, so we can count higher. So, we define a new addition operation. Rather than adding 1, we define the general operation of addition recursively. To add two numbers like a and b, we can define this addition in terms of a unit increment:

$$
a + b = a + 1 + 1 + 1 + \dots + 1
$$

We increment the quantity a by 1, b times. This gives us a way to add arbitrary numbers together, so now we can reach much larger numbers by taking the largest number that we can count to, and adding that number to itself.

Extending this approach can lead us from an increment operation (performed b times) to an addition operation (`+b`).

It can also lead from an addition operation (performed b times) to a multiplication operation (`*b`).

Extending the idea further, we can apply the multiplication operation (performed b times) and obtain an exponentiation operation (`^b`).

This recursive definition of new operations can continue as long as we'd like: applying the exponentiation operation b times yields tetration (`^b^b^b^b^b...^b`).

But let's get back to addition.

<a name="addition1"></a>
### Solution 1: Positive Integers Only

Adding two positive integers is the simplest case. 
Essentially, we just perform two loops: 
the first loop increments the result and increments a temporary variable 1, 
and does that until the temporary variable 1 is equal to the first number. 
The second loop increments the result and increments the result by 1 
for a number of times equal to the number at index 1.

```
001   Z2                    // clear space for the result
002   Z3                    // clear space for temp variable 1
003   I2                    // increment result
004   I3                    // increment temp variable 1
005   J3,0 --> 003
006   Z4                    // clear space for temp variable 2
007   I2                    // increment result
008   I3                    // increment temp variable 2
009   J4,1 --> 007
010   Z3                    // clean up
```

(Because we only have an increment operation at our disposal, 
there is no way for us to deal with negative numbers. 
Dittos for non-integer real numbers.) 

This method will fail when either of the two numbers we are adding are zero.

<a name="addition2"></a>
### Solution 2: Dealing With Zeros

A second solution that is a bit more challenging is dealing with the case of possible zeros 
in the first or second position. The algorithm above will increment the result and the 
temporary variable *at least once* (similar to a do-while loop structure), 
which will always cause the comparison operation `J2,0` or `J3,1` to fail
if either cell 0 or cell 1 holds a zero.

Here is code that can deal more gracefully with a zero in either 
the first or second positions. This utilizes some extra space in memory
to keep track of whether index 0 is a zero and whether index 1 is a zero.

```
// initialize
001     Z3
002     Z4 // temp 0
003     Z5 // temp 1
004     Z6 // is index 0 a zero?
005     Z7 // is index 1 a zero?
006     Z8 // zero
007     Z9 // one
008     I9

// increment by amount in index 0
009     J0,8 --> 014
010     I6
011     J4,6 --> 014
012     I4
013     I3
014     J0,4 --> 009

// increment by amount in index 1
015     J1,8 --> 020
016     I7
017     J7,8 --> 020
018     I5
019     I3
020     J1,5 --> 017

// clean up
021     Z4
022     Z5
023     Z6
024     Z7
```

The central idea behind this algorithm is, we keep incrementing the target cell while a 
condition is false, and the condition we are checking is based on a separate, independent counter.
That allows us to correctly increment (and stop incrementing) based on the two numbers 
in index 0 and index 1. 
(We don't want the final result cell to be involved in our final condition check.) 

This pattern can also be expanded to work for adding an arbitrary number of numbers; 
one simply needs to add an additional temp variable and an additional "is zero" variable 
for each new number being added to the total, then another block of 6 statements
to increment by the amount in the given index.
The block of 6 statements checks if the number we are adding is zero, 
and if it is not, the result is incremented by that many times. 

<a name="decrement"></a>
## Implementing a Decrement Operator on the Z-Machine

Suppose an operator places a number into cell 0 of the Z-Machine's memory. 
We require that the Z-Machine subtract 1 from that number, and place it in cell 1. 

The pseudocode approach here is to increment two cells in a particular order:
cell 2, which contains a sentinel value, is incremented. The program them checks if 
cell 2 is equal to cell 0. If it is not, the program increments cell 1, and repeats.
If cell 2 is equal to cell 0, the program stops before cell 1 is incremented, leaving it 
one less than the original value in cell 0.

```
001   Z1			// decrement result
002   Z2			// zero
003   Z3			// one
004   I3
005   J2,3 --> 007  // always false
006   I1
007   I2
008   J2,0 --> 006
```

This pseudocode uses hard-coded constants (zero and one) to create a jump condition
that is always false and therefore always followed. This allows the machine to 
skip a line of code like instruction 006, and perform the increment operation 
in a staggered manner, as described above.

<a name="lessthan"></a>
## Implementing a Less Than Operator on the Z-Machine

Another challenging operation to implement with the Z-Machine is a comparison operator. 
Suppose that an operator places two numbers into the first two memory positions of 
the Z-Machine. That is, index 0 contains a number A, and index 1 contains a number B. 
Supposing these numbers are both natural numbers (either 0 or positive integers), 
a comparison operator will compare the two numbers, select the smaller of the two numbers, 
and place it into the third position in memory (index 2).

The pseudocode approach to implement the comparison operator is to create 
a counter that start at zero, and check if it is equal to A or B 
(the numbers at index 0 and index 1). 
If we continue to increment our counter, and check if it is equal to A or B, 
and stop when it reaches either A or B, we can guarantee that we will stop 
when the counter reaches the smaller of the two numbers.

In order to increment the memory cell at index 2 to hold the smaller of the two numbers 
at index 0 and index 1, we can use the following Z-Machine code, 
which continually checks if the number at index 2 is equal to 
either the number at index 0 or the number at index 1, increments if false, 
and stops when true (when it reaches the smaller of the two). 

```
001		Z2 // smaller of the two numbers
002		Z3 // zero
003		Z4 // one
004		I4

005		J0,2 --> 007
006		J3,4 --> 011
007		J1,2 --> 009
008		J3,4 --> 011
009		I2
010		J3,4 --> 005
011		Z4
```

Note that this code successfully handles the case where either number (or both) 
is 0 or any positive integer.


<a name="whocares"></a>
## Okay, Great. Who Cares?

This whole exercise may appear, at first glance, to be an exercise in trivial pursuit. 
Why bother reinventing the wheel? Isn't this nothing more than an entertaining puzzle?

To the contrary - the process of assembling a sequence of simple operations into a cascade of
more complex operations is precisely how computational devices are assembled from 
circuit components. For example, a [flip flop circuit](https://en.wikipedia.org/wiki/Flip-flop_%28electronics%29)
utilizes a pair of NOR (negation of OR) gates to store bits. The [Apollo Guidance Computer](https://en.wikipedia.org/wiki/Apollo_Guidance_Computer)
was composed entirely of NOR gates. 

In fact, the Apollo Guidance Computer is a fantastic example of a computational device 
constructed from a set of such simple instructions as the ones available in the Z-Machine.
A few example operations from the Wikipedia article on the Apollo Guidance Computer:

```
AD (add)
    Add the contents of memory to register A and store the result in A.

INDEX
    Add the data retrieved at the address specified by the instruction to the next instruction. 
	INDEX can be used to add or subtract an index value to the base address specified by 
	the operand of the instruction that follows INDEX. This method is used to implement 
	arrays and table look-ups.
```

It is not unusual for a hardware platform to have a small set of basic commands or instructions
that can be carried out, and for that set of instructions to be different from hardware platform
to hardware platform. Designing a new computational device requires the system designer
to adapt to the hardware's capabilities - not the other way around. 
For that reason, it is important to keep those engineering and puzzle-solving skills sharp.
You never know when you'll be designing a new computer device.


<a name="sources"></a>
## Sources

1. "The Two Problems I Had To Solve In My Oxford Interview." John Graham-Cumming. Published 2 May 2013. Accessed 24 April 2017.
<[http://blog.jgc.org/2013/05/the-two-problems-i-had-to-solve-in-my.html](http://blog.jgc.org/2013/05/the-two-problems-i-had-to-solve-in-my.html)>

2. "Flip Flop (electronics)." Wikipedia. The Wikimedia Foundation. Edited 13 April 2017. Accessed 24 April 2017.
<[https://en.wikipedia.org/wiki/Flip-flop_%28electronics%29](https://en.wikipedia.org/wiki/Flip-flop_%28electronics%29)>

3. "Apollo Guidance Computer." Wikipedia. The Wikimedia Foundation. Edited 5 April 2017. Accessed 24 April 2017.
<[https://en.wikipedia.org/wiki/Apollo_Guidance_Computer](https://en.wikipedia.org/wiki/Apollo_Guidance_Computer)>

