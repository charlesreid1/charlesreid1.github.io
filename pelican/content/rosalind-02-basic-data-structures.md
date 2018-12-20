Title: Basic Data Structures in Go
Date: 2018-12-19 20:00
Category: Rosalind
Tags: go, golang, rosalind, bioinformatics
Status: draft

## Basic Data Structures in Go

Continuing with our series of blog posts on what
we've been learning about Go in the process of solving
problems on Rosalind.info, this post will cover how 
some basic data structures work in Go, and how we
used each to solve problems from the Chapter 1 Rosalind
problems.

### Maps

The simplest way to describe a map is to say it is a
structure useful for storing key-value pairs.

Before we walk through what maps look like in Go, let's
talk about what a map is (in the data structure sense).
And to do that, it's useful to talk a bit about mathematical
functions and maps in the mathematical sense.

#### What is a map

The term "map" is taken from mathematics. A map is just a
relationship - a general term, but still useful. Most 
mathematics courses deal with functions, which are formally 
defined as **maps** from one set of numbers onto another,
such that one input corresponds to one output.

A (data structure) map, similarly, is a relationship between
two sets - a key set, and a value set. Each key corresponds
to only one value. 

Maps are typically stored under the hood as either a hash
map (which does not sort keys and has very fast O(1), or
constant time, operations) or a tree map (which sorts keys 
using a binary tree and has slower O(log N) operations).

#### Map notation in Go

In Go, map types are denoted `map[keyType]valueType`.

For example, to map strings to integers, we would use
a map of type `map[string]int`. 

We create a map variable by declaring its type:

```
var m map[string]int
```

However, this does not allocate any space for the map,
and trying to add keys to the map at this point would
result in an error.

We need to actually allocate space for the map. In Go,
you can allocate space for a map two ways: first, using
Go's built-in `make()` function; and second, by creating
and populating the map in one line.

#### Using `make()` with maps

To allocate space for a map, you can use the `make()`
function and pass it the map type. This will actually
create space in memory for the map, and allow you to 
add items or look up keys in the map.

```
var m map[string]int
m = make(map[string]int)
```

#### Creating and populating

If you want to create and populate the map in one line,
you can specify the type, then have trailing brackets
containing the items you want to add:

```
// Create an empty map
m := map[string]int{}
```

```
// Create and populate a map
m := map[string]int{"A":10, "T":15, "G":20, "C":25}
```

#### Zero values

One feature of maps that makes them really easy to work
with is, if you try and look up a key, and the key does
not exist in the map, the map will not raise an exception
(which Python does), it will return the zero value of 
the value type. 

For example, the zero value of the `int` type is 0, 
so if we create a map like `m := map[string]int{"A":10}`
and we then look up a key that isn't in the map, like 
`m["G"]`, Go will return 0.

Similarly, the zero value for booleans is false, so you
can utilize the zero value behavior to create a set data
structure using maps. By creating a `map[keyType]bool`
map, you can use the boolean value to indicate membership
of a key in the given set. Then, if you look up keys that
do not exist in the map, Go will return the zero value of
booleans by default, which will be false.

#### Example: Assembling kmer histogram

Here is an example using maps: this function assembles
a kmer histogram from a strand of DNA base pairs. To do
this, it loops over every codon in the DNA strand and
increments a counter in a map. Finally, this histogram
map is returned. (This function is useful for determining
the most frequent kmer.)

```go
// Return the histogram of kmers of length k 
// found in the given input
func KmerHistogram(input string, k int) (map[string]int,error) {

    result := map[string]int{}

    if len(input)<1 {
        err := fmt.Sprintf("Error: input string was not DNA. Only characters ATCG are allowed, you had %s",input)
        return result, errors.New(err)
    }

    // Number of substring overlaps
    overlap := len(input) - k + 1

    // If overlap < 1, we are looking
    // for kmers longer than our input
    if overlap<1 {
        return result,nil
    }

    // Iterate over each position,
    // extract the string,
    // increment the count.
    for i:=0; i<overlap; i++ {
        // Get the kmer of interest
        substr := input[i:i+k]

        // If it doesn't exist, the value is 0
        result[substr] += 1
    }

    return result,nil
}
```

### Strings


### Bit Vectors

