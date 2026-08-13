Title: Blind SQL Injection with Conditional Responses
Date: 2023-05-22 14:00
Category: Security
Tags: security, sql injection, sqli, blind sqli, portswigger, burp suite
Status: draft

Part 4 of our
[PortSwigger Web Security Academy series](working-through-the-portswigger-web-security-academy.html).
This one covers blind SQL injection with conditional responses, which is
the easier of the two blind SQLi flavors we work through in this series.

Wiki notes:
[SQL Injection/Blind](https://charlesreid1.com/wiki/SQL_Injection/Blind).

## The Setup

Some SQL injection vulnerabilities never give you a direct channel back
for the query results. The application runs a SQL query with your input,
but the response doesn't render the result or leak database errors. The
canonical example is a cookie tracking ID: the ID gets used in a SQL
query on every request, but the query output is not rendered anywhere on
the page.

You can still exploit it. The technique is called *blind* SQL injection,
because you can't see the query result directly, but you can *infer* it
from other things the page does.

## The Boolean Oracle

The version we cover in this post relies on the page rendering
*differently* depending on whether the injected query returns a row.
Classic PortSwigger example: a page that shows "Welcome back" if the
tracking ID matches a valid user in the database, and doesn't otherwise.

Send this request:

```
TrackingId=xyz' AND '1'='1
```

The `AND '1'='1'` is unconditionally true, so if the outer query would
have matched anything, it still matches. Welcome-back banner shows up.

Now send this one:

```
TrackingId=xyz' AND '1'='2
```

The `AND '1'='2'` is unconditionally false, so no rows match. No
welcome-back banner.

Two requests. Two different pages. That's your boolean oracle. Any yes/no
question you can encode as a SQL condition, you can ask the database and
get an answer via page behavior.

## Extracting a Password One Character at a Time

Once you have the oracle, the game is to encode useful yes/no questions.
The useful one is "is the first character of the administrator's password
greater than X?"

```
TrackingId=xyz' AND SUBSTRING((SELECT Password FROM Users WHERE Username = 'Administrator'), 1, 1) > 'm
```

If the welcome-back banner appears, the first character is greater than
`m`. If not, it's less than or equal to `m`.

Binary-search the alphabet:

* Is char 1 > `m`? Yes → search `n` through `z`
* Is char 1 > `s`? Yes → search `t` through `z`
* Is char 1 > `v`? No → search `t` through `v`
* Is char 1 > `u`? No → search `t` through `u`
* Is char 1 > `t`? No → char 1 is `t`

Repeat for character 2. Then character 3. And so on until the password is
in your notebook.

## Automating It In Burp Suite

Doing this by hand for a 20-character password is not something a normal
person will finish. Burp Intruder does the automation.

The recipe:

1. Right-click the request in Burp, "Send to Intruder"
2. In Intruder → Positions, mark the `m` (the letter being tested) as
   the payload position
3. In Intruder → Payloads, set payload type to "Brute forcer" and give
   it the alphabet you care about (`abcdefghijklmnopqrstuvwxyz` plus
   digits and any symbols the password might contain)
4. Run the attack. Sort results by response length or by whether the
   welcome-back string appears in the body. The one match is your
   answer.

For 20 characters, you would normally repeat this 20 times. Or, better,
use Intruder's "Cluster bomb" attack type with two payload positions
(one for character index, one for the letter), which runs all
combinations in one go. Cluster bomb is worth learning - it comes up a
lot in this kind of extraction work.

## When It Doesn't Work

Conditional-response blind SQLi is not always available. Sometimes the
page renders identically no matter what the query returns. When that
happens, you fall back to either

* **Conditional errors** - deliberately cause a SQL error when your
  boolean condition is true, and use HTTP 500 vs 200 as the oracle. This
  is [the next post](blind-sql-injection-with-conditional-errors.html)
  in the series.
* **Time-based** - deliberately make the query sleep for a few seconds
  when your boolean is true, and use response time as the oracle. Useful
  when even errors are suppressed.

The theme is: as long as *anything* the server does depends on the truth
of your boolean, you have an oracle. The rest is engineering.

## References

* Our wiki: [SQL Injection/Blind](https://charlesreid1.com/wiki/SQL_Injection/Blind)
* [PortSwigger blind SQL injection](https://portswigger.net/web-security/sql-injection/blind)
* [Lab 11 - Blind SQLi with conditional responses](https://portswigger.net/web-security/sql-injection/blind/lab-conditional-responses)
