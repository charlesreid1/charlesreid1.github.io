Title: Graphs for Bioinformatics, Part 1: de Bruijn Graphs, Hamiltonian Paths, and Eulerian Paths
Date: 2019-05-02 19:00
Category: Computational Biology
Tags: go, golang, rosalind, computational biology, bioinformatics, euler, recursion, backtracking, graphs, algorithms, hamiltonian, eulerian
Status: draft

# Table of Contents

* [The Context: Rosalind\.info](#the-context-rosalindinfo)
* [Graphs for Bioinformatics](#graphs-for-bioinformatics)
    * [Building a Kmer Graph (The Wrong Graph)](#building-a-kmer-graph-the-wrong-graph)
    * [Building a De Bruijn Graph (The Right Graph)](#building-a-de-bruijn-graph-the-right-graph)
    * [Transform the Problem: Hamiltonian Paths to Eulerian Paths](#transform-the-problem-hamiltonian-paths-to-eulerian-paths)
* [An Example](#an-example)
* [Back to DNA](#back-to-dna)

<br />
<br />

# The Context: Rosalind.info

To provide a bit of context for a discussion of Euler paths and Euler cycles:
starting around December, a group of us in the [Lab for Data Intensive Biology (DIB Lab)](http://ivory.idyll.org/lab/)
started working through the textbook [Bioinformatics Algorithms: An Active Learning Approach](http://bioinformaticsalgorithms.com/)
and the associated website, [Rosalind.info](https://rosalind.info).

Rosalind.info is a site that is similar in style to [Project Euler](https://projecteuler.net/),
a [familiar topic on this blog](https://charlesreid1.github.io/tag/project-euler.html).
Project Euler poses computationally challenging problems in the domain of mathematics.

Like Project Euler, the visitor is given one small example input and the corresponding 
correct output, and one large example input and corresponding output. Also like Project
Euler, the problems vary in how much computer science versus domain expertise is needed,
but they are largely focused on writing algorithms rather than on the science behind the
computations.

Unlike Project Euler, however, Rosalind.info does give plenty of hints (via the textbook,
if you have a copy), and sometimes even gives pseudocode for the algorithm. **The book is
required to get enough context to answer some of the Rosalind.info problems.**

# Graphs for Bioinformatics

The textbook focuses on different problems in each chapter. For example, Chapter 1 uses
the example of a string of DNA that marks where replication begins to introduce some
basic bioinformatics concepts and algorithms. Chapter 2 uses the concept of molecular
clocks to introduce motifs and motif-finding, the focus of most of the problems in
Chapter 2.

Chapter 3 focuses on the problem of genome assembly - how we assemble an entire genome
from short segments alone. In particular, the chapter focuses on de Bruijn graphs, 
which are graphs that, given a sequence of symbols drawn from an alphabet, are composed 
of edges (one for each **k-mer**, that is, a chunk of the sequence of length k),
and vertices (one for each k-mer prefix and k-mer suffix, connected by a directed edge
of the k-mer). We will cover more of the details of these graphs shortly.

## Building a Kmer Graph (The Wrong Graph)

The Bioinformatics Algorithm book starts with a general discussion of how to 
represent a sequence of DNA nucleotides using a graph. The idea they discuss 
initially (which is an obvious, but not necessarily good, one) is splitting
the sequence into k-mer chunks, like so:

```
      Sequence:   TAATGCCATGGGATGTT
      Pieces:     TAA 
                   AAT
                    ATG 
                     TGC
                      GCC 
                       CCA
                        CAT 
                         ATG
                          TGG 
                           GGG
                            GGA 
                             GAT
                              ATG 
                               TGT
                                GTT
```

and letting one k-mer be represented by one vertex. Then the sequence
above could be turned into the graph:

```
TAA -> AAT -> ATG -> TGC -> GCC -> CCA -> CAT -> ATG -> TGG -> GGG -> GGA -> GAT -> ATG -> TGT -> GTT
```

On this graph, every edge has the property that the first (k-1)
nucleotides of the destination match the last (k-1) nucleotides
of the source. 

If we did not know this sequence in advance, we could draw _every_
edge with that property - every time the last (k-1) characters of
a kmer match the first (k-1) characters of another kmer, an edge
is drawn between those two vertices. 

That graph would result in _many_ more edges than the graph shown above.

Furthermore, in theory, if each read sequence came from a single genome
and we had the entire genome covered by read sequences, a path through
the graph that visits every vertex (every k-mer) would yield the full
genome.

A path through a graph that visits every vertex once is called a 
**Hamiltonian path**.

Why is this hard? Because the problem of proving a Hamiltonian
path exists, let alone finding it, becomes very difficult for
large graphs.

## Building a De Bruijn Graph (The Right Graph)

Nicolaas de Bruijn introduced (in 1946, in a paper entitled simply
["A combinatorial problem"](https://pure.tue.nl/ws/files/4442708/597473.pdf))
a new way of representing a sequence with a graph. He split a given
sequence into k-mers, as before, but instead of representing
each k-mer as a _vertex_ on the graph, he represented each 
k-mer as an _edge_ on the graph.

This type of graph is called a **de Bruijn graph**.

Specifically, for a DNA sequence, each k-mer from the sequence is
represented by an edge, where the source vertex
is that k-mer's (k-1)-nucleotide suffix and the destination vertex
is that k-mer's (k-1)-nucleotide prefix.

```
      Sequence:   TAATGCCATGGGATGTT
      Pieces:     TA  
                   AA
                    AT 
                     TG
                      GC 
                       CC
                        CA 
                         AT
                          TG 
                           GG
                            GG 
                             GA 
                              AT  
                               TG 
                                GT 
                                 TT
```

Now this sequence is written as the graph:

```
TA -> AA -> AT -> TG -> GC -> CC -> CA -> AT -> TG -> GG -> GG -> GA -> AT -> TG -> GT -> TT
```

so that the original breakup of the sequence into k-mers is still
represented, but now as edges rather than as vertices. That is, the 
k-mer `TAA` is represented by the edge `TA -> AA`.

## Transform the Problem: Hamiltonian Paths to Eulerian Paths

The change in the problem representation (kmers as vertices to kmers
as edges) changes the problem of finding the **Hamiltonian path** 
(a path through the graph that visits every _vertex_ exactly once) 
into the probelm of finding the **Eulerian path**
(a path through the graph that visits every _edge_ exactly once).

# An Example

Let's look at a slightly simpler example - the one de Bruijn was
originally considering - so we can see de Bruijn graphs in action
in a slightly simpler case.

In his 1946 paper ["A combinatorial problem"](https://pure.tue.nl/ws/files/4442708/597473.pdf),
de Bruijn describes the problem thus:

> Some years ago Ir. K. Posthumus stated an interesting conjecture
> concerning certain cycles of digits 0 or 1, which we shall call
> $P_n$ cycles. For $n = 1, 2, 3, \dots$, a $P_n$ cycle be an ordered
> cycle of $2^n$ digits 0 or 1, such that the $2^n$ possible ordered
> sets of $n$ consecutive digits of that cycle are all different.
> As a consequence, any ordered set of $n$ digits 0 or 1 occurs exactly
> once in that cycle.
>
> For example, a $P_3$ cycle is $00010111$, respectively showing the
> triples 000, 001, 010, 011, 111, 100, 100, which are all the possible
> triples indeed.

In this case, de Bruijn is discussing _complete_ de Bruijn graphs - he
constructs a de Bruijn graph of all possible 3-mers (our k-mers, $k = 3$),
and constructs a path through the graph that visits every edge of the
graph. Here is the sequence broken down as above:

```
      Sequence:   00010111
      Pieces:     00  
                   00
                    01
                     10
                      01
                       11
                        11
```

The alphabet here is binary: 0 and 1. 

This (seemingly simple) example is a bit confusing, but here's
what's going on: we have four vertices on the de Bruijn graph,
consisting of the 2-mers:

```
00
01
10
11
```

Now, if we draw an edge for every possible 3-mer, we would 
start with the 3-mer `000`, which is actually represented
by a self-edge from vertex `00` to vertex `00`, because the
prefix matches the suffix.

Similarly, the 3-mer `111` is represented by a self-edge
from vertex `11` to vertex `11`.

The other 3-mers are represented by their corresponding edges:
`001` is represented by the edge `00 -> 01`, `010` by the edge
`01 -> 10`, etc.

By drawing **every possible edge** (to represent every possible
3-mer), we assemble the **complete de Bruijn graph** (that is,
the de Bruijn graph containing vertices for all possible
2-mers connected by edges representing every possible 3-mer
in the given alphabet).

The sequence de Bruijn gives in his paper is an Euler path
through the _complete_ (de Bruijn) graph (that is, a path 
through the de Bruijn graph that visits every edge exactly 
once):

```
Sequence: 00010111

00 -> 00 -> 01 -> 10 -> 01 -> 11 -> 11
```

# Back to DNA 

Now the utility of the de Bruijn methodology is more clear:
if we can come up with fast, efficient algorithms to find
Euler paths on large graphs, we can transform the assembly 
problem (given fragments of a long sequence, reconstruct
the sequence) into the problem of finding an Eulerian path,
which is tractable even for large graphs.

Compare this with string matching algorithms utilizing
dynamic programming, which can cost $O(N^2)$ and make
genome assembly computationally infeasible.

