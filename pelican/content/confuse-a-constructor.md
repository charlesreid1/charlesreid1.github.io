Title: Confuse-A-Constructor: When Class A's Constructor Returns Objects of Type B
Date: 2020-02-22 13:00
Category: Python
Tags: python, constructor, computer science, object oriented programming

## Table of Contents

* [Confuse\-A\-Constructor](#confuse-a-constructor)
* [What is the constructor?](#what-is-the-constructor)
* [Rewiring the constructor to do\.\.\. weird stuff](#rewiring-the-constructor-to-do-weird-stuff)
* [A simple example class](#a-simple-example-class)
* [Adding a \_\_new\_\_ method](#adding-a-__new__-method)
* [When \_\_new\_\_ returns objects, not classes](#when-__new__-returns-objects-not-classes)
* [Moving beyond argparse](#moving-beyond-argparse)
* [Using \_\_new\_\_ in your patterns](#using-__new__-in-your-patterns)

## Confuse-A-Constructor

Today, we are going to confuse a constructor.

<iframe allowFullScreen="allowFullScreen" src="https://www.youtube.com/embed/1tsIxNci_dE?ecver=1&amp;iv_load_policy=1&amp;rel=0&amp;yt:stretch=16:9&amp;autohide=1&amp;color=red&amp;width=560&amp;width=560" width="560" height="315" allowtransparency="true" frameborder="0">
    <script type="text/javascript">function execute_YTvideo(){return youtube.query({ids:"channel==MINE",startDate:"2019-01-01",endDate:"2019-12-31",metrics:"views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,subscribersGained",dimensions:"day",sort:"day"}).then(function(e){},function(e){console.error("Execute error",e)})}</script>
</iframe>

## What is the constructor?

One of the first concepts encountered in object-oriented programming
is that of the _constructor_, the method that is run immediately after
an object is instantiated that configures and initializes the object.

In Python, a constructor is defined by the `__init__` function.
The constructor is not permitted to return a value, because
constructing a new instance of class A should result in an object
of type A. Returning something would just be confusing things.

But does it ever make sense for a constructor of class A to return
an object of type B? And if it does make sense, how do we go about
doing it?

## Rewiring the constructor to do... weird stuff

The answer lies in Python's `__new__` method, which is a method called
when a class is defined (not instantiated). The `__new__` method is
different from the `__init__` method, and does not do the same thing.

The `__new__` method for class A should only return the type of class A.
If `__new__` returns anything else, Python will not run the `__init__`
method for class A.

For example, suppose we want a wrapper class that transparently constructs
different kinds of objects conditionally - based on a configuration file,
or the state of a file, or some other condition. We want to construct an
object of type A and get back an object of type B, C, or D. How to do that?

First, let's look at how the `__new__` method works.

## A simple example class

Start with a simple example class:

```python
class A(object):

    def __init__(self, *args, **kwargs):
        print("Instance of class A created")

    def hello(self):
        print("Hello world")
```

Executing this gives:

```
In [3]: my_object = A()
Instance of class A created

In [4]: my_object.hello()
Hello world
```

## Adding a `__new__` method

Now let's look at a class A where we define the `__new__` method. This method
controls how the instantiation of objects of type A work, so we can do something
like limiting the creation of objects of type A to when a certain condition is
met:

```python
import random

def tossCoin():
    if random.random() < 0.5:
        return True
    else:
        return False

class A5050(object):
    def __new__(cls, *args, **kwargs):
        if not tossCoin():
            raise RuntimeError("Count not create instance")
        instance = super(A5050, cls).__new__(cls, *args, **kwargs)
        return instance

    def __init__(self, *args, **kwargs):
        print("Instance of class A5050 created")

    def hello(self):
        print("Hello world")
```

Now we can run this block of code:

```python
def make_a5050():
    try:
        my_object = A5050()
        my_object.hello()
    except RuntimeError:
        print("Better luck next time!")
```

It takes a few tries:

```text
In [9]: make_a5050()
Better luck next time!

In [10]: make_a5050()
Instance of class A5050 created
Hello world
```

The `__new__` method for the `A5050` class raises a runtime error
with a 50% probability. Otherwise, it calls the `__new__` method
of the parent class (`object`, which returns a class of type `object`).
We pass the same arguments and keyword arguments (args/kwargs) on to the
super class `__new__`, but we could optionally modify them here (say, add
a keyword, or check the state of a file, or etc.).

This is just an example of how the instantiation behavior of a class
can be modified before its constructor is even called by using the
`__new__` method.

## When `__new__` returns objects, not classes

In the above example, our `__new__` method returned the result of
a call to `__new__` of a parent class. What happens if `__new__`
returns something else?

First, repeating an important point made above: if `__new__` for a class
returns anything _other_ than that class type, then `__init__` will not 
be called for that class.

That means that the `__new__` method should _either_ return a class (if
returning the type of its parent class, like a normal `__new__` method
does), _or_ it should return an instantiated object.

Let's imagine that we want to create different instances of different
classes based on a command line flag passed to the script:

```python
class BaseClass(object):
    def hello(self):
        print("Hello world from class %s"%(self.__class__.__name__))

class B(BaseClass):
    pass

class C(BaseClass):
    pass

class D(BaseClass):
    pass

class A(object):
    def __new__(cls, args):
        if args.B:
            return B()
        elif args.C:
            return C()
        elif args.D:
            return D()
        else:
            raise RuntimeError("Could not create instance")

if __name__=="__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-B', action='store_true',
                        help='Return object of type B')
    parser.add_argument('-C', action='store_true',
                        help='Return object of type C')
    parser.add_argument('-D', action='store_true',
                        help='Return object of type D')
    
    args = parser.parse_args()

    a = A(args)
    print(type(a))
```

Now if we run this script and pass it different flags, we get
a variable `a` with different types:

```text
$ py wat2.py -h
usage: wat2.py [-h] [-B] [-C] [-D]

optional arguments:
  -h, --help  show this help message and exit
  -B          Return object of type B
  -C          Return object of type C
  -D          Return object of type D
```

Now try the three flags:

```text
$ py wat2.py -B
<class '__main__.B'>

$ py wat2.py -C
<class '__main__.C'>

$ py wat2.py -D
<class '__main__.D'>
```

## Moving beyond argparse

The example above shows how the constructor can use
argparse options to determine what kind of object
to return with `__new__`, but you can use other
types of conditions as well:

- using command line options (see argparse example above)
- using configuration file options
- using environment variable values
- checking status of a file or port
- checking whether internet connection is available

## Using `__new__` in your patterns

We have already covered the [Registry](#)
pattern in a prior blog post, but the
`__new__` method lends itself well to
all kinds of other patterns, including the
Singleton pattern and the Factory pattern.

There are some very useful patterns covered
in this Github repository: <https://github.com/faif/python-patterns>
