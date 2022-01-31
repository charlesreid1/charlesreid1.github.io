Title: MediaWiki Patterns for a Zettelkasten: Monthly Template Pattern
Date: 2022-01-31 9:00
Category: Zettelkasten
Tags: zettelkasten, mediawiki, note taking, memory

[TOC]

This post is part 3 of a series.

## What is a Zettelkasten?

See [Part 1](https://charlesreid1.github.io/using-mediawiki-as-a-zettelkasten-or-external-brain.html) of this series for a little more background on what we're
talking about! But basically:

* A zettelkasten is a system of note-taking, where notes are kept simple
  and tags, or categories, are added to notes to interlink them and create
  a network of connected notes that aid in discovery and memory.

* MediaWiki (the software that runs Wikipedia) is a mature PHP software package
  for creating a wiki, that has many built-in features that make it very amenable
  for use as a zettelkasten.

## The Monthly Template Pattern

We cover the monthly template pattern in full detail here: <https://charlesreid1.com/wiki/Zettelkasten/Patterns/Monthly_Template_Pattern>

This blog post is a summary of what's on that page.

## What is the Monthly Template?

The monthly template is a MediaWiki template (a bit of text that can be dynamically inserted into other pages)
that inserts links to all daily pages for a given month.
The monthly template is called something like `[[Template:January2016]]`. All daily pages in January 2016 would dynamically include
this monthly template by having the text `{{January2016}}` at the end of the note. 

We have mentioned before ([Part 2](https://charlesreid1.github.io/mediawiki-patterns-for-a-zettelkasten-daily-page-pattern.html))
that interlinks between different pages are crucial to making the wiki easy to navigate; the monthly template
is a way to make navigation easier by inserting links for all daily pages in a given month.

## What's in the Monthly Template?

Each monthly template consists of a box with the following links:

* List of links to all other daily pages in the given month
* Links to the previous month's template and the next month's template
* Links (direct links) to view or edit the monthly template

The last bullet point seems minor, but we have found it enormously useful to include with all templates.

## Example Monthly Template

We've set up an example monthly template on our public wiki (which is not a zettelkasten!) for a hypothetical
January 2016: <https://charlesreid1.com/wiki/Template:January2016>

We hope the example shows the monthly template in action and helps clarify some of the details in this post.

## More Details

For more details, see the full writeup on our (public non-zettelkasten!) wiki here:
<https://charlesreid1.com/wiki/Zettelkasten/Patterns/Monthly_Template_Pattern>

