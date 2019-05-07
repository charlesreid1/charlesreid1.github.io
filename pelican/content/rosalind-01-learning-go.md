Title: Learning Bioinformatics with Go and Rosalind
Date: 2018-12-18 20:00
Category: Computational Biology
Tags: go, golang, rosalind, computational biology, bioinformatics

## Learning Go with Rosalind

### What is Rosalind?

Rosalind.info is a website with programming challenges, similar in spirit
to [Project Euler](https://charlesreid1.com/wiki/Project_Euler), but with
a focus on bioinformatics. 

Problems in the bioinformatics track are presented grouped by chapter,
with several problems per chapter. The problems are designed like a coding
competition, with problems providing structured input files and expecting
structured output from each calculation. Each time you solve a problem, a
unique input is generated, and you have a time limit in which to run your
code to solve the problem.

### What is Go?

Go is a programming language that is static, compiled, and concurrent.
It is essentially intended as a modern replacement to C and C++, and is
designed for more modern hardware, networks, and scale of code projects.

Go is a language that was invented in Google. It provides some very
powerful features, and its design for concurrency is the primary feature
that motivated me to learn Go. See 
[this Go blog post](https://blog.golang.org/concurrency-is-not-parallelism)
on "Concurrency is not parallelism" for a more in-depth discussion of
Go's concurrency design, and how that is different from (and more general
and more powerful than) parallelism.

## Initial Impression of Go

My initial impression of Go has been positive thus far.

### Syntax

The first thing about Go that we will remark on is the syntax - it 
is unusual because it reverses the order that most programming languages
use for variable and type declarations. 

For example, in Java, you declare an integer array like this:

```
public int[5] arr;
```

while in Go, you would declare an analogous data structure like this:

```
var arr [5]int
```

While this reversal is a bit confusing at first, it is different enough 
from other languages that it easily sticks in your head - which is actually
a welcome change from the stew of slightly-different-but-largely-overlapping 
syntax occurring across common programming languages.

Go also shares many of the features that make Python such an easy language
to use, including lack of semicolons (yay!) and a useful selection of built-in
methods. 

### Godoc

One of the handiest features of Go is `godoc`, a command-line utility that runs
a local web server at `http:8080` that serves up Go documentation. This includes
documentation for the standard Go library, as well as documentation for any
libraries found in the Go PATH.

### Environment Variables

Speaking of the Go PATH, one confusing thing about getting started with Go is
all of the environment variables that must be set for Go to find various things.

Basically, you need to have two directories for Go: the location of your Go tree,
and the directory where you store Go packages and executables.

* `$GOROOT` refers to the location of your Go tree. For example, this might be the
  directory `~/go`.

* `$GOPATH` refers to the location where your Go packages and executables are stored.
  For example, this might be `~/work`.

Both of these variables should be set in your `~/.profile`.

See [Go/Installing](https://charlesreid1.com/wiki/Go/Installing#Paths) on the 
charlesreid1 wiki for coverage of getting set up with Go.

### Arrays and Slices

The first concept in Go that threw me off was the concept of arrays versus slices.
This was principally due to the poor explanation and choice of examples given on the
Go blog post on how slices work.

Arrays are chunks of memory that are set aside to store contiguous slots for data.
To create an array, its size must be known in advance, making them less useful
in practice. To resize an array, a new array must be created, and the old array
copied into the new array.

Slices, on the other hand, can be thought of as tiny data structures
containing pointers to array data. Slices can easily be resized by changing the
data structure, without changing the underlying data.

There are also built-in `make()` and `copy()` functions, to allocate slices
that have a specified capacity (or none, in which case the slice has a variable 
size) and copy data from arrays to slices or from slice to slice.

The confusion around such a fundamental data type makes Go more difficult to learn
and to intuit about what's going on. While Go is clearly superior to C and Java
in many ways, it also has some unfortunate stumbling blocks in its most basic
data structure that many early learners are sure to have trouble with.

## Learning a New Language

One of the things that stood out to me while learning Go was how different it was
from learning a non-language systems technology (library) like Docker or docker-compose, 
or Ansible. 

When you are learning a second or third programming language, you generally have a
mental roadmap of concepts, and how they fit together and build upon each other.
Furthermore, you already know, before ever starting to learn the language, what
that roadmap of concepts generally looks like, from your prior learnings.

(If you pick up and compare any dozen books on various programming languages, 
you'll find certain core concepts that are repeated from book to book.)

Compare this with a technology like Ansible, an extremely powerful Python library
that is used for automation of IT and compute infrastructure. While extremely powerful,
Ansible is also extremely complex, and feels bewildering to learn because
it requires all users (including seasoned experts in Unix shell scripting), to 
re-learn an entirely new way of doing things using Ansible's system of modules 
and YAML syntax.

Ansible has no conceptual roadmap. The Ansible documentation moves somewhat
haphazardly through the many topics that must be covered but that don't fit
together.  Books that cover Ansible often follow the documentation's
organization, or have a similarly confused organization of concepts.
There is no denying it's a great piece of software, but it is very difficult
to reason about and teach compared to a computer language.

## Core Concepts

The first few Rosalind problems from Chapter 1
were an excellent warm-up to get to know Go,
since the tasks were relatively easy and the
main bit to work out was how to use the data
structure correctly, rather than the algorithm.

Three data structures that we ended up utilizing 
to solve the Chapter 1 challenges using Go were:

* Hash maps
* Strings
* Bit vectors

More coverage of how these data structures work in Go,
plus details of how we used them to solve Rosalind
probelms, to follow in the next blog post.

