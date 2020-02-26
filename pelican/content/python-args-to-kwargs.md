Title: Python: From Args to Kwargs
Date: 2020-02-25 16:00
Category: Python
Tags: python, programming, arguments, functions, methods, parameters

## Table of Contents

* [Overview](#overview)
* [The Easy Way: locals()](#the-easy-way-locals)
* [When locals() Won't Work: Getting a Method Signature Programmatically](#when-locals-wont-work-getting-a-method-signature-programmatically)
* [Args to Kwargs: Parameter Extraction from Decorator](#args-to-kwargs-parameter-extraction-from-decorator)

## Overview

In this short blog post, we talk about how and when you can take a method signature
that defines input positional arguments by name, like this:

```text
def foo(arg1, arg2, arg3):
    pass
```

and write code that will return a dictionary containing a keyword arguments-like structure:

```text
>>> foo('red', 'blue', 'green')
{
    'arg1': 'red',
    'arg2': 'blue',
    'arg3': 'green'
}
```

We will cover an example of writing a decorator that utilizes input arguments from both
the decorator and from the function it wraps, and how to keep all of that information
straight.

## The Easy Way: `locals()`

We'll start with the easiest possible wyay to turn args into kwargs: `locals()`. The `locals()`
function is one of the built-in methods provided by Python:

```text
>>> print(help(locals))

Help on built-in function locals in module builtins:

locals()
    Return a dictionary containing the current scope's local variables.

    NOTE: Whether or not updates to this dictionary will affect name lookups in
    the local scope and vice-versa is *implementation dependent* and not
    covered by any backwards compatibility guarantees.
```

This is a straightforward way to get a dictionary of input argument names mapping to
the values provided by the user:

```text
>>> def foo(arg1, arg2, arg3):
...     print(locals())
...
>>> foo('asdf', 'qwerty', 'oioioioi')
{'arg3': 'oioioioi', 'arg2': 'qwerty', 'arg1': 'asdf'}
```


## When `locals()` Won't Work: Getting a Method Signature Programmatically

Sometimes, `locals()` won't get you what you need - like when you're decorating a function,
and you don't have the original method signature.

In that case, you can still use a function handle and get the original positional argument
names from the function signature.

In Python, the signature of a method can be obtained using the `inspect` module's
`signature()` method, which can be passed a function:

```text
>>> import inspect
>>> def foo(arg1, arg2, arg3):
...      pass
...
>>> print(inspect.signature(foo))
(arg1, arg2, arg3)
```

The `_parameters` attribute of the signature will yield an ordered list of parameters in the
method signature, which is equivalent to the variable names that are used in the method
definition (`arg1`, `arg2`, and `arg3` in the example `foo()` function above):

```text
>>> print(list(inspect.signature(foo)._parameters))
['arg1', 'arg2', 'arg3']
```

## Args to Kwargs: Parameter Extraction from Decorator

We can use this to get the original variable names from a function handle, even if we don't
have its original method signature (i.e., if we're a decorator and are just passed the function).

Here is an example of a decorator that extracts positional arguments from the function it
decorates (and prints them out!):

```python
import inspect

def real_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        # This is where the interesting stuff starts!
        # We have a handle to a function that we're
        # decorating, but we don't have its original
        # method signature.
        # No sweat. Turn positional args into augmented
        # kwargs!
        func_kwargs = {}
        sig = inspect.signature(wrapper)
        for i, p in enumerate(list(sig._parameters)):
            try:
                func_kwargs[p] = args[i]
            except IndexError:
                # Unspecified positional argument
                # (using default value)
                pass
        
        print(f"wrapper extracted the following params: {func_kwargs}")
        func(*args, **kwargs)

    return wrapper

# don't forget to top it off
# by decorating a simple function
# and calling it if script is run
@real_decorator
def foo(arg1, arg2, arg3):
    print("hello world!")

if  __name__=="__main__":
    foo('asdf', 'qwerty', 'wioioioio')
```

And when run, the result is:

```text
$ py five.py
wrapper extracted the following params: {'arg1': 'asdf', 'arg2': 'qwerty', 'arg3': 'wioioioio'}
hello world!
```



