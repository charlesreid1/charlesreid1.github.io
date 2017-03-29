Title: Fixing Bottlenecks in the Guava Traveling Salesperson Problem Code
Date: 2017-03-29 14:00
Category: Java
Tags: computer science, guava, graph, TSP

* [Intro](#tsp2-intro)
* [The Graphs We Are Solving](#tsp2-graphs)
    * [Visualizations of Graphs](#tsp2-viz-graphs)
* [Guava TSP Solution](#tsp2-guava-tsp-soln)
    * [TSP Solution](#tsp2-guava-tsp-soln)


<a name="tsp2-intro"></a>
## Intro 

In a prior blog post we introduced you to the traveling salesperson problem (TSP),
which involves finding the shortest path through every city in a group of cities
connected by a network of roads. Using Google Guava, we have implemented a solution 
to the TSP in Java.

Our philosophy toward timing, profiling, and optimization is that it is always best 
to work from data - and timing is the first place to begin collecting data.
As we will show in this blog post, simply timing your function for different problem sizes
can reveal scaling behavior that indicates bottlenecks, bugs, or inefficiencies in the algorithm.

In this post, we use simple timing tools and a spreadsheet 
to plot scaling behavior and identify bottlenecks in the 
traveling salesperson problem code. Fixing the bottleneck
led to a reduction in cost of **two orders of magnitude**.

![TSP Guava Solution scaling results - initial and pessimist algorithms](/images/tsp-guava-initial-pessimist.png)

In this post we'll cover what we did to time the problem,
the initial results, and the algorithm improvement that led to 
the massive performance improvement.

But first, let's look at some of the graphs that are being solved.

<a name="tsp2-graphs"></a>
## The Graphs We Are Solving

Let's start by having a look at some of the graphs we will be solving,
and the representation of the problem.

<a name="tsp2-viz-graphs"></a>
### Visualizations of Graphs

The first few graphs start out simple: here is a randomly generated 4-node traveling salesman problem
(we wil cover the code that generates the graph pictured here in a moment):

![TSP graph with 4 nodes](/images/graphviz_tsp_4.png)

**Shortest Route: [0, 2, 3, 1] Distance: 112.0**

Here is another randomly generated graph with 5 nodes:

![TSP graph with 5 nodes](/images/graphviz_tsp_5.png)

**Shortest Route: [0, 4, 2, 1, 3]	Distance: 130.0**

With 6 nodes:

![TSP graph with 6 nodes](/images/graphviz_tsp_6.png)

**Shortest Route: [0, 2, 4, 1, 5, 3]	Distance: 163.0**

But problem of this sise are still trivially easy for a processor to handle.
Our inefficient, first-pass algorithm started to show signs of eating up CPU cycles 
at around 9 nodes (albeit less than 1 second). Here is the graph with 9 nodes:

![TSP graph with 9 nodes](/images/graphviz_tsp_9.png)

**Shortest Route: [0, 6, 1, 7, 3, 2, 5, 8, 4]	Distance: 166.0**

With 12 nodes:

![TSP graph with 12 nodes](/images/graphviz_tsp_12.png)

**Shortest Route: [0, 7, 5, 4, 1, 8, 6, 10, 11, 9, 3, 2]	Distance: 236.0**

At 14 nodes, even the efficient algorithm crosses the 1 second threshold.

![TSP graph with 14 nodes](/images/graphviz_tsp_14.png)

**Shortest Route: [0, 2, 6, 10, 13, 12, 7, 4, 1, 11, 5, 3, 9, 8]	Distance: 277.0**

We tested randomly-generated, fully-connected graphs of up to 18 nodes, 
and the algorithm was able to compute solutions within a few minutes.
Here is an 18-node graph:

![TSP graph with 18 nodes](/images/graphviz_tsp_18.png)

**Shortest Route: [0, 3, 10, 6, 12, 5, 11, 2, 14, 8, 13, 4, 7, 1, 9]	Distance: 267.0**


<a name="tsp2-guava"></a>
## Improving the Guava TSP Solution and the Pessimist Algorithm

In a prior post we covered the implementation of a solution to the TSP 
using Guava's Network objects. This implementation utilized a recursive
depth-first search algorithm to search for the shortest path among all nodes.

To recap, here is what the recursive backtracking `explore()` method looked like:

```java
	/** Recursive backtracking method: explore possible solutions starting at this node, having made nchoices */
	public void explore(Node node, int nchoices) {

		if(nchoices == graphSize) {
			// 
			// BASE CASE
			//
			if(this.this_distance < this.min_distance || this.min_distance < 0) {
				// Solution base case
				this.min_distance = this.this_distance;
				printSolution();
			}
			
		} else {
			//
			// RECURSIVE CASE
			// 	
			Set<Node> neighbors = graph.adjacentNodes(node);
			for(Node neighbor : neighbors) {
				if(neighbor.visited == false) {
					
					int distance_btwn = -10000;
					
					for( Edge edge : graph.edgesConnecting(node, neighbor) ) {
						distance_btwn = edge.value;
					}

					// Make a choice
					this.route[nchoices] = neighbor.id;
					neighbor.visit();
					this.this_distance += distance_btwn;
					
					// Explore the consequences
					explore(neighbor,nchoices+1);
					
					// Unmake the choice
					this.route[nchoices] = -1;
					neighbor.unvisit();
					this.this_distance -= distance_btwn;
				}
				// Move on to the next choice (continue loop)
			}				
		} // End base/recursive case
	}
```

However, this algorithm contained a flaw - not by implementing a mistake in the calculation,
but by ignoring an important piece of information. 

<a name="tsp2-theflaw"></a>
### The Flaw

As the recursive depth-first search traverses the graph, the algorithm is checking if all nodes have been traversed.
When all nodes have been traversed, it then compares the distance of that journey to the current shortest journey.
If the new journey is shorter, it is saved as the new shortest journey, otherwise it is ignored and we move on.

What this ignores is the fact that any path, at any point, can be checked to see if it is 
longer than the current minimum, and if it is, any possibilities that follow from it can be skipped.

For example, consider the TSP on a graph of six cities, A B C D E F.

Suppose that the algorithm is in the midst of the recursive backtracking solution,
and has a current minimum distance and minimum path of the route `A-B-E-D-C-F`, which is 24 miles.

Now suppose that the algorithm is searching for solutions that begin with the choice `A-E-C`,
and the distance `A-E-C` is 28 miles.

The naive algorithm ignores this information, and continues choosing from among the 
3 remaining cities, computing the total length for $3! = 6$ additional routes, and finding 
that all six of them do not work.

The smart algorithm checks _each time it chooses a new node_ whether the length of the current route
exceeds the current minimum route distance (if one has been found/set).
If not, the algorithm keeps going, but if so, it skips choosing neighbors 
and returns directly to the parent caller.

<a name="tsp2-fixing"></a>

Fixing the flaw is surpsingly easy: we just add an if statement.

```java
		if(nchoices == graphSize) {
			// 
			// BASE CASE
			//
			if(this.this_distance < this.min_distance || this.min_distance < 0) {
				// Solution base case:
				this.min_distance = this.this_distance;
				printSolution();
			}
			
		} else {
			//
			// RECURSIVE CASE
			// 	

            /* 
             * The following lines result in a huge computational cost savings.
            */
            if(this.min_distance>0 && this.this_distance>this.min_distance) {
                // Just give up already. It's meaningless. There's no point.
                return;
            }

			// Everything else stays exactly the same
			Set<Node> neighbors = graph.adjacentNodes(node);
			for(Node neighbor : neighbors) {
				if(neighbor.visited == false) {
					
					int distance_btwn = -10000;
					
					for( Edge edge : graph.edgesConnecting(node, neighbor) ) {
						distance_btwn = edge.value;
					}

					// Make a choice
					this.route[nchoices] = neighbor.id;
					neighbor.visit();
					this.this_distance += distance_btwn;
					
					// Explore the consequences
					explore(neighbor,nchoices+1);
					
					// Unmake the choice
					this.route[nchoices] = -1;
					neighbor.unvisit();
					this.this_distance -= distance_btwn;
				}
				// Move on to the next choice (continue loop)
			}				
		} // End base/recursive case
	}
```

This algorithm is dubbed The Pessimistic Algorithm. Let's see how it works.
Here is that new if statement:

```java
if(this.min_distance>0 && this.this_distance>this.min_distance) {
    // Just give up already. It's meaningless. There's no point.
    return;
}
```

This is a test of two conditions - first, we check if a first minimum distance has actually been found,
and second, we check if the distance of the current path is greater than the minimum distance.
If it is, we give up continuing our search down this path, and just return back to the calling function.










