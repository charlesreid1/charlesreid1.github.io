Title: CSE 143 Final Project: Classy
Date: 2017-06-20 11:00
Category: Computer Science
Tags: programming, computer science, final project, competitive programming

# Table of Contents

* [Problem Description](#classy-problem)
* [Solution Approach](#classy-approach)
* [Solution Algorithm](#classy-algo)
* [Solution Pseudocode](#classy-pseudo)
* [Solution Code](#classy-code)
* [References](#classy-refs)

<a name="classy-intro"></a>
# Problem Description

Comedian John Cleese, in his memoir __So Anyway...__, described the social classes of his
mother and father as "upper-uper-lower-middle class" and "middle-middle-middle-lower-middle class",
respectively. Write a program that will sort individuals based on a labeling of their 
social standing by class.

The three main classes are upper, middle, and lower. Classes progress hierarchically
from right to left. For example, lower-upper would come before lower-lower.
There is also ordering within a class, so upper-upper is a higher class than middle-upper.

Once you have reached the lowest level of detail of one of the classes, assume that
all further classes are equivalent to middle. This means upper and middle-upper are
equivalent, and middle-middle-lower-middle and lower-middle are equivalent.

Input files have a line with the number of names, then one name per line,
with the name, a colon, then the title. For example:

```plain
5
mom: upper upper lowre middle class
dad: middle middle lower middle class
queen_elizabeth: upper upper class
chair: lower lower class
unclebob: middle lower middle class
```

The proper output should be the name of each person,
sorted in order according to their social status, e.g.,

```plain
queenelizabeth
mom
dad
unclebob
chair
```

<a name="classy-approach"></a>
# Solution Approach

(This discusses an approach specific to Java, 
but a similar approach could be adopted for other languages
in which comparison operators can be overloaded for objects.)

The problem lays out all of the essential components that a solution requires.
This can most easily be implemented using an object and a comparator: 
the object represents a person, and has a field to store their name and a field
to store their titles (array-like container for Strings). These objects
would then implement comparators so that indivduals could be compared. 
This functionality then allows the array to be sorted, using the built-in 
Colletions sort function or a custom sort function.

<a name="classy-algo"></a>
# Solution Algorithm 

<a name="classy-pseudo"></a>
# Solution Pseudocode

<a name="classy-code"></a>
# Solution Code

<a name="classy-refs"></a>
# References

1. "ACM Pacific Region Programming Competition." Association of Computing Machinery. 19 June 2017.
<[http://acmicpc-pacnw.org/](http://acmicpc-pacnw.org/)>


