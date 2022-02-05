Title: MediaWiki Patterns for a Zettelkasten: Organizing Pages
Date: 2022-02-04 16:00
Category: Zettelkasten
Tags: zettelkasten, mediawiki, note taking, memory

[TOC]

This post is part 4 of a series.

## What is a Zettelkasten?

See [Part 1](https://charlesreid1.github.io/using-mediawiki-as-a-zettelkasten-or-external-brain.html) of this series for a little more background on what we're
talking about! But basically:

* A zettelkasten is a system of note-taking, where notes are kept simple
  and tags, or categories, are added to notes to interlink them and create
  a network of connected notes that aid in discovery and memory.

* MediaWiki (the software that runs Wikipedia) is a mature PHP software package
  for creating a wiki, that has many built-in features that make it very amenable
  for use as a zettelkasten.

## Organizing a Page

The way that pages are organized on a wiki is central to the way the entire wiki is structured. While it may seem
like a trivial topic that anyone can figure out as they go, a zettelkasten is intended to hold notes accumulated
over many years, and as pages accumulate more information they can start to become inconsistent, crowded, and
messy.

We are here with some battle-tested patterns to help manage that mess and keep pages organized and useful
(for all of the many purposes a note in a zettelkasten may need to serve) for years to come.

The three patterns we use to help organize pages on the MediaWiki zettelkasten are:

1. Reserve top-level headers for meta-level page organization (different sections for different uses of the page).
1. Take notes chronologically in a top-level Notes section.
1. Move information to sub-pages as it accumulates or if requires more room.

## What Problem Are We Trying To Solve?

To understand what problem these patterns are trying to solve, suppose you have your MediaWiki zettelkasten, and
you start a single note that is on a broad topic. The note might start with a simple structure, have its own
internal logic, and be organized consistently. Easy as that!

But now suppose you come back to that same topic three months later, with a different perspective and a different
purpose. Maybe you're starting a new project, and re-using some information from the existing note but also adding new
information. Or maybe you learned some new information that changes the way the page should be organized.

With a page in place, with its own structure and organization and logic, it can be difficult to know where to
incorporate new information down the road. The ideal note-taking system eliminates that kind of internal friction,
and makes it as easy as possible to capture new information, without the cognitive burden of having to reorganize
the page again and again.

## Pattern 1: Reserve Top Level Sections

This strategy is a small and easy-to-implement change in how new pages are created, that keeps the page flexible
for multiple different uses. 

The strategy is this: when creating a page, the initial version of the page should only use second-level or deeper
section headers, so any section like `=Specifications=` would become `==Specifications==`.

Yup, that's it! We also have a simple example of a MediaWiki page before/after applying this pattern here:
<https://charlesreid1.com/wiki/Zettelkasten/Patterns/Page_Organization#Pattern_1:_Reserve_Top_Level_Sections>

## Pattern 2: Taking Notes Chronologically

We reserve top-level headers for dividing the page based on its different uses. If we want to start taking notes,
we can add a top-level Notes section to the bottom and start taking notes there. 

To keep notes organized chronologically, we add a second-level header with the year, month, and date. That way,
while we're taking notes, we don't have to worry about how to incorporate the information into the existing
"Overview" information, or try and filter the information as we go. We add notes to the notes section, and can copy
or move information to other parts of the page later. 

Here is a simple example of a MediaWiki page after applying this pattern:
<https://charlesreid1.com/wiki/Zettelkasten/Patterns/Page_Organization#Pattern_2:_Taking_Notes_Chronologically>

## Pattern 3: Subpages

While following the pattern covered above, you might find that on a particular day, working on a particular task,
the notes for that task end up being much more complicated than initially expected - it might involve research,
links, tasks, notes, and in general require more room than the sub-sub-subsection allotted to it by using the
two patterns we have covered.

In that situation, you can replace the sub-sub-section's text with a link to a subpage (for example, on the
`[[Foobar]]` page, if you are working on Baz and it gets complicated, you create a subpage `[[Foobar/Baz]]`).
The original page should link to the subpage, and vice-versa, to make it easy to navigate. Any relevant
Category tags should also be added to the subpage, to help make it findable.

This page shows another simple MediaWiki example page showing the subpage pattern in action:
<https://charlesreid1.com/wiki/Zettelkasten/Patterns/Page_Organization#Pattern_3:_Subpages>

## More Details

For more details, see the full writeup on our (public non-zettelkasten!) wiki here:
<https://charlesreid1.com/wiki/Zettelkasten/Patterns/Page_Organization>

