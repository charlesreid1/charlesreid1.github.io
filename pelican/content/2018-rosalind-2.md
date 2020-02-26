Title: Basic Data Structures in Go: Maps
Date: 2018-12-20 17:00
Category: Computational Biology
Tags: go, golang, rosalind, computational biology, bioinformatics, maps

## Basic Data Structures in Go: Maps

Continuing with our series of blog posts on what
we've been learning about Go in the process of solving
problems on Rosalind.info, this post will cover how 
some basic data structures work in Go, and how we
used each to solve problems from the Chapter 1 Rosalind
problems.

## Maps

The simplest way to describe a map is to say it is a
structure useful for storing key-value pairs.

Before we walk through what maps look like in Go, let's
talk about what a map is (in the data structure sense).
And to do that, it's useful to talk a bit about mathematical
functions and maps in the mathematical sense.

### What is a map

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

### Map notation in Go

In Go, map types are denoted `map[keyType]valueType`.

For example, to map strings to integers, we would use
a map of type `map[string]int`. 

We create a map variable by declaring its type:

```go
var m map[string]int
```

However, this does not allocate any space for the map,
and trying to add keys to the map at this point would
result in an error.

We need to actually allocate space for the map. In Go,
you can allocate space for a map two ways: first, using
Go's built-in `make()` function; and second, by creating
and populating the map in one line.

### Using `make()` with maps

To allocate space for a map, you can use the `make()`
function and pass it the map type. This will actually
create space in memory for the map, and allow you to 
add items or look up keys in the map.

```go
var m map[string]int
m = make(map[string]int)
```

### Creating and populating

If you want to create and populate the map in one line,
you can specify the type, then have trailing brackets
containing the items you want to add:

```go
// Create an empty map
m := map[string]int{}
```

```go
// Create and populate a map
m := map[string]int{"A":10, "T":15, "G":20, "C":25}
```

### Zero values

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

### Easy iterating over maps

It is easy to iterate over maps using the `range` keyword
in Go, which will return the keys (optionally, both keys 
and values) of the map in a loop:

```go
var m map[string]int{
        "ABC":10, 
        "DEF":20, 
        "GHI":30
}

for k,v := range m {
    fmt.Println("Key:",k," --> Value:",v)
}
```

## Example: Assembling kmer histogram

Here is an example using maps: this function assembles
a kmer histogram from a strand of DNA base pairs. To do
this, it loops over every codon in the DNA strand and
increments a counter in a map. Finally, this histogram
map is returned. (This function is useful for determining
the most frequent kmer.)

Here's the whole function that helps solve Rosalind problem
BA1B. We'll look at it piece by piece below: 

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

### Function Walkthrough

The first thing you'll notice is the comment style:
there is a comment right before each function, which
is common practice in Go, because comments that come
before a function are picked up by `godoc` (the Go
documentation tool) and turned into documentation.

```go
// Return the histogram of kmers of length k 
// found in the given input
func KmerHistogram(input string, k int) (map[string]int,error) {
```

Go has internalized the idea that comments are a part
of the documentation, so comments don't need to be 
formatted in any special way (like `/// this` or `/** this */`
business) to end up being picked up by godoc.

Next, we create an empty map (kmer strings to integer
frequency counters) and stride over the entire input string
with a window the size of the kmers we are interested in,
adding or incrementing each corresponding counter in the map
as we go.

The overlap variable is the number of possible kmers of length
`k` in the entire input string, which requires a bit of algebra
to gt the indices right:

```go
    // Number of substring overlaps
    overlap := len(input) - k + 1
```

The for loop utilizes Go's slice notation to take a slice of
the string (which does not require creating or duplicating any
string data), and uses the extracted kmer as a key to add or 
increment the counter: 

```go
    // Iterate over each position,
    // extract the string,
    // increment the count.
    for i:=0; i<overlap; i++ {
        // Get the kmer of interest
        substr := input[i:i+k]

        // If it doesn't exist, the value is 0
        result[substr] += 1
    }
```

This is where the behavior of maps for non-existent keys comes
in handy - in Go, if you ask for a key that does not exist
in the map, the map will return the zero value of the specified
type. 

This statement:

```go
        result[substr] += 1
```

can also be written as:

```go
        result[substr] = result[substr] + 1
```

So, the first time a kmer (stored in `substr`) is encountered, the
kmer will not exist as a key in the map, and the key lookup on the 
right hand side will return 0, incrementing the counter to 1
the first time the kmer is encountered.

Subsequent times the kmer is encountered, the value will be found 
and substituted on the right side so it will be incremented by 1.

Finally, when we return from the function, we can use a Python-like
syntax of returning multiple values separated by commas, yet
another great feature of Go: 

```go
    return result,nil
}
```

By convention, the return types of functions will include an error type 
at the very end, so if you had a function named `ExampleFunction` that 
returned three integers, the function definition would look like this:

```go
func ExampleFunction() (int, int, int, error) {
    ...    
}
```

Additionally, we also see from the function's return statement
above that we can use the reserved keyword `nil` to set a variable
to a null value, and that the convention is to return `nil` in place
of the error, so that in the calling function we can set up a structure
like this:

```
a, b, c, err := ExampleFunction()

if err != nil {
    err := "Please read this important message"
    return -1,-1,-1,errors.New(err)
}
```

## Summary

Maps are my favorite data structure, so I'm glad that they're
easy to use in Go. Some important points about using
maps in Go:

* Declaring a variable as a map type does not allocate any space
  for the map; saying `var m map[keyType]valueType` and then 
  trying to access keys will cause an exception.

* To allcoate space for a map, use `make(map[keyType]valueType)` 
  or instantiate with the `{}` notation, like 
  `m := map[keyType]valueType{"asdf":1}`

* To ask for a key, use the square bracket notation. To set a value
  for a key, use the square bracket notation on the left and assign
  a value on the right: `m[my_key] = my_value`

* Asking for missing keys will return the zero value of whatever
  type the map values are. 

* Iterating over key-value pairs in a map using a for loop is easy
  using the built-in `range` keyword.


## Addendum: Check if a Key is in a Map

Because of the default behavior of maps, where they return a zero value for
keys that do not exist in the map, it is not immediately obvious how to
differentiate between the case where a key is in a map already and has a zero
value, versus the case where the key does not yet exist in the map and the zero
value is only being returned because the key can't be found.

To resolve this, we can use two Go features: error-checking, and the underscore - 
a variable that serves as a one-way sink for information, and serves a similar
purpose to the underscore in Python.

First, we mentioned above that various operations that can return errors will return
an error type as the last return type, along with any other return values.
This includes the operation of accessing a key. To assign the value and the error
to variables at once:

```go
v, err := m[my_key]
```

Now, to check if the key exists in the map, we are only concerned with the variable
`err` and we don't really need the variable `v`. Instead of assigning `v` to a variable
that we never use, and then having the Go compiler complain about it, we can use the
underscore as a placeholder:

```go
_, err := m[my_key]
```

Now, we just add a check for whether `err` is nil, and voila, we have our check of
whether a key is in the map or not:

```go
_, err := m[my_key]

if err != nil {
    // This key is missing from the map

} else {
    // This key already exists in the map

}
```

