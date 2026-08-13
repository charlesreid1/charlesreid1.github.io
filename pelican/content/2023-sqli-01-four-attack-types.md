Title: SQL Injection Fundamentals: Four Attack Shapes
Date: 2023-05-21 14:00
Category: Security
Tags: security, sql injection, sqli, portswigger, web security, owasp

This is part 2 of our series on working through the
[PortSwigger Web Security Academy](working-through-the-portswigger-web-security-academy.html).
This one covers SQL injection at a bird's-eye view - the four main attack
shapes that show up over and over, with the smallest possible example of
each. Later posts will drill into specific attack types.

Full notes on our wiki:
[SQL Injection](https://charlesreid1.com/wiki/SQL_Injection).

## What SQL Injection Is

SQL injection is a web security bug that lets attackers execute their own
SQL against your database, by taking advantage of user inputs that are
not sanitized before being pasted into a SQL query.

The reason it is worth caring about is impact vs. effort. SQL injection
is one of the highest-impact web vulnerabilities (attacker can potentially
read or modify anything in the database), and one of the lowest-effort
to actually pull off. That combination is why it has been in the
[OWASP Top 10](https://charlesreid1.com/wiki/OWASP) since forever.

## The Four Shapes

Our notes group SQL injection into four attack shapes:

1. Retrieving hidden data
2. Subverting application logic
3. UNION attacks
4. Blind SQL injection

The rest of this post walks through the smallest example of each.

## Shape 1: Retrieving Hidden Data

Suppose a shopping site has this URL for showing product listings:

```
https://insecure-website.com/products?category=Gifts
```

Behind the scenes, that URL runs this SQL query:

```
SELECT * FROM products WHERE category = 'Gifts' AND released = 1
```

The `released = 1` clause hides unreleased products from the public. If
the `category` parameter is not sanitized, we can smuggle in SQL that
comments out the rest of the query:

```
https://insecure-website.com/products?category=Gifts'--
```

The `--` starts a SQL comment. Everything after it is ignored, including
the `AND released = 1` check. Result: all products, including
unreleased ones, get returned.

Same trick with an unconditional truthy clause:

```
https://insecure-website.com/products?category=Gifts'+OR+1=1--
```

## Shape 2: Subverting Application Logic

Same idea, applied to authentication. If a login form runs

```
SELECT * FROM users WHERE username = 'user' AND password = 'nopass'
```

and doesn't sanitize the username field, you can log in as anyone by
supplying the username:

```
administrator'--
```

Everything after the `--` (including the entire password check) becomes
a comment. The query returns the administrator row. You are logged in.

You have to guess the username - `admin`, `administrator`, `root`,
`superuser` - so this is not a one-shot attack, but it is not a hard
attack either. If you see a login page throwing internal server errors
when you put a single quote in the username field, that is your signal.

## Shape 3: UNION Attacks

UNION attacks use SQL's `UNION` operator to piggyback data from other
tables into the results of the original query. If a shopping site runs

```
SELECT name, description FROM products WHERE category = 'Gifts'
```

and the `category` parameter is injectable, we can attach a UNION:

```
' UNION SELECT username, password FROM users--
```

The final query becomes

```
SELECT name, description FROM products WHERE category = ''
UNION SELECT username, password FROM users--'
```

which returns product listings and every username/password pair. Whatever
UI was going to display product name and description now also displays
usernames and passwords.

The oversimplified version above works out cleanly, but in practice you
need to figure out the column count of the outer query first, then make
sure the columns you union in are type-compatible. We covered that in
[the next post](sql-injection-union-attacks.html).

## Shape 4: Blind SQL Injection

Blind SQLi is what you do when the application is vulnerable but the
query results don't come back to you in the HTTP response. Cookie tracking
IDs are the classic example - the ID gets fed to a SQL query on every
request, but the query result is never rendered on the page.

Even without seeing the result directly, you can often *infer* it from
how the page behaves. Ship one of these two requests:

```
xyz' AND '1'='1
xyz' AND '1'='2
```

If the page renders differently in the two cases (say, one shows a
"Welcome back" banner and the other doesn't), congratulations, you have
a boolean oracle. Now you can ask the database yes/no questions and get
answers via page behavior. Wrap the boolean around anything you want to
know:

```
xyz' AND SUBSTRING((SELECT Password FROM Users WHERE Username = 'Administrator'), 1, 1) > 'm
```

That request returns "Welcome back" if the first character of the
administrator's password is greater than `m`, and doesn't otherwise. Do
that in a binary search per character, and you have the whole password.

Blind SQLi comes in a few flavors - conditional responses (above),
conditional errors, and time-based. We cover the first two in
[the next](blind-sql-injection-with-conditional-responses.html)
[couple](blind-sql-injection-with-conditional-errors.html) of posts.

## What Ties Them Together

Every one of these attacks is a variation on the same theme: a user input
is being pasted directly into a SQL query, and the attacker can supply
SQL syntax that changes the meaning of the query. The fix is the same in
every case: parameterized queries. Not string concatenation. Not escaping.
Parameterized queries.

## References

* Our wiki: [SQL Injection](https://charlesreid1.com/wiki/SQL_Injection)
* [PortSwigger SQL Injection cheat sheet](https://portswigger.net/web-security/sql-injection/cheat-sheet)
* [Web Security Academy - SQL Injection](https://portswigger.net/web-security/sql-injection)
