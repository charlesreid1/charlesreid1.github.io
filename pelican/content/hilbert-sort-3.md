Title: CSE 143 Final Project: Hilbert Sort: 3. The Code
Date: 2017-06-30 20:00
Category: Computer Science
Tags: programming, computer science, final project, competitive programming, hilbert sort, java

# Table of Contents

This is the third in a series of three posts 
detailing the Hilbert Sort problem,
its solution, and its implementation.
This post deals with the code to solve the
Hilbert Sort problem.

* [Pseudocode](#hilbert3-pseudocode)

* [Code](#hilbert3-code)
	* [Utility Classes](#hilbert3-utility)
	* [Recursive Sort Function](#hilbert3-recursive)
	* [Main Method](#hilbert3-main)

* [References](#hilbert2-references)


<a name="hilbert3-pseudocode"></a>
# Hilbert Sort: Pseudocode

From our prior post, here is the psudocode for our Hilbert Sort function:

```
define hilbert_sort( unsorted queue, square dimension ):
	create southwest queue
	create northwest queue
	create northeast queue
	create southeast queue
	for each point:
		if in southwest:
			create new point using X -> Y, Y -> X
			add to southwest queue
		if in northwest:
			create new point using X -> 2X, Y -> 2Y - S
			add to northwest queue
		if in northeast:
			create new point using X -> 2X - S, Y -> 2Y - S
			add to northeast queue
		if in southeast:
			create new point using X -> S - 2Y, Y -> 2S - 2X
			add to southeast queue

		hilbertsort(southwest queue, square dimension)
		hilbertsort(northwest queue, square dimension)
		hilbertsort(northeast queue, square dimension)
		hilbertsort(southeast queue, square dimension)

		create new results queue
		add points from southwest into results queue
		add points from northwest into results queue
		add points from northeast into results queue
		add points from southeast into results queue
		return results queue
```

Because we are manually sorting, and we want order to be preserved,
we should be using a queue to organize points as we sort them.
That way, we add them in sorted order, and we are then able to remove
them in sorted order.



<a name="hilbert3-code"></a>
# Hilbert Sort: Code

We begin by covering a utility class used by the Hilbert Sort method
to store $(X,Y)$ points. This is a simple example of a composition 
design pattern. Next, we cover the bulk of the problem solution: 
the recursive sort method that partiions points into quadrants.
Finally, we cover the main method, which demonstrates reading data
from an input file and passing it to the sort method.

<a name="hilbert3-utility"></a>
## Hilbert Sort: Utility Classes

To organize $(X,Y)$ point data, we use a simple class
using composition. This is defined next to the HilbertSort 
class.

```
/**
 * An (x,y) Point class. 
 */
class Point {
	int x, y; // (x,y) point.
	String name; // Each (x,y) point has a name in the file. Used for output.
	/** Constructor. */
	public Point(int x, int y, String name) { 
		this.x = x; this.y = y; this.name = name;
	}
	/** String representation (x,y). */
	public String toString() { 
		return "("+this.x+","+this.y+","+this.name+")";
	}
}
```


<a name="hilbert3-recursive"></a>
## Recursive Sort Function

Following is the recursive sort method, which (like merge sort)
consists of a split step, which partitions an $S \times S$ 
square into quadrants and distributes points in the square into their
corresponding quadrants, and a merge step, which stitches together
each quadrant in the correct order. 

```
	/** Recursive implementation of a Hilbert sort. */
	public static Queue<Point> hilbertSort(Queue<Point> inputP, int S) {
		// Recursive method:
		// Apply the Hilbert geometrical quadrant division 
		// to sort points by when they are visited by a Hilbert curve.
		//
		// Base case: 
		// There are 1 or fewer points in each quadrant.
		// Keep splitting into quadrants until we reach the base case. 
		if(inputP.size()<1) {
			return new LinkedList<Point>();
		} else if(inputP.size()==1) {
			return inputP;
		}

		// split by quadrant
		Queue<Point> qSW = new LinkedList<Point>();
		Queue<Point> qNW = new LinkedList<Point>();
		Queue<Point> qNE = new LinkedList<Point>();
		Queue<Point> qSE = new LinkedList<Point>();

		// Sort points by dividing into quadrants
		for(Point p : inputP) { 

			// Prepare for the tricky part.
			//
			// Rotate the quadrant, and points in it,
			// so that everything is now translated to fit
			// how the template of the Hilbert curve is being drawn.
			// (SW->NW->NE-SE)

			boolean inSWquadrant = (2*p.x <= S) && (2*p.y <= S);
			boolean inNWquadrant = (2*p.x <= S) && (2*p.y >= S);

			boolean inNEquadrant = (2*p.x >= S) && (2*p.y >= S);
			boolean inSEquadrant = (2*p.x >= S) && (2*p.y <= S);

			// Each time we sort (x,y) points into quadrants,
			// we also transform each coordinate point 
			// in such a way that it rescales to an S x S square,
			// but does not modify the order of the points. 
			//
			// Note that we can keep everything as integers by
			// continuing to look at an S x S square,
			// and double the x and y values to shift them over/up.
			//
			// Two easy cases:
			if(inNWquadrant) {
				// Northwest quadrant: 
				// - shift y down by S/2
				// - keep x and y in same order
				qNW.add( new Point(2*p.x, 2*p.y-S, p.name) );

			} else if(inNEquadrant) {
				// Northeast quadrant:
				// - shift x and y down by S/2
				// - keep x and y in same order
				qNE.add( new Point(2*p.x - S, 2*p.y - S, p.name) );

			} else if(inSWquadrant) { 
				// Southwest quadrant:
				// - x and y need to swap places 
				// - that's it.
				qSW.add( new Point(2*p.y, 2*p.x, p.name) );

			} else if(inSEquadrant) { 
				// Southeast quadrant:
				// - trickiest quadrant.
				// - We want to preserve S - x, distance from right side
				// - we want to use it as the new y coordinate
				qSE.add( new Point(S - 2*p.y, 2*(S - p.x), p.name) );

			}

		}
		// Sort til you reach the base case.
		qSW = hilbertSort(qSW, S); 
		qNW = hilbertSort(qNW, S); 
		qNE = hilbertSort(qNE, S); 
		qSE = hilbertSort(qSE, S);

		Queue<Point> result = new LinkedList<Point>();
		for(Point q : qSW) result.add(q);
		for(Point q : qNW) result.add(q);
		for(Point q : qNE) result.add(q); 
		for(Point q : qSE) result.add(q);

		return result;
	}
```

<a name="hilbert3-main"></a>
## Main Method

The last part of the code is the portion that loads the points and their labels 
from a file, and populates a Queue of Point objects from it.
This queue of points is then sorted and returned in order.

```
	/** Main driver. */
	public static void main(String[] args) { 
		
		Scanner stdin = new Scanner(new BufferedReader(new InputStreamReader(System.in)));

		int n = stdin.nextInt();
		int S = stdin.nextInt();

		// n lines of 3 tokens each
		Queue<Point> inputPoints = new LinkedList<Point>();
		for(int i=0; i<n; i++) { 
			int x0 = stdin.nextInt();
			int y0 = stdin.nextInt();
			String label = stdin.next();
			inputPoints.add(new Point(x0,y0,label));
		}
		Queue<Point> sortedPoints = hilbertSort(inputPoints, S);
		for(Point p : sortedPoints) { 
			System.out.println(p.name);
		}
	}
```

<a name="hilbert3-refs"></a>
# References

1. "ACM Pacific Region Programming Competition." Association of Computing Machinery. Accessed 19 June 2017.
<[http://acmicpc-pacnw.org/](http://acmicpc-pacnw.org/)>

2. "Hilbert Sort." Git repository, git.charlesreid1.com. Charles Reid. Updated 16 June 2017.
<[https://git.charlesreid1.com/cs/finalproject-143/src/master/hilbert/HilbertSort.java](https://git.charlesreid1.com/cs/finalproject-143/src/master/hilbert/HilbertSort.java)>


