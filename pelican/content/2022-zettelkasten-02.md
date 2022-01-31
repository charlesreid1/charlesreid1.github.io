Title: MediaWiki Patterns for a Zettelkasten: Daily Page Pattern
Date: 2022-01-30 18:00
Category: Zettelkasten
Tags: zettelkasten, mediawiki, note taking, memory

[TOC]

This post is part 2 of a series.

## What is a Zettelkasten?

See [Part 1](https://charlesreid1.github.io/using-mediawiki-as-a-zettelkasten-or-external-brain.html) of this series for a little more background on what we're
talking about! But basically:

* A zettelkasten is a system of note-taking, where notes are kept simple
  and tags, or categories, are added to notes to interlink them and create
  a network of connected notes that aid in discovery and memory.

* MediaWiki (the software that runs Wikipedia) is a mature PHP software package
  for creating a wiki, that has many built-in features that make it very amenable
  for use as a zettelkasten.

## The Daily Page Pattern

We cover the daily page pattern in full detail here: <https://charlesreid1.com/wiki/Zettelkasten/Patterns/Daily_Page_Pattern>

This blog post is a summary of what's on that page.

## What is the Daily Page?

The Daily Page pattern consists of creating a new page named `[[YYYYMMDD]]` each day,
and using that page to organize and assemble notes for that day.

By creating a new note/article to collect everything from a given day, it means there is a clean slate each day. 

Interlinks from each day's page to other pages are crucial: many inter-wiki links create a link structure that
allow easy navigation of the wiki. Each article in the wiki is a node in a network of interlinked pages; an article
with lots of wiki links makes it easy to jump around the network.

## What's on the Daily Page?

Each daily page has a specific structure. (Note that using MediaWiki means the creation of daily pages can be
automated using bots!) A daily page contains the following:

* Summary of prior day, plus link to prior day (making it easy to navigate backwards)
* Work daily page - we have a separate daily page for work notes
* Links section - here, we collect interesting links. This usually starts as a copy-paste dump, but most links
  will eventually be moved to their own notes (a place to collect information about the link, in addition to the
  link itself).
* Monthly template - we make heavy use of MediaWiki templates (chunks of transcluded text) on our zettelkasten.
  The Monthly Template Pattern (to be covered in a later post) consists of a template with a list of links to all
  daily pages for a given month. This makes it easy to navigate from one day of the month to another.
* Categories - we don't tend to add many categories to daily notes, but we add a category for notes in a give
  month, of the form `[[Category:YYYYMM]]`, to collect all daily pages from a given month. (We also add a category
  for the year, `[[Category:YYYY]]`, which can be helpful in finding older notes.)

Of course, not every day is spent in front of a computer, and sometimes days must be retroactively logged,
but those days can be back-filled with notes.

## Example Daily Page

We've set up an example daily page on our public wiki (which is not a zettelkasten!) from a hypothetical January 1,
2016: <https://charlesreid1.com/wiki/20160101>

Seeing the daily page in action might help this post make a little more sense.

## Advantages of the Daily Page Pattern

The daily page pattern has several advantages. Here are a few:

* The daily page pattern scales well; combined with other patterns, it can help categorize and sift through a large
  amount of information from any one day, and create a detailed record of goings-on from a given day that can
  greatly aid the memory.

* As notes on a particular task or topic get more complicated, we move them to subpages, like
  `[[YYYYMMDD/Foobar]]`, to allow more space to develop the idea or take notes on a blank page.
  The subpage links back to the daily page, and the daily page links to the subpage, to keep all
  pages networked and easy to navigate.

* The daily page pattern is flexible in terms of the time scales it can handle. A zettelkasten that's started in
  2022 can still be used to create detailed notes in the past; if we have a note from July 1, 2007, we can make a new
  page `[[20070701]]` and add the information there. (As mentioned above, adding a category like
  `[[Category:2007]]` to that page can make it easier to find again.)


## Disadvantages of Daily Page Pattern

The daily page pattern does have some disadvantages: when information throughput is low, the daily page
pattern can tend to make pages feel barren and empty.
When there is too much information coming in, a blank canvas can help things feel more calm.
But when there is only a trickle of information coming in, the blank canvas an feel like it is swallowing work.

We have given some thought to this problem, and have a few thoughts:

* One useful general principle is persistence - having lists or chunks of text that persist across days, so it
  doesn't feel like work is being swallowed by the wiki. MediaWiki templates are perfect for this, and can be used
  to maintain lists of pages, lists of todo pages, or lists of projects being worked on.

* We have put the persistence principle into practice by keeping a template for our monthly projects.
  In a given month, we have many projects that we're working on, and each one has various topic pages
  and todo pages to keep track of what we're working on with that project. The monthly project template
  allows us to keep track of what projects we're working on over the course of a month, but each month
  we also get the chance to refresh the list by creating a new one, and preserve that project list in whatever
  state it was in at the end of the month.

* It's possible to use a Weekly Page Pattern or a Monthly Page Pattern in place of a Daily Page Pattern,
  but we do have some thoughts on that.

* In our experience, the weekly pages create a complication in naming - there isn't a good way to conveniently
  know, in advance, which weekly page to go to for a given date. If figuring that out isn't a problem,
  then this would be a good option - a week is a good timeframe for a single page of notes.
  Enough time for ideas to persist and stew, but not so long that the page gets stale.

* We feel that a monthly page is too long a time period to organize notes on a single page - after just a few days,
  the page's content can begin to feel stale, the page may lack the room for accommodating a new idea, or it may
  just feel like all the old ideas are distracting from coming up with new ideas. Whatever it is, we don't
  think the monthly page pattern works well.

* All of that being said, try things out to see what suits your needs!

## More Details

For more details, see the full writeup on our (public non-zettelkasten!) wiki here:
<https://charlesreid1.com/wiki/Zettelkasten/Patterns/Daily_Page_Pattern>

