Title: Using MediaWiki as a Zettelkasten or External Brain
Date: 2022-01-28 13:00
Category: Zettelkasten
Tags: zettelkasten, mediawiki, vpn, note taking, memory

[TOC]

This post is part 1 of a series.

## What is a Zettelkasten?

Before we talk about using MediaWiki as a zettelkasten, let's start with the basics:
_what is a zettelkasten?_

[(Wikipedia article)](https://en.wikipedia.org/wiki/Zettelkasten)

German for "slip box", a zettelkasten is a system for organizing notes and thoughts
that facilitates cross-references and serendipitous connections. The key to a good
zettelkasten is filling it with many notes that are well-tagged. Once the zettelkasten
is filled with notes, it can facilitate connections between new notes and existing notes.
In this way, a zettelkasten is not only a way to help store and remember information,
it is a way to enhance creativity by facilitating connections between material.

By nature, each zettelkasten will be unique to its owner, as the goal of the zettelkasten
is to help facilitate memory and connections between ideas, and everyone's mind works
differently. Each zettelkasten uses different media - index cards, filing cabinets, software - 
and different techniques.

## MediaWiki As Zettelkasten

In the series of blog posts that will follow this one, we will be giving you an inside glimpse
of our particular zettelkasten, which is built around [MediaWiki](https://mediawiki.org), the same
wiki software that runs Wikipedia. We will cover what our
daily zettelkasten "routine" looks like, some general techniques for anyone using a zettelkasten,
and some particular features of MediaWiki that we use in our zettelkasten.

But first, a bit of history to cover how we got here.

## In The Beginning: Some History

We first stumbled on the idea of a zettelkasten around May of 2020, and it immediately resonated.
But our search for the perfect notetaking system had far predated this discovery. We have sampled
our share of notetaking systems over the years, and each has had its pain points. Finding the
perfect notetaking system requires discovering the pitfalls of many not-so-perfect notetaking systems.

### The Dark Ages:

**Spiral notebooks**:

Back in the analog days, we kept several sets of spiral notebooks for different
subjects. We always valued the ability of this note-taking system to allow a context-switch by just
closing one notebook and opening another. And nothing beats the tactile sensation of paging through
a spiral notebook that is filled with writing.

**Palm pilot**:

As a teenager, we got our hands on a used Palm Pilot, and it quickly became
a combination note-taking device and library. My notes were stuffed with abridged summaries of historical
facts, philosphy books, chemistry facts, and mathematical formulas. 
(It would take about a decade before internet on cellphones was commonplace, and you could easily
resolve an argument during a car trip about some historical trivia by looking something up on Wikipedia.
Come to mention it, Wikipedia was still in its infancy.)

**Binders**:

Our spiral notebook system got upgraded into a binder system when we were taking college
courses and had to keep notes, homework, exams, and papers together. It mostly worked well, but you could
only carry two or three binders at a time. With a textbook or two, the backpack became a rucksack.
The portability/availability tradeoff was a constant and common tradeoff in the pre-cloud, pre-mobile internet 
days. As a younger person, you don't have your own office, so portability is particularly important.

**Hipster PDA**:

Yes, we admit to adopting the [Hipster PDA](https://en.wikipedia.org/wiki/Hipster_PDA) at
one point. (What is a hipster PDA, you ask? Imagine a small stack of half-cut index cards, held together by a binder
clip or rubber band or box, small enough to slip into a pocket. That was essentially our hipster PDA.)

We had a stack of white cards, plus different colored cards inserted to mark different sections.
The top section of cards were the calendar, with one card for each of the next 30 days or so; 
the back of those cards had brief notes or tasks for that day, or any important events.
There was a section for todo cards, which had a topic for the tasks on the front, and a list of tasks on the back.
There was a section for cards with information to study, perfect while waiting to catch a bus.

No surprises, this method was just too inefficient to last long. The lack of space on the cards, and the
constant desire to rearrange the information on the cards, made it hard to strike the right balance.

Here is the most value lesson we learned from that entire experience, distilled down to its essence:

There are some things that are best done with paper, not digital tools. 

**CALENDARS ARE NOT ONE OF THOSE THINGS.**

### The Renaissance: 

**Evernote**:

Around the turn of 2010, we made heavy use of Evernote as a central place for
storing information and notes. We can say, with the benefit of hindsight, that we were trying to implement
something like a zettelkasten with Evernote.

* The way we used Evernote was by trying to implement the idea that Evernote could serve two purposes:

* First, it could be used to capture external information - ideas, links, books, a quote, a key reference.
  (The Evernote Web Clipper, a browser extension that would save a website to Evernote, was invaluable.)
  If you could get the text into Evernote, then it could be searched, and the search function
  cold become a path to discovering connections between notes and topics.
* Second, if you created notes for each day, or for specific events or meetings on specific days,
  you could use it as a journal, and start to create a cross-referenced record of what you did
  on different days with different ideas. This could help with strengthening memory and recall.

Evernote soured on me when Evernote the company began to hop on the commercialization train, leaving many
long-standing and basic user interface bugs unfixed while they spent all their time and effort developing
and marketing products like digital pens and special paper that would convert handwritten notes into Evernote
notes. It was absurd.

Ultimately, the Achilles Heel was the fact that their application was a walled garden of content, in a format
that was complicated to export and in a custom XML format that had to be picked apart to get your stuff out.

Combined with the UI bugs in the Evernote application, the prospect of sinking time and effort into organizing
my "external brain" in the form of notes in their walled garden application made no sense.

We also discovered a problem with our method of capturing external information. If information is
simply dumped wholesale into a search engine, as the Web Clipper did, it created an enormous amount of
noise in search results. Nothing useful gets unearthed, no new connections are made.
Too much content leads to no meaning.

Ideas need to be carefully extracted from their environment and placed in a fresh, empty note, with plenty of space to grow.

**Github**:

We have approximately one billion GitHub repositories and/or Gists accumulated from
our various side projects and distractions. Of these, several are just plain old readmes, because you can
make a Readme look like a million bucks by adding some lorem ipsum and some fake badges from badge.io,
and Markdown is a very convenient way to write up technical content (except math, but even that problem has solutions)
(get it).

**AMP (Apache + MySQL + PHP) and DynDNS**:

In the early 2010s we discovered the wonder of hosting our own website
on our own machine, thanks to the now-defunct DynDNS service. By running this wonderful desktop widget 
you could turn a local server into a public website, and we began the time-honored tradtion of nerds everywhere
of using technology to document our adventures with technology, and to document the technology we were using to
run the technology used to document our adventures with technology. All gone now, but some of the pages live on
somewhere on <https://charlesreid1.com/wiki>.

### The Enlightenment:

**Joplin**: 

A sensible alternative to Evernote that we wish we had discovered sooner.
A nice, easy-to-use, open-source application that implements the Evernote concept, but using Markdown,
simple flat text files, optional backup via cloud synchronization service, encryption, and many other features,
all wrapped in a handsome and simple UI. (Why... Why didn't we discover it sooner??)

**MediaWiki**: 

While we were learning about PHP, we discovered that MediaWiki, the software
that runs Wikipedia, is built on PHP, and we spun up our own wiki. We have maintained that same
wiki for over a decade at <https://charlesreid1.com/wiki/>

### The Modern Era:

**Private MediaWiki Zettelkasten**:

We have reached a point where we know both what we want and what technology
can provide it. MediaWiki is that technology. In the blog posts that follow, we will detail the reasons we think
MediaWiki is the best choice for Zettelkasten software, and how we've used MediaWiki features to supercharge
our notetaking, thinking, and information retention.

## Zettelkasten Is Not A Public Wiki

We use our zettelkasten MediaWiki (hereafter referred to as the "private wiki") the same way a person would use a 
private journal or appointment book: it is not intended for public consumption. So to be clear, we do not use our 
public wiki <https://charlesreid1.com/wiki> as the zettelkasten - we have a totally separate private wiki
serving that role.

(That being said, a lot of the patterns we developed for using our public wiki for note-taking, studying, and side
proejcts ended up being very helpful for the private wiki.)

## Private Wiki Details

**Where is the private wiki run?**

* We run it on a desktop server sitting in the living room, so that we have physical access to the machine
  (for troubleshooting, backups, security, and fast local network)

**What software is it running?**

* The desktop server runs Linux, the MediaWiki software, plus an Apache server with PHP enabled

* MediaWiki can be a bit complicated to get up and running and properly configured, and is the biggest hurdle to
  setting up a private wiki. But the payoff is tremendous.

* We have made our personal situation more complicated by using Docker to run MediaWiki, MySQL, Apache, PHP, and
  an Nginx reverse proxy via networked containers. ***We do not recommend our Docker pod approach to anyone, ever.***

* The private wiki pod looks similar to the pod that runs the public wiki, pod-charlesreid1
  (<https://github.com/charlesreid1-docker/pod-charlesreid1>)

**What network is it on? How do you keep it private, but also accessible remotely?**

* The private wiki server is connected to a [Tinc](https://www.tinc-vpn.org/) virtual private network in the cloud.
  Tinc can form mesh VPN networks, meaning if two VPN clients (the wiki server and a laptop accessing the wiki)
  live on the same local network with very short hop, but the VPN server is hundreds of miles away, the traffic can
  traverse the shortest route (local network only), rather than having to pass through the server, with a higher 
  latency.

* When away from home, any machine that is a VPN client (for example, a work laptop and a personal laptop)
  can access the private wiki. Tinc uses certificates for identity verification, and becoming a client
  requires copying a client certificate to the VPN server.

**How do you make URLs pretty, so the private wiki is available at wiki.example.com?**

* Making the private wiki available at pretty URLs (using a domain you own) works as follows:

* Create a public DNS entry for wiki.example.com that points to an IP at a local network IP address, like
  `10.1.2.3`. This should be the VPN IP address of the private wiki server.

* When random people visit wiki.example.com, it will redirect them to that local network IP address, 
  which will never resolve to the private wiki because they will never be connected to the VPN network.

* When VPN clients visit wiki.example.com, it will redirect them to that local network IP address,
  which will route the traffic to the private wiki server via the VPN network connection. It will
  load just like a normal site.

**How do you handle HTTPS and SSL Certificates?**

* For the above to actually work and for the page to load, the browser will want a certificate for wiki.example.com

* We are using LetsEncrypt, so periodically we have to switch the DNS entry from the private IP address to a public
  IP address, perform the certificate renewal process on that machine, and then switch the DNS entry back.

* If the private wiki server is behind a NAT and not publicly accessible, then the machine that renews the
  certificate will be separate from the machine that runs the private wiki. In this case, certificates
  must be copied from one machine to another. That turns out to be complicated, because LetsEncrypt cert files
  are owned by root, and LetsEncrypt is extremely picky about its entire directory structure - anything in the
  wrong place will cause mysterious certbot failures.

* If the DNS provider doesn't allow programmatic DNS changes, then the above certificate renewal process
  can only be done manually.

* If the DNS provider does allow programmatic DNS changes, make sure it's locked down, for example by restricting
  the source IP of API calls that make DNS changes.

**Is that all?**

* Probably not, but we did our best. Good luck.

The end result is a private MediaWiki that's all yours! Available at your own domain! Accessible only to you!

It's an exciting feeling, opening a brand-new wiki for the first time.

## What Will Be Covered In This Series?

A brief preview of what we will cover in this series of blog posts:

* How to use daily/monthly pages to organize notes and work
* How to use MediaWiki Categories and Templates to connect notes together
* How to keep track of random bits of information like links
* How to keep track of todo lists and projects
* How to organize information on a page, and general organization patterns
* How to make the wiki easy to navigate
* Flag templates
* Rolling text templates

Check back soon for links.
