Title: A Few of My Favorite PEPs
Date: 2019-02-11 12:00
Category: Python
Tags: python, pep, computer science, programming

## Table of Contents

* [What's your favorite PEP?](#fav)
* [PEP 0](#p0)
* [PEP 8](#p8)
* [PEP 20](#p20)
* [PEP 3099](#p3099)
    * [Addendum: 2 to 3 Changes](#2to3)
* [PEP 202](#p202)
* [All the PEPs on Github](#gh)

<br />
<br />

<a name="fav"></a>
## What's your favorite PEP?

PEPs, or **Python Enhancement Proposals**, are documents in which
features, additions, or general ideas are proposed as additions
to the core Python language.

As a Python user, we believe it's important to ask questions like this.

Picking a "favorite PEP" is not just about having a ready and clever
answer to a question you might expect in a technical interview;
the PEP documents really _are_ important, and really _do_ shape 
where Python is today and where it will be in the future.

So let's look at a few of our favorite PEPs.


<a name="p0"></a>
## PEP 0: The PEP Index

PEP0 - the easiest answer to the question, "what's your favorite PEP?"

[PEP 0 - Index of Python Enhancement Proposals (PEPs)](https://www.python.org/dev/peps/)
lists all PEPs, including PEPs about PEPs, accepted PEPs, open PEPs,
finished PEPs, informational PEPs, and abandoned PEPs.

This is also a good place to search for a keyword or browse PEPs.

This PEP is the favorite of people who love enumerations, library card catalogs,
biblical genealogies, and litanies.


<a name="p8"></a>
## PEP 8: The Python Style Guide

[PEP 8](https://www.python.org/dev/peps/pep-0008/)
covers the recommended Python style.
It is a surprisingly quick read.

This PEP dishes "official" opinions about 
controversial topics such as:

- tabs or spaces (spoiler: ***spaces***)
- line width
- whitespace
- naming conventions for variables, classes, and modules

This PEP is the chosen favorite of those programmers who keep their
crayons organized in the correct color order.


<a name="p20"></a>
## PEP 20: The Zen of Python

[PEP 20](https://www.python.org/dev/peps/pep-0020/) contains
20 aphorisms that compose the Zen of Python - only 19 of which
are contained in the PEP...

Also available from Python via:

```
>>> import this
```

Many of the aphorisms in PEP 20 come in pairs.

The first seven alone compose an excellent philosophy of programming.
Six symmetric rules:

```text
Beautiful is better than ugly.

Explicit is better than implicit.

Simple is better than complex.

Complex is better than complicated.

Flat is better than nested.

Sparse is better than dense.
```

The seventh, one of the principal ideas behind Python:

```text
Readability counts.
```

The next pair of aphorisms is important to our own style of programming:

```text
Special cases aren't special enough to break the rules.

Although practicality beats purity.
```

The latter aphorism is an acknowledgement that, ultimately, programming
is a means to an end, and Python (or whatever programming language you use)
should not _get in the way_ of reaching that end - especially not for the
sake of some abstract principle or theory. 

PEP 20 weighs in on errors:

```text
Errors should never pass silently.

Unless explicitly silenced.
```

Slightly perplexing:

```text
In the face of ambiguity, refuse the temptation to guess.
```

More pairs:

```text
There should be one-- and preferably only one -- obvious way to do it.

Although that way may not be obvious at first unless you're Dutch.
```

From the [Wikipedia page on Guido van Rossum](https://en.wikipedia.org/wiki/Guido_van_Rossum):

> Guido van Rossum is a Dutch programmer...

```text
Now is better than never.

Although never is often better than *right* now.
```

That last one sounds like an excuse for procrastination.

```text
If the implementation is hard to explain, it's a bad idea.

If the implementation is easy to explain, it may be a good idea.
```

Finally, the last aphorism covers the reason you never see 
`from module import *`:

```text
Namespaces are one honking great idea - let's do more of those!
```

Namespaces, in this case, come from importing everything in 
a Python package into a particular variable name - like 
`import itertools` or `import numpy as np`.

It turns out that, yes, in fact, namespaces are a great idea!


<a name="p3099"></a>
## PEP 3099: Things That Will Not Change in Python 3000

We can't really decide what we enjoy most about [PEP 3099](https://www.python.org/dev/peps/pep-3099/).
Maybe it's the fact that it does the opposite of what most 
proclamations of a new major version do, which is, to say
what new features it will _not_ have.
Maybe it's the way the language's creators demonstrate how well
they have learned from the mistakes of others who adopt
the "Burn it to the ground and rewrite from scratch"
philosophy. Or maybe it's the delightful nostalgia of 
"Python 3000".

In any case, PEP 3099 is an instructive read, because any feature
that will explicitly be kept during a major version bump is clearly
either (a) useful, (b) important, or (c) both. Additionally, it 
gives some insight into the design decisions made when Python
was implemented ("Why does Python do X this way, instead of 
some other easier way?").

Not only that, you also get to walk through a graveyard of
abandoned (but still interesting) ideas, and the links given
in the PEP to the Python mailing list can provide additional
useful information.


<a name="2to3"></a>
## Addendum: PEPs Affecting 2 to 3 Changes

In contrast to PEP 3099, which contains a list of all the things
that _did not_ change in Python 3, there were a large number of
PEPs that _did_ cause Python 3 to behave differently from Python 2.

* [PEP 237](https://www.python.org/dev/peps/pep-0237): Unified long integers and integers
* [PEP 238](https://www.python.org/dev/peps/pep-0238): Changed the division operator
* [PEP 412](https://www.python.org/dev/peps/pep-0412): Key-sharing dictionary
* [PEP 428](https://www.python.org/dev/peps/pep-0428): Object-oriented filesystem paths
* [PEP 435](https://www.python.org/dev/peps/pep-0435): Adding enum type
* [PEP 448](https://www.python.org/dev/peps/pep-0448): Unpacking
* [PEP 450](https://www.python.org/dev/peps/pep-0450): Adding stats to standard library
* [PEP 498](https://www.python.org/dev/peps/pep-0498): Literal string interpolation
* [PEP 515](https://www.python.org/dev/peps/pep-0515): Underscores in numeric literals
* [PEP 3101](https://www.python.org/dev/peps/pep-3101): Advanced string formatting
* [PEP 3102](https://www.python.org/dev/peps/pep-3102): Keyword-only arguments
* [PEP 3105](https://www.python.org/dev/peps/pep-3105): Make print a function
* [PEP 3111](https://www.python.org/dev/peps/pep-3111): User input in Python 3000
* [PEP 3114](https://www.python.org/dev/peps/pep-3114): Renaming `next()` to `__next__()`
* [PEP 3135](https://www.python.org/dev/peps/pep-3135): Super behavior


<a name="p202"></a>
## PEP 202: List Comprehensions

Of course, picking your favorite PEP can also be an opportunity
to make a statement about your favorite language feature of Python,
since many of Python's most useful language features got their start 
as PEPs.

For us, list comprehensions (covered in [PEP 202](https://www.python.org/dev/peps/pep-0202/))
area clear winner in any competition of most useful language features. 
List comprehensions are a way of shortening for loop syntax, making it
much easier to perform map and filtering operations. Some examples
from PEP 202:

```
>>> print([i for i in range(20) if i%2 == 0])
[0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

>>> nums = [1, 2, 3, 4]

>>> fruit = ["Apples", "Peaches", "Pears", "Bananas"]

>>> print [(i, f) for i in nums for f in fruit]
[(1, 'Apples'), (1, 'Peaches'), (1, 'Pears'), (1, 'Bananas'),
 (2, 'Apples'), (2, 'Peaches'), (2, 'Pears'), (2, 'Bananas'),
 (3, 'Apples'), (3, 'Peaches'), (3, 'Pears'), (3, 'Bananas'),
 (4, 'Apples'), (4, 'Peaches'), (4, 'Pears'), (4, 'Bananas')]

>>> print([(i, f) for i in nums for f in fruit if f[0] == "P"])
[(1, 'Peaches'), (1, 'Pears'),
 (2, 'Peaches'), (2, 'Pears'),
 (3, 'Peaches'), (3, 'Pears'),
 (4, 'Peaches'), (4, 'Pears')]

>>> print([(i, f) for i in nums for f in fruit if f[0] == "P" if i%2 == 1])
[(1, 'Peaches'), (1, 'Pears'), (3, 'Peaches'), (3, 'Pears')]

>>> print([i for i in zip(nums, fruit) if i[0]%2==0])
[(2, 'Peaches'), (4, 'Bananas')]
```

List comprehensions enable code to be short but expressive, 
brief but elegant. Brevity is the soul of wit, after all.

<a name="gh"></a>
## All the PEPs on Github

[All the PEPs are available on Github.](https://github.com/python/peps)


