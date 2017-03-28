Title: Traveling Salesperson Problem: Timing the Guava Solution
Status: draft
Date: 2017-03-28 12:00
Category: Java
Tags: computer science, guava, graph, TSP

* [Intro](#intro)
* [The Graphs We Are Solving](#graphs)
    * [Visualizations of Graphs](#viz-graphs)
* [Guava TSP Solution](#guava-tsp-soln)
    * [TSP Solution](#guava-tsp-soln)


<a name="intro"></a>
## Intro 

In a prior blog post we introduced you to the traveling salesperson problem (TSP),
which involves finding the shortest path through every city in a group of cities
connected by a network of roads. Using Google Guava, we have implemented a solution 
to the TSP in Java.

Our philosophy toward timing, profiling, and optimization is that it is always best 
to work from data - and timing is the first place to begin collecting data.
As we will show in this blog post, simply timing your function for different problem sizes
can reveal scaling behavior that indicates bottlenecks, bugs, or inefficiencies in the algorithm.

In this post, we use some simple timing tools and a Google Sheets spreadsheet
to identify a bottleneck in our traveling salesperson problem code that will give us 
a reduction in cost of **two orders of magnitude**.

![TSP Guava Solution scaling results - initial and pessimist algorithms](/images/tsp-guava-initial-pessimist.png)

<a name="graphs"></a>
## The Graphs We Are Solving

Let's start by having a look at some of the graphs we will be solving,
and the representation of the problem.

<a name="viz-graphs"></a>
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
and the algorithm was able to compute solutions in a reasonable amount of time.

![TSP graph with 18 nodes](/images/graphviz_tsp_18.png)

**Shortest Route: [0, 3, 10, 6, 12, 5, 11, 2, 14, 8, 13, 4, 7, 1, 9]	Distance: 267.0**







