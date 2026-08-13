Title: Working Through the PortSwigger Web Security Academy
Date: 2023-05-20 20:00
Category: Security
Tags: security, web security, portswigger, burp suite, owasp, pentesting

This post is part 1 of a series. We spent a chunk of May and June 2023
working through the [PortSwigger Web Security Academy](https://portswigger.net/web-security)
labs, mostly the SQL injection track, and taking notes on our wiki as we
went. This post is the setup - what the Academy is, why we picked it, and
how it fits together. The posts that follow will cover the specific
techniques.

## What the Academy Is

PortSwigger makes [Burp Suite](https://charlesreid1.com/wiki/Burp_Suite),
which is the standard tool for web application security testing. They also
run a free online academy at
[portswigger.net/web-security](https://portswigger.net/web-security), which
consists of written lessons plus hands-on labs. The labs are hosted for
you - you get a URL, you attack the app running at that URL, and the
Academy tracks whether you succeeded.

The labs are organized roughly by the
[OWASP Top 10](https://charlesreid1.com/wiki/OWASP), which is the standard
catalog of web application vulnerability categories. SQL injection, XSS,
XXE, access control issues, authentication bugs, and so on.

The reason to pick this Academy over the other options is that the labs
are *real vulnerable web apps*, not multiple-choice questions. You are
using actual Burp Suite against actual HTTP requests. When you finish a
lab, you have practiced the thing, not read about the thing.

## Our Setup

The setup is not complicated:

* [Burp Suite Community Edition](https://portswigger.net/burp/communitydownload)
  (free, sufficient for most labs, painful for a few of the automation-heavy
  ones)
* A [PortSwigger account](https://portswigger.net) (also free)
* A browser configured to proxy through Burp on port 8080
* A wiki page to take notes on, so you remember what you learned a week
  later

That last one is the whole point. The Academy is good, but if you finish
a lab and move on without writing anything down, you will forget the
technique inside a month. Writing up each lab in your own words - the
setup, the attack, the trick that made it work - is what turns lab
practice into retained knowledge.

## The OWASP Top 10 as a Scaffold

We use [OWASP Top 10](https://charlesreid1.com/wiki/OWASP) as the
organizing scaffold for our security notes on the wiki. It is not the only
way to slice web security, but it is the way that most people talk about
web security, and it is what you'll see referenced in bug bounty programs
and pentest reports. Learning to recognize each category is a solid
foundation.

The list has changed over the years - the 2021 version reorganized things
significantly - but the SQL injection, XSS, and XXE categories that we
focus on in this series have been fixtures since the beginning.

## What This Series Will Cover

Rough plan for the next few posts:

* SQL injection fundamentals - the four attack shapes that cover most
  cases
* UNION attacks specifically, and how to use them to dump data from
  tables you don't have direct access to
* Blind SQL injection with conditional responses - inferring data from
  page behavior
* Blind SQL injection with conditional errors - the more advanced
  Oracle-flavored variant
* A short post on two Burp Suite extensions that are worth installing
  before you start

Everything is grounded in a specific PortSwigger lab. Everything has a
corresponding page on our
[wiki](https://charlesreid1.com/wiki/Category:Security). If the summary
here is not enough detail, the wiki page is the deep version.

## References

* [Web Security Academy](https://portswigger.net/web-security)
* Our wiki notes: [Burp Suite](https://charlesreid1.com/wiki/Burp_Suite),
  [SQL Injection](https://charlesreid1.com/wiki/SQL_Injection),
  [OWASP](https://charlesreid1.com/wiki/OWASP)
