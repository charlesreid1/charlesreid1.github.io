Title: CSE 143 Final Project: Classy
Date: 2017-06-20 11:00
Category: Computer Science
Tags: programming, computer science, final project, competitive programming

# Table of Contents

* [Problem Description](#classy-problem)
* [Solution Approach](#classy-approach)
* [Solution Algorithm](#classy-algo)
* [Solution Pseudocode](#classy-pseudo)
* [Solution OOP](#classy-oop)
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
would then implement comparators so that individuals could be compared. 
This functionality then allows the array to be sorted, using the built-in 
Collections sort function or a custom sort function.

<a name="classy-algo"></a>
# Solution Algorithm 

The classy algorithm can be briefly described in this way: we are iterating over two lists of strings,
of possibly unequal length, and comparing them right to left. We have a few very simple rules that 
determine whether one title comes before the other. We have a few simple rules for breaking ties.

The core of the algorithm is the comparison operation, in which we are assuming that these two things 
are equal, until we encounter evidence to the contrary. Briefly, the pseudocode can be expressed as follows
(where we adopt the Java convention that a negative result means the first item comes before the second item):

```
if item1 < item2:
	return -1
else if item1 > item2: 
	return 1
else:
	# keep going
```

If we find a difference, we stop and return right away, 
but otherwise we continue, and assume the two are equal.

The problem statement tells us that if a title is missing, and the title lengths are mismatched, we should 
fill in with "middle". This translates into a second comparison block, in which one of the items is 
hard-coded as "middle", due to an empty list of titles:

```
if item < "middle":
	return -1
else if item > "middle"
	return 1
else:
	# keep going
```

Here is how these fit together:
* Start by splitting the input titles, most likely strings, into lists
* Iterate over each title, from right to left, and compare the titles.
* When we reach the end of the shorter list, continue comparing titles right to left, filling in "middle".
* If the titles are tied, break ties with name.
* The algorithm should be implemented in a way that has access to both the titles and the names of the two people being compared.
* In Java, we can define people objects, then we can either have People objects implement Comparable, or we can define our own Comparator for two People objects.

<a name="classy-pseudo"></a>
# Solution Pseudocode

When we translate the above procedure into Python-like pseudocode, here is the result:

```
define compare_lengths(title1, title2):
	list1 = title1.split()
	list2 = title2.split()
	for i in min(list1.size, list2.size):
		sal1 = list1.reverse[i]
		sal2 = list2.reverse[i]
		if sal1 < sal2:
			return -1
		else if sal1 > sal2:
			return 1
	
	larger_list = <point to larger list>
	for i in ( min(list1.size,list2.size)+1 ... max(list1.size, list2.size) ):
		salX = larger_list.reverse[i]
		if SalX < "middle":
			return -1
		if salX > "middle"
			return 1
	
	# If you get here, it's a tie. Use names for tie-breaker.

```

<a name="classy-oop"></a>
# Solution OOP

Java solution: can use objects that implement Comparable, or define our own Comparator objects.

<a name="classy-code"></a>
# Solution Code

<a name="classy-refs"></a>
# References

1. "ACM Pacific Region Programming Competition." Association of Computing Machinery. 19 June 2017.
<[http://acmicpc-pacnw.org/](http://acmicpc-pacnw.org/)>




















