Title: Two Burp Suite Extensions Worth Installing: JWT Editor and Hackvertor
Date: 2023-06-04 20:30
Category: Security
Tags: security, burp suite, extensions, jwt, encoding, portswigger
Status: draft

Short post, high signal-to-noise. If you're using
[Burp Suite](https://charlesreid1.com/wiki/Burp_Suite) for web security
testing, there are two extensions we install on every fresh Burp
installation before doing anything else. Both are free, both are in the
official BApp Store, both take about thirty seconds to install, and both
will save you hours the first time you need them.

Wiki reference:
[Burp Suite/Extensions](https://charlesreid1.com/wiki/Burp_Suite/Extensions).

## How To Install BApp Store Extensions

For anyone who hasn't installed a Burp extension before:

1. In Burp, go to Extensions → BApp Store
2. Search for the extension name
3. Click "Install"
4. Wait for it to appear in the Installed tab

You can also install manually from a JAR file: Extensions → BApp Store →
Manual install at the bottom, pick the file, click Open.

## Extension 1: JWT Editor

[JWT Editor on the BApp Store](https://portswigger.net/bappstore/26aaa5ded2f74beea19e2ed8345a93dd)

JWT Editor lets you view and edit the contents of JSON Web Tokens
in-flight. If a request contains a JWT in an `Authorization: Bearer ...`
header or a cookie, JWT Editor gives you a tab that shows the decoded
header and payload, lets you edit either one, and re-encodes and re-signs
the token on the way out.

Why it matters: JWTs are opaque strings of base64 to the naked eye. If
you want to test what happens when the `role` claim in the payload
changes from `user` to `admin`, or what the server does when you swap
the signing algorithm from `RS256` to `none`, JWT Editor is the tool.

Without it: you're manually base64-decoding, editing JSON in a text
editor, base64-encoding, and pasting the result back into the request.
Every time. For every request.

With it: you edit the JSON in a form, and Burp handles the rest.

## Extension 2: Hackvertor

[Hackvertor on the BApp Store](https://portswigger.net/bappstore/65033cbd2c344fbabe57ac060b5dd100)

Hackvertor is a tag-based conversion tool. You write tags in your request
payloads that get expanded before the request goes out - things like
URL-encode this, base64-encode that, MD5-hash the other thing, ROT13
the result, and so on. Tags can be nested and chained.

The killer feature is bypassing weak Web Application Firewalls. Many WAFs
look for specific attack patterns - the literal string `UNION SELECT`,
for example, or the literal string `<script>`. Hackvertor lets you write
your payload once, then wrap it in a chain of encoding tags that produces
a request the WAF doesn't recognize but the target application still
parses correctly.

If you're doing any serious SQL injection or XSS testing against
real-world targets, Hackvertor turns "the WAF blocked me" into "the WAF
blocked one shape of my payload."

## Other Extensions Worth Knowing About

We won't cover them here, but a few more from the BApp Store that come
up regularly:

* **Autorize** - automated access control testing
* **Turbo Intruder** - much faster than the built-in Intruder for
  high-request-count attacks
* **Logger++** - richer request logging than the built-in HTTP history

Our full list, with notes on when each one matters, is on the
[Burp Suite/Extensions](https://charlesreid1.com/wiki/Burp_Suite/Extensions)
wiki page.

## References

* Our wiki: [Burp Suite/Extensions](https://charlesreid1.com/wiki/Burp_Suite/Extensions)
* [Burp Suite BApp Store](https://portswigger.net/bappstore)
