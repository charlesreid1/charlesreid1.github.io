Title: Python Patterns: The Registry
Date: 2020-02-20 22:22
Category: Python
Tags: python, programming, patterns, design patterns, registry, computer science

# Table of Contents

* [Overview](#overview)
* [What is the Registry Pattern?](#what-is-the-registry-pattern)
    * [The Registry Base Type](#the-registry-base-type)
    * [The Base Registered Class](#the-base-registered-class)
    * [Extending the Base Registered Class](#extending-the-base-registered-class)
    * [Seeing it in action](#seeing-it-in-action)
* [Examples](#examples)
    * [Example: Search Engine](#example-search-engine)
        * [Registry Subclasses](#registry-subclasses)
        * [Doctype Registry Base Type](#doctype-registry-base-type)
        * [Base Registered Doctype Class](#base-registered-doctype-class)
        * [Derived Registered Doctype Class](#derived-registered-doctype-class)
        * [Using the Registry](#using-the-registry)
* [Further Modifications](#further-modifications)
* [Summary](#summary)

# Overview

This post is a summary of a useful Python programming pattern called the Registry pattern.

The Registry pattern is a way of keeping track of all subclasses of a given class.

More details about this pattern are available at <https://github.com/faif/python-patterns>.

# What is the Registry Pattern?

Let's start with a common scenario: you have some kind of manager class that is
managing multiple related subclasses, and you are looking for a simpler way to
manage the subclasses.

The registry pattern creates a map of labels to class types, and allows you to
access a single registry common to all of those classes. The registry is updated
every time a new class is added.

This is useful for several situations, including these two examples:

- You want the manager class to iterate over every available subclass and call a
  particular method on each subclass
- You want to streamline a factory class, which takes an input label (like the name
  of a class) and creates/returns an object of that type

## The Registry Base Type

We start by defining a registry base type (or class). This class defines one behavior,
which is adding itself to the class registry. It creates a shared instance variable called
`REGISTRY` which is shared amongst all of the classes, and is also accessible via a class
method.

This is the base class; any class we want registered should inherit from this class.
It should also extend the `type` class, since it is itself a class type:

```python
class RegistryBase(type):

    REGISTRY = {}

    def __new__(cls, name, bases, attrs):
        # instantiate a new type corresponding to the type of class being defined
        # this is currently RegisterBase but in child classes will be the child class
        new_cls = type.__new__(cls, name, bases, attrs)
        cls.REGISTRY[new_cls.__name__] = new_cls
        return new_cls

    @classmethod
    def get_registry(cls):
        return dict(cls.REGISTRY)
```

The design here is subtle, but the details are important to understand how it works.

A few important things to note, progressing from top to bottom:

- The `REGISTRY` variable is defined outside the scope of any class methods, meaning it is a
  shared instance variable (a variable that is shared across all instances of `RegistryBase`);
  this is an example of the Borg pattern.

- The `RegistryBase` class defines `__new__`, not `__init__`; the `__new__` method is run when
  the class is defined, while `__init__` is run when the classs is instantiated. This ensures
  that any subclasses that inherit from `RegistryBase` add themselves to the registry when they
  are defined, not when they are instantiated.

- In the constructor, we store a reference to the current class using this line:

  ```
  new_cls = type.__new__(cls, name, bases, attrs)
  ```
   
  This creates a new class, but of type `type` (confusing, but basically it means we store
  a reference to this _**type**_ of object, not just a reference to a particular object).

  It is important to note that once we use the registry, the value that is returned is callable,
  and will create an object corresponding to that type.

- We define a `get_registry` method to return a copy of the registry; this must be decorated with
  a `@classmethod` decorator (not a `@staticmethod` decorator) so that it has access to the registry,
  which is a class instance variable.

**BONUS NOTE:** From prior experience, we have found it easiest to ignore the case of the
label (uppercase, lowercase, CamelCase, etc) and convert all class names to lowercase in the
registry:

```python
        cls.REGISTRY[new_cls.__name__.lower()] = new_cls
```


## The Base Registered Class

Now we can define a base class that will extend the `RegistryBase` class. However, because `RegistryBase`
is a `type` class, we shouldn't extend it directly - we should use it as a _metaclass_.

```python
class BaseRegisteredClass(metaclass=RegistryBase):
    pass
```

Any class that inherits from this `BaseRegisteredClass` will now be included in the registry when it is
defined.


## Extending the Base Registered Class

The next step is to use the base registered class to start creating interesting classes:

```python
class ExtendedRegisteredClass(BaseRegisteredClass):
    def __init__(self, *args, **kwargs):
        pass
```

We skip defining constructor behavior, as the call order is what's important.


## Seeing it in action

Now we can see the process of adding subclasses to the registry in action.

Start by checking the registry before we have created any subclasses:

```text
>>> print(RegistryHolder.REGISTRY)
['BaseRegisteredClass']
```

Next, define the extended registered class:

```text
>>> class ExtendedRegisteredClass(BaseRegisteredClass):
...     def __init__(self, *args, **kwargs):
...         pass
```

Remember, we add the new class to the registry in the `__new__` method, not the
`__init__` method, so we don't even need to instantiate an `ExtendedRegisteredClass`
object for it to be added to the registry. Check the registry again:

```text
>>> print(RegistryHolder.REGISTRY)
['BaseRegisteredClass', 'ExtendedRegisteredClass']
```


# Examples

Let's consider a specific example to help illustrate the usefulness of the Registry pattern:
adding the ability to index different kinds of documents to a search engine.

## Example: Search Engine

Suppose we are writing a search engine, and we are working on the search engine
backend. Specifically, consider the backend portion that iterates over a group of
documents, checks if the document is already in the search index, and either adds
a new item to the search index, updates an existing item in the search index, or
deletes an item from the search index.

### Registry Subclasses

A search engine may index multiple kinds of documents, each living in different locations.
For example, a search index may index .docx files in a Google Drive folder,
Github issues, and/or a local folder full of Markdown files. For each of these
document types, we must define:

- How to add or update all documents in the document storage system (Google Drive, Github
  API, local filesystem, etc.); this method should be able to get a list of documents of this
  document type that are already in the search index, either by running a query itself, or by
  accepting a list of documents already in the index as an input argument

- What schema to use (mapping various field names to data types) for documents of this type

- How to display search results when they are documents of this type (i.e., how to display
  what fields when showing the user search results)

This can be done by defining classes corresponding to different document types, where
each class defines how to do the above actions, and wraps them in high-level API methods
that the manager classes can call.

The manager classes want a way to get a list of available document types, and to call
each document type's high-level API methods. This can be done with the registry.

### Doctype Registry Base Type

Start by defining a base type that will register new subclasses in a doctype registry. Note that
as per the [`__new__` documentation](https://docs.python.org/3/reference/datamodel.html#object.__new__),
the `__new__` method takes the class (in our case, a class of type `type`) as the first argument `cls`,
and it should return a new object instance (which, again, is an instance of type `type`).

```python
class DoctypeRegistryBase(type):

    DOCTYPE_REGISTRY = {}

    def __new__(cls, name, bases, attrs):
        new_cls = type.__new__(cls, name, bases, attrs)
        cls.DOCTYPE_REGISTRY[new_cls.__name__.lower()] = new_cls
        return new_cls

    @classmethod
    def get_doctype_registry(cls):
        return dict(cls.DOCTYPE_REGISTRY)
```

### Base Registered Doctype Class

Next, we define a base class for any document type that we want registered in the doctype
registry, using `DoctypeRegistryBase` as our metaclass (because it is a class of type `type`,
as opposed to a normal class).  All document types are required to define three bits of behavior
(interacting with the document storage system to iterate over all documents; extracting information
from individual documents; and displaying a given document type when it is a search result. We
define these virtual methods on the base registered doctype class.

```python
class BaseRegisteredDoctypeClass(metaclass=DoctypeRegistryBase):

    def add_update_delete(self, *args, **kwargs):
        """
        Iterate over all documents in the document storage system
        and add/update/delete documents as needed.
        """
        raise NotImplementedError()

    def get_schema(self, *args, **kwargs):
        """
        Assemble and return the schema (map of field names to data types)
        """
        raise NotImplementedError()

    def render_search_result(self, *args, **kwargs):
        """
        Use a Jinja template to render a single search result of type doctype
        to display to the user via the web interface
        """
        raise NotImplementedError()
```

### Derived Registered Doctype Class

Now that we have a base class, we can define child classes that have the specific
API functionality needed.

Here is a high-level sketch of what the Github issue document type class might look like,
starting with the add/update/delete method, which boils down to some set operations to determine
what documents to add, update, or delete from the search index.

(Also note, these methods are defined as static methods because they are called once for each
doctype class, but this does not necessarily need to be the case.)

```python
class GithubIssueDoctype(BaseRegisteredDoctypeClass):

    @staticmethod
    def add_update_delete(self, *args, **kwargs):
        # Get set of indexed document IDs
        indexed_docs = set()
        results = run_search_index_query(doctype = self.__name__.lower())
        for result in results:
            indexed_docs.add(result.id)

        # Get set of remote document IDs
        remote_docs = set()
        for org_name in get_org_names():
            for repo_name in get_repo_names(org_name):
                for file in get_repo_files(repo_name, org_name):
                    remote_docs.add(file.id)

        # Do some set math to figure out what to add/update/delete
        add_ids = remote_docs.difference(indexed_docs)
        update_ids = indexed_docs.union(remote_docs)
        delete_ids = indexed_docs.difference(remote_docs)

        # Do the operations
        for add_id in add_ids:
            add_document_to_index(add_id)
        for update_id in update_ids:
            update_document_in_index(update_id)
        for delete_id in delete_ids:
            delete_document_in_index(delete_id)

    @staticmethod
    def get_schema(self, *args, **kwargs):
        ...

    @staticmethod
    def render_search_result(self, *args, **kwargs):
        ...
```

Now we do the same for documents on Google Drive, defining a different `add_update_delete()` method
specific to Google Drive documents (note that while the sketch of this method looks similar to the
Github doctype above, the implementation will look more and more different as we include more and more
detail in our method and API calls).

As before, we make these methods static.

```python
class GoogleDocsDoctype(BaseRegisteredDoctypeClass):

    @staticmethod
    def add_update_delete(self, *args, **kwargs):
        # Get set of indexed document IDs
        indexed_dcos = set()
        results = run_search_index_query(doctype = self.__name__.lower())
        for result in results:
            indexed_docs.add(result.id)

        # Get set of remote document IDs
        remote_docs = set()
        for files in get_gdrive_file_list():
            remote_docs.add(file.id)

        # Do some math to figure out what to add/update/delete
        add_ids = remote_docs.difference(indexed_docs)
        update_ids = indexed_docs.union(remote_docs)
        delete_ids = indexed_docs.difference(remote_docs)

        # Do the operations
        for add_id in add_ids:
            add_document_to_index(add_id)
        for update_id in update_ids:
            update_document_in_index(update_id)
        for delete_id in delete_ids:
            delete_document_in_index(delete_id)

    @staticmethod
    def get_schema(self, *args, **kwargs):
        ...

    @staticmethod
    def render_search_result(self, *args, **kwargs):
        ...
```

### Using the Registry

The last step is to actually use the registry from the class that manages all of our subclasses.
In this case, we have a `Search` class that defines high-level operations (such as, "add/update/delete
all documents indexed by this search engine") and in turn calls the corresponding method for each doctype
that has been registered.

```python
class Search(object):

    def add_update_delete_all(self, *args, **kwargs):

        # Iterate over every doc type
        for doctype_name in DoctypeRegistryBase.DOCTYPE_REGISTRY:

            # Get a handle to the doctype class
            doctype_class = DoctypeRegistryBase.DOCTYPE_REGISTRY[doctype_name]

            # Call the static method add_update_delete on the doctype class
            doctype_class.add_update_delete(*args, **kwargs)

            # Note: if these methods were not static, we would need to create an instance first
            # doctype_instance = doctype_class()
            # doctype_instance.add_update_delete(*args, **kwargs)
```

# Further Modifications

In the example above, we don't have any need to create specific instances of the document type classes,
since they do not need to preserve their state between calls, and we only need one instance of the doctype
class per search engine.

We could re-implement this pattern, modifying the search engine doctype classes to be normal, non-static
classes. This would allow us to have, say, two instances of the Github issues doctype class (corresponding
to two different sets of Github API credentials, or two different Github accounts), or two instances of the
Google Drive doctype class (corresponding to two different Google Drive folders). In this case, we would
want to restructure the Search class to instantiate and save doctype class instances in the constructor,
and use them later.

Here's an example `Search` class that would instantiate one of each subclass in the constructor, to be used
in later methods:

```python
class Search(object):

    def __init__(self, *args, **kwargs):

        # Store instances of each doctype
        self.all_doctypes = []

        # Iterate over every doc type
        for doctype_name in DoctypeRegistryBase.DOCTYPE_REGISTRY:

        # Get a handle to the doctype class
        doctype_class = DoctypeRegistryBase.DOCTYPE_REGISTRY[doctype_name]

        # Create an instance of type doctype_class
        doctype_instance = doctype_class()

        # Save for later
        all_doctypes.append(doctype_instance)

    def add_update_delete(self, *args, **kwargs):

        # Call the add_update_delete method on each doctype instance
        for doctype_name, doctype_instance in self.all_doctypes.items():
            doctype_instance.add_update_delete(*args, **kwargs)
```

(Note that this would work best if we removed the `@staticmethod` decorators from the doctype classes
defined above.)

# Summary

In this post, we covered a useful programming pattern, the Registry, and showed it in action for one
example - allowing a search engine index to register various document type subclasses, then use those
registered subclasses to propagate calls to all document types later.

