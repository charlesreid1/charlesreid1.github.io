Title: Graphs for Bioinformatics, Part 2: Finding Eulerian Paths
Date: 2019-05-07 16:00
Category: Computational Biology
Tags: go, golang, rosalind, computational biology, bioinformatics, euler, recursion, backtracking, graphs, algorithms, hamiltonian, eulerian

# Table of Contents

* [The Context: de Bruijn Graphs](#the-context-de-bruijn-graphs)
* [Assembling the de Bruijn Graph](#assembling-the-de-bruijn-graph)
    * [Directed Graph Representation: Adjacency List](#directed-graph-representation-adjacency-list)
    * [A Quick Example](#a-quick-example)
    * [Python vs. Go](#python-vs-go)
    * [Directed Graph Class: Python Implementation](#directed-graph-class-python-implementation)
* [Checking for Eulerian Paths and Cycles](#checking-for-eulerian-paths-and-cycles)
* [Algorithm Building Blocks](#algorithm-building-blocks)
    * [Depth First Search](#depth-first-search)
    * [Kosaraju's Algorithm: Connected Components](#kosarajus-algorithm-connected-components)
* [Finding the Eulerian Path or Cycle](#finding-the-eulerian-path-or-cycle)
    * [Hierholzer's Algorithm: Finding Euler Cycles](#hierholzers-algorithm-finding-euler-cycles)
    * [Hierholzer's Algorithm: Finding Euler Paths](#hierholzers-algorithm-finding-euler-paths)
* [Final Code](#final-code)

<br />
<br />

# The Context: de Bruijn Graphs

In [Part 1 of this post](https://charlesreid1.github.io/graphs-for-bioinformatics-part-1-de-bruijn-graphs-hamiltonian-paths-and-eulerian-paths.html)
we discussed a data structure called a de Bruijn graph and covered its application
to genome assembly. To summarize, a de Bruijn graph is a type of graph that represents
a set of k-mers as a set of directed edges on a graph, connecting the k-mer's (k-1)-mer prefix
(the source vertex) to the k-mer's (k-1)-mer suffix (the destination vertex).

As an example, if $k = 5$, we can represent the k-mer "AAGCT" as an edge connecting the vertex
`AAGC` to the vertex `AGCT`.

The de Bruijn graph is used to solve a set of problems on [Rosalind.info](https://rosalind.info),
a website with bioinformatics programming challenges, as part of working through the
textbook [Bioinformatics Algorithms: An Active Learning Approach](http://bioinformaticsalgorithms.com/)
and its associated website ([Rosalind.info](https://rosalind.info)).

# Assembling the de Bruijn Graph

The problems from Rosalind.info that require the use of a de Bruijn graph come from
Chapter 3. These problems generally give the user either a list of k-mers (to assemble
into a de Bruijn graph, as in problem [BA3E](http://rosalind.info/problems/ba3e/)) 
or a long sequence of DNA (which can be turned into a list of
k-mers and assembled into a de Bruijn graph, as in problem [BA3D](http://rosalind.info/problems/ba3d/)).

If we are starting with a long string of DNA, we can run through the entire string
and extract k-mers using a sliding window. For a string of DNA of length $d$, this procedure
will create $d - k + 1$ k-mers.

## Directed Graph Representation: Adjacency List

The de Bruijn graph is a directed graph. To represent this
graph in memory, we utilize an adjacency list data structure.
An adjacency list is a key-value lookup table (implemented using
a hash map) wherein each _source vertex_ in the graph is a key 
in the lookup table, and the corresponding value is a list of
all _destination vertices_ (all vertices that have a directed
edge starting from the source vertex and ending at that vertex).

A Python dictionary can be used to implement the adjacency list
hash table. The dictionary keys are the source vertices (or rather,
their string labels), and the dictionary values are a list of 
destination vertices (a list of their string labels).

Thus, the graph `AA -> BB -> CC -> DD` would be represented with
the hash table:

```
adjacency_list['AA'] = ['BB']
adjacency_list['BB'] = ['CC']
adjacency_list['CC'] = ['DD']
```

(Notice from this example that the keys of the adjacency list
gives a list of _source vertices only_, to get all vertices we
need to look at the values of the adjacency list too.)

## A Quick Example

As a simple example, consider the de Bruijn graph formed from
the DNA string `AAGATTCTCTAC` and $k = 4$.

This is first turned into a bag of $d - k + 1 = 9$ 
4-mers (our edges):

```
Sequence:   AAGATTCTCTAC
4-mers:     AAGA
             AGAT
              GATT
               ATTC
                TTCT
                 TCTC
                  CTCT
                   TCTA
                    CTAC
```

Next, we also create a bag of $d - k + 1 = 10$ 
3-mers (vertices):

```
Sequence:   AAGATTCTCTAC
3-mers:     AAG
             AGA
              GAT
               ATT
                TTC
                 TCT
                  CTC
                   TCT
                    CTA
                     TAC
```

Now we can iterate over every 4-mer edge, find its
prefix 3-mer and suffix 3-mer, and create a corresponding
entry in the adjacency list hash table.

The list of edges looks like this:

```
AAG -> AGA
AGA -> GAT
ATT -> TTC
CTA -> TAC
CTC -> TCT
GAT -> ATT
TCT -> CTA,CTC
TTC -> TCT
```

The corresponding dictionary should look like this:

```
adjacency_list['AAG'] = ['AGA']
adjacency_list['AGA'] = ['GAT']
adjacency_list['ATT'] = ['TTC']
adjacency_list['CTA'] = ['TAC']
adjacency_list['CTC'] = ['TCT']
adjacency_list['GAT'] = ['ATT']
adjacency_list['TCT'] = ['CTA','CTC']
adjacency_list['TTC'] = ['TCT']
```

## Python vs Go

Now that we're ready to implement a directed graph object
and populate it using the data given in the problem, we 
have to make the difficult choice of what language we
want to use to implement the directed graph.

We have covered our use of the Go programming language 
for Rosalind.info problems before (we have previously 
covered recursion for Chapter 2 problems in 
[Part 1](https://charlesreid1.github.io/recursive-backtracking-in-go-for-bioinformatics-applications-1-counting-variations.html),
[Part 2](https://charlesreid1.github.io/recursive-backtracking-in-go-for-bioinformatics-applications-2-generating-variations.html),
and [Part 3](https://charlesreid1.github.io/recursive-backtracking-in-go-for-bioinformatics-applications-3-go-implementation-of-backtracking.html)
of another post, and we also wrote [this post](https://charlesreid1.github.io/learning-bioinformatics-with-go-and-rosalind.html)
on our impression of Go and its usefulness in
bioinformatics.

We are also implementing all of the solutions to the
Rosalind.info problems in our Go libarary, [go-rosalind](https://github.com/charlesreid1/go-rosalind)
(see [corresponding documentation on godoc.org](https://godoc.org/github.com/charlesreid1/go-rosalind/rosalind)).

**However,** we have learned the hard way that Go requires
a lot of boilerplate code (boilerplate code that is necessary,
mind you, because all of that boilerplate will eventually
morph into something problem-specific).

This all means that Go is a very cumbersome language to use
to get an algorithm prototype up and running.

Python, on the other hand, is a very easy language for
prototyping and has plenty of handy built-in functions
and modules that make prototyping an algorithm far 
easier and faster than doing it in Go.

Our strategy, therefore, is to prototype our algorithm
and corresponding graph object in Python, get the
algorithm working and tested, then convert the code 
to Go when we are finished.

## Directed Graph Class: Python Implementation

Note that while we could simply use the dictionary object
itself as the graph data structure, this is somewhat
inelegant, and we would like instead to define a class
to bundle related behavior and data together.

We implement the directed graph by defining an `AdjacencyGraph`
class. This is just a glorified wrapper around the ajacency
list dictionary, with some extra methods.

We start by defining the class (it inherits from `object` so
it has no parent type):

```
class AdjacencyGraph(object):
    """Directed graph stored using an adjacency list"""
    def __init__(self):
        """Constructor"""
        self.adj = {}
        self.dfs_started = False
```

The constructor just initializes an empty adjacency list dictionary.

We also define two built-in methods for convenience:
`__str__` for the string representation of the graph 
(so we can pass the graph object to `print()`), and
`__len__` for getting the number of (source) vertices 
on the graph.

```
    def __str__(self):
        """String representation"""
        s = []
        for source in self.adj.keys():
            sinks = self.adj[source]
            for sink in sinks:
                m = "%s -> %s\n"%(source,sink)
                s.append(m)
        return "".join(s)

    def __len__(self):
        """Number of vertices on graph"""
        s = set()
        for source in self.adj.keys():
            s.add(source)
            for sink in self.adj[k]:
                s.add(sink)
        return len(s)
```

Next, we define some basic functionality useful for all graphs:

* Getting the in-degree and out-degree of a vertex

```
    def in_degree(self,u):
        n = 0
        for v in self.adj.keys():
            sinks = self.adj[v]
            if u in sinks:
                n += 1
        return n

    def out_degree(self,u):
        if u in self.adj.keys():
            return len(self.adj[u])
        else:
            return 0
```

We also define a generator for creating vertices:

```
    def vertices(self):
        vertices = set()
        for k in self.adj.keys():
            vertices.add(k)
            for m in self.adj[k]:
                vertices.add(m)
        for v in vertices:
            yield v

    def n_vertices(self):
        return len(self)

    def n_edges(self):
        n = 0
        for source in self.adj.keys():
            try:
                n += len(self.adj[source])
            except:
                # in case value is None
                pass
        return n

    def get_neighbors(self,u):
        """Get all neighbors of node u"""
        # Note: neighbors are stored in
        # sorted order
        if u in self.adj.keys():
            return self.adj[u]
        else:
            return []
```

Finally, we add a method `add_edge()` that allows us
to create an edge from vertex u to vertex v (and add
the vertices to the graph if either do not yet exist
on the graph).

For convenience, we maintain the adjacency list values
(the list of destination vertices) in lexicographic
order.

```
    def add_edge(self, u, v):
        """Add an edge from u to v"""
        # For each source vertex:
        if u in self.adj.keys():

            # Get existing sink list
            t = self.adj[u]

            # Append to it
            t.append(v)

            # Keep list of sinks sorted
            # (lexicographic string sorting)
            t.sort()

            # Create the new edge 
            # from source to sink
            self.adj[u] = t

        else:
            # Initialize the list of sinks (v)
            # for the given source (u)
            self.adj[u] = [v]
```

Now, to assemble the de Bruijn graph, we can iterate
over every k-mer edge, form the prefix and suffix vertices,
and call the `add_edge()` function on the graph.

# Checking for Eulerian Paths and Cycles

To recap Eulerian paths versus Eulerian cycles (discussed in
[Part 1 of this post](https://charlesreid1.github.io/graphs-for-bioinformatics-part-1-de-bruijn-graphs-hamiltonian-paths-and-eulerian-paths.html):

* An Eulerian path is a path that visits every edge of a given graph exactly once.
* An Eulerian cycle is an Eulerian path that begins and ends at the ''same vertex''.

According to Steven Skienna's <u>Algorithm Design Handbook</u>,
there are two conditions that must be met for an Eulerian path or
cycle to exist. These conditions are different for undirected graphs
versus directed graphs.

**Undirected graphs:** 

* An undirected graph contains an Euler **cycle** iff
  (1) it is connected, and (2) each vertex is of even
  degree.

* An undirected graph contains an Euler **path** iff (1)
  it is connected, and all but two vertices are of even
  degree. These two vertices will be the start and end
  vertices for the Eulerian path.

**Directed graphs:**

* A directed graph contains an Euler cycle iff (1) it is
  strongly-connected, and (2) each vertex has the same
  in-degree as out-degree

* A directed graph contains an Euler path iff (1) it is
  connected, and (2) all vertices except two (x,y) have
  the same in-degree as out-degree, and (x,y) are
  vertices with in-degree one less than and one more
  than out-degree

# Algorithm Building Blocks

Algorithm to find Eulerian paths/cycles consists of several steps using several algorithms.

Undirected graphs are the simpler case; directed graphs are more complicated.

## Depth First Search

To perform a DFS on a directed graph, implement two functions:

1. Write a DFS function that takes a graph as an input argument and that visits each node of the
   graph in a depth-first search.

2. Write a visitation function that takes a node as an input argument and that performs some action
   on the node. This visitation function is called by the DFS function on each node that it visits.

## Kosaraju's Algorithm: Connected Components

On an undirected graph, can use Fleury's Algorithm
to follow edges (classify edges as bridge or non-bridge,
then leave bridges for last).

On a directed graph, we have twice the amount of work:
we are not just checking that all vertices are reachable
from a given vertex, we are also checking that all vertices
can also reach that vertex.

# To Be Continued...

In the next part of this post, we will start with the slightly simpler case of finding an Euler cycle
(which has no start or end vertices). Then we will show how finding the Euler path is actually a special
case of finding the Euler cycle.

First, we will use [Hierholzer's
Algorithm](https://charlesreid1.com/wiki/Graphs/Euler_Circuit#Directed_Graphs:_Hierholzer.27s_Algorithm)
to find Euler cycles (this is the simpler case). Order does not matter because it is a cycle;
Hierholzer's algorithm is used to find the Euler cycle.

Next, we will modify the above algorithm to find Euler paths. This requires keeping track of
the start and end candidate nodes. We verify only one each; we complete the cycle by adding an edge.
Once we find the cycle, we remove the edge. Finally, we rearrange the cycle to have the correct
start and end nodes.

Stay tuned for Part 3...
