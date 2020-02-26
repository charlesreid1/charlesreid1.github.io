Title: CSE 143 Final Project: Classy
Date: 2017-06-23 9:00
Category: Computer Science
Tags: programming, comparison, sorting, algorithms, computer science, final project, competitive programming

# Table of Contents

* [Problem Description](#classy-problem)
* [Solution Approach](#classy-approach)
* [Algorithm](#classy-algo)
* [Pseudocode](#classy-pseudo)
* [Using an Object-Oriented Approach](#classy-oop)
* [Code](#classy-code)
* [References](#classy-refs)

<a name="classy-problem"></a>
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

```text
5
mom: upper upper lowre middle class
dad: middle middle lower middle class
queen_elizabeth: upper upper class
chair: lower lower class
unclebob: middle lower middle class
```

The proper output should be the name of each person,
sorted in order according to their social status, e.g.,

```text
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
# Algorithm 

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
# Pseudocode

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
# Using an Object-Oriented Approach

To apply object-oriented principles in this situation, 
we want to bundle together related data, and abstract 
away details. That means we want to create an object
to associate the name and titles of a given person,
and implement functionality to allow each person
to be compared with other people. 

This will allow us to create two people 
and compare them with greater than, less than, or 
equal to operators. More importantly, this will also allow us 
to perform sorting.

Our Java program Classy is a simple driver that loads the names and titles
of people from standard input.

The Person class stores associated name and title data for each person.
This class implements the Comparable interface, which requires it 
to implement a `compareTo()` method.


```
class Person implements Comparable<Person> {

	...

	public int compareTo(Person p2) { 
```

The Person class constructor just tokenizes one line of input,
populating the titles list and the person's name. Here is the 
declaration of those private fields:

```
class Person implements Comparable<Person> {
	private String name;
	private ArrayList<String> titles;

	...

```

The implementation of the compareTo method 
utilized Stack objects to examine the 
sequence of titles in reverse.

Pop the stacks until one of them is empty.
Then, keep popping until both are empty, 
using "middle" in place of the empty stack.

```
	/** Compare a person to another person. */
	public int compareTo(Person p2) { 

		Stack<String> st1 = new Stack<String>();
		Stack<String> st2 = new Stack<String>();

		// Add names to stack, left to right
		for(String title : this.getTitles()) {
			st1.push(title);
		}
		for(String title : p2.getTitles()) { 
			st2.push(title);
		}

		// Compare each name, from right-to-left.
		// If stack 1 is not empty, pop next item, otherwise use "middle"
		// If stack 2 is not empty, pop next item, otherwise use "middle"

		int max = Math.max(this.getTitles().size(), p2.getTitles().size());
		for(int i=0; i<max; i++) {

			// Pop names from the stack, right to left.
			String s1, s2;

			if(!st1.isEmpty()) {
				s1 = st1.pop();
			} else {
				s1 = "middle";
			}

			if(!st2.isEmpty()) {
				s2 = st2.pop();
			} else {
				s2 = "middle";
			}

			// Rather than converting strings to numbers,
			// compare the strings directly (lower < middle < upper).
			int res = s2.compareTo(s1);

			// Return the first non-zero value
			if( res != 0 ) {
				return res;
			}
		}

		// If we reach here, there was a tie.
		// Use name as tie breaker.
		return this.getName().compareTo(p2.getName());
	}
```


<a name="classy-code"></a>
# Code

Here is the entire Classy code, also available on 
[git.charlesreid1.com](https://git.charlesreid1.com/cs/finalproject-143/src/master/classy/Classy.java):

```
import java.util.*; 
import java.io.*;
public class Classy { 

	public static void main(String[] args) { 
		Scanner s = new Scanner(new BufferedReader(new InputStreamReader(System.in)));

		// Read the input file: new Person for each line
		int n = Integer.parseInt(s.nextLine());
		ArrayList<Person> people = new ArrayList<Person>();
		while(s.hasNextLine()) {
			String line = s.nextLine();
			String[] deets = line.split(" ");
			Person p = new Person(deets);
			people.add(p);
		}

		Collections.sort(people);
		for(Person p : people) { 
			System.out.println(p);
		}
	}
}

class Person implements Comparable<Person> {
	private String name;
	private ArrayList<String> titles;

	/** Person constructor - pass in a String array with the deets. */
	public Person(String[] deets) { 
		name = deets[0];
		// Remove : from name
		name = name.substring(0,name.length()-1);

		// initialize list of classes 
		titles = new ArrayList<String>();
		for(int i=1; i<deets.length-1; i++) { 
			titles.add(deets[i]);
		}
		// Last word will be "class", so ignore.
	}

	/** Get a person's name. */
	public String getName() { return name; }

	/** Get a person's titles in an ArrayList. */
	public ArrayList<String> getTitles() { return titles; }

	/** Get a string representation of a person. */
	public String toString() { return getName(); }

	/** Compare a person to another person. */
	public int compareTo(Person p2) { 

		Stack<String> st1 = new Stack<String>();
		Stack<String> st2 = new Stack<String>();

		// Add names to stack, left to right
		for(String title : this.getTitles()) {
			st1.push(title);
		}
		for(String title : p2.getTitles()) { 
			st2.push(title);
		}

		// Compare each name, from right-to-left.
		// If stack 1 is not empty, pop next item, otherwise use "middle"
		// If stack 2 is not empty, pop next item, otherwise use "middle"

		int max = Math.max(this.getTitles().size(), p2.getTitles().size());
		for(int i=0; i<max; i++) {

			// Pop names from the stack, right to left.
			String s1, s2;

			if(!st1.isEmpty()) {
				s1 = st1.pop();
			} else {
				s1 = "middle";
			}

			if(!st2.isEmpty()) {
				s2 = st2.pop();
			} else {
				s2 = "middle";
			}

			// Rather than converting strings to numbers,
			// compare the strings directly (lower < middle < upper).
			int res = s2.compareTo(s1);

			// Return the first non-zero value
			if( res != 0 ) {
				return res;
			}
		}

		// If we reach here, there was a tie.
		// Use name as tie breaker.
		return this.getName().compareTo(p2.getName());
	}
}
```

<a name="classy-refs"></a>
# References

1. "ACM Pacific Region Programming Competition." Association of Computing Machinery. 19 June 2017.
<[http://acmicpc-pacnw.org/](http://acmicpc-pacnw.org/)>

2. "finalproject-143 (git repository)." Charles Reid. Modified 16 June 2017. Accessed 23 June 2017.
<[https://git.charlesreid1.com/cs/finalproject-143/src/master/classy/Classy.java](https://git.charlesreid1.com/cs/finalproject-143/src/master/classy/Classy.java)>

