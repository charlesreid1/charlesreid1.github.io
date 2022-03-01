Title: MediaWiki Patterns for a Zettelkasten: Todo Lists
Date: 2022-02-28 16:00
Category: Zettelkasten
Tags: zettelkasten, mediawiki, note taking, memory

[TOC]

This post is part 5 of a series.

## What is a Zettelkasten?

See [Part 1](https://charlesreid1.github.io/using-mediawiki-as-a-zettelkasten-or-external-brain.html) of this series for a little more background on what we're
talking about! But basically:

* A zettelkasten is a system of note-taking, where notes are kept simple
  and tags, or categories, are added to notes to interlink them and create
  a network of connected notes that aid in discovery and memory.

* MediaWiki (the software that runs Wikipedia) is a mature PHP software package
  for creating a wiki, that has many built-in features that make it very amenable
  for use as a zettelkasten.

## Todo Lists

This post will use information covered in our previous posts, mainly from [Part 3](https://charlesreid1.github.io/mediawiki-patterns-for-a-zettelkasten-organizing-pages.html)
on organizing pages, but applied to pages in the wiki that are dedicated to keeping track of todo lists.

## The Todo Category

Before we get into how we organize todo lists, we should mention that we make heavy use of this pattern in our wiki, 
so we have many todo lists. To keep track of all the todo lists, it can be useful to have a way to get a list of todo lists.

Whenever we create a new todo list page, we always add the category [[Category:Todo]] to the todo list.
If we need to see all our todo lists in one place, we just visit that Category:Todo page, and MediaWiki
will automatically generate a list of all todo lists.

## Start with Top Level Sections

When starting a todo list page, we use a strategy covered in [Part 3](https://charlesreid1.github.io/mediawiki-patterns-for-a-zettelkasten-organizing-pages.html),
which is to reserve top-level sections for the different purposes the page may serve.

Typical top-level sections in our todo list pages are:

* **Overview** - used if we are revisiting the page and need a brief summary of the most important information
* **Plan** - contains planned todo items, work that is not yet in progress
* **Todo** - contains items that are currently in progress, usually notes from today or this week (and empty if a todo page is not being actively used)
* **Done** - items that were previously in Todo, but were completed
* **Notes** - a top-level section that contains notes about the todo list topic. Not necessarily todo items, but useful/related to the todo list.

The Notes section is useful when the todo list is still taking shape; the Overview section is useful when the todo
list is done, and there is a concrete outcome or important summary information to refer back to.
The Plan section is useful as a catch-all basket for future tasks, or tasks that aren't being addressed yet.
And so on.

## Topic Subsubsections

The top-level sections of the page are dedicated to different uses of the page: Overview, Planned Todo Items,
In-Progress Todo Items, Completed Todo Items, Notes, etc.

Within those sections, the second-level headers organize information and notes by date. The second-level headers
have the form `YYYYMMDD`. 

The third-level headers are topic headers. If a single todo item requires completing tasks A, B, and C,
which are completed on the same date, then tasks A, B, and C would have their own third-level headers.

As a more concrete example, if I start working on a task to "Foo the bar" on 2016-01-01, I will go to the
top-level section for In-Progress Todo Items, add a subsection 20160101, and then add a sub-subsection "Foo the
bar":

```plain
=Todo In Progress=

==20160101==

===Foo the bar===

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent maximus, purus a gravida suscipit, urna neque
pharetra sem, in luctus nisl arcu eu risus. Aliquam vulputate ac tortor et ornare.
```

## Todo Subpages

What if halfway through task C, things start to get complicated? Starting notes at a third-level header doesn't
leave room for many more headers - so if you find yourself needing to organize notes for task C into their own
sections and subsections, start a subpage. If your todo list is at `[[Todo/Foobar]]`, then split the notes for task C
into their own subpage, `[[Todo/Foobar/Task C]]`. Create links between the two pages, so it's easier to navigate
to/from them.

## Notes First, Overview Last

In terms of order, we usually organize the top level sections of the page in the order we've specified above:
Overview, Planned Todo Items, In-Progress Todo Items, Done Todo Items, and Notes. These can be modified to suit
your own purposes or the particular todo list.

Usually, we will start with the last section - Notes - and end with the first section - the Overview.

The Notes section is where we start when we're trying to figure out how to organize the todo list page. The notes
section is typically only useful when you're starting up a todo list, which is why it goes at the bottom - it is
rarely used once the todo list is started.

The Overview section is where we summarize important outcomes from various todo tasks. It might be a summary of
major efforts, or a list or table that's the outcome of all of the work on the todo list. In any case, if you need
to add an Overview section, you'll know it.

## An Example

We have an example page showing this pattern in action. It's here: <https://charlesreid1.com/wiki/Todo/Foo>

## More Details

For more details, see the full writeup on our (public non-zettelkasten!) wiki here:
<https://charlesreid1.com/wiki/Zettelkasten/Patterns/Todo_Lists>

