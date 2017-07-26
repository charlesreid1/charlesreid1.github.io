Title: Computing Square Roots: Part 2: Using Continued Fractions
Date: 2017-07-14 20:00
Category: Mathematics
Tags: computer science, java, mathematics, square roots, numerical methods, continued fractions

## Table of Contents

* [Number Systems and Representations](#cf-number-systems)
* [Continued Fraction Representations](#cf-cf)
* [Convergents of Continued Fractions](#cf-convergents)
* [Example: Continued Fraction Coefficients of $\sqrt{14}$](#cf-example-coeffs)
* [Example: Convergents of $\sqrt{14}$](#cf-example-convergents)
* [Approximating Square Roots](#cf-sqrt-approx)


<a name="cf-number-systems"></a>
## Continued Fractions

Let's start part 2 of our discussion of computing square roots by talking about 
continued fractions. When we first learn mathematics, we learn to count in the 
base 10 system: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9. We can construct representations of 
all of the integers using these 10 digits, by arranging them in a different order.
So, for example, saying 125 is equivalent to saying:

$$
125 = 1 \times 10^2 + 2 \times 10^1 + 5 \times 10^0
$$

Later on in our mathematical lives, we learn that we can use other integers
as our base, or **radix**, by decomposing 125 into powers of that integer. For example, 125
can be decomposed into powers of 2. In a base 2 system, we have only two symbols,
0 and 1, so 125 can be represented as 1111101, which is equivalent to saying:

$$
125 = 1 \times 2^6 + 1 \times 2^5 + 1 \times 2^4 + 1 \times 2^3 + 1 \times 2^2 + 1 \times 2
$$

Note that 1111101 is close to 1111111, which is $2^7 = 128$.

As Knuth points out in his <u>Art of Computer Programming</u>, Part II:

<blockquote>
<i>"If our ancestors had invented arithmetic by counting with their two fists
or their eight fingers, instead of their ten "digits," we would never have to 
worry about writing binary-decimal conversion routines. (And we would perhaps
never have learned as much about number systems.)
</i>
</blockquote>

This idea of an alternative radix to the traditional base 10 leads to entirely new 
number systems with their own interesting properties. However, it goes even further - 
as a high school student in 1955, Donald Knuth invented a number system with an
imaginary, 4-symbol radix in base $2i$ (where $i = \sqrt{-1}$), called 
the [quater-imaginary base](https://en.wikipedia.org/wiki/Quater-imaginary_base).

There are also number systems that use an irrational radix, such as 
[phinary](https://en.wikipedia.org/wiki/Golden_ratio_base), which uses the golden ratio
as its radix. Thus, the Golden Ratio $\phi = \dfrac{1 + \sqrt{5}}{2}$ becomes $\phi = 1$,
$2 = \phi^1 + \phi^-2$ becomes $2 = 10.01$, $5 = \phi^3 + \phi^{-1} + \phi^{-4}$ 
becomes $5 = 1000.1001$, and so on. In the case of the irrational number $\sqrt{5}$, 
this number becomes a rational number in base $\phi$: $\sqrt{5} = \phi^2 + \phi^{-1}$ 
becomes $\sqrt{5} = 10.1$.

The single central idea behind these number systems is that the abstract 
set of integers $\mathbb{Z}$ are being represented on an [algebraic ring](https://en.wikipedia.org/wiki/Ring_(algebra)),
which is a fundamental mathematical object. Initially the idea of a ring
may seem strange, but it creates the foundations of modern number theory.

<a name="cf-cf"></a>
## Continued Fraction Representations

(Note that while the next two sections will have a lot of "magic numbers," we will
step through the procedure in the following sections, and it will be more clear
where these numbers come from. There is also an excellent continued fractions calculator
available online [here](http://www.maths.surrey.ac.uk/hosted-sites/R.Knott/Fibonacci/cfCALC.html).)

We can use other kinds of mathematical objects to represent different numbers.
Another technique is to use continued fractions to represent numbers.
These are well-studied mathematical objects that date back to Euclid's <u>Elements</u>.
The basic idea is to create a recursive expression that involves fractions nested
beneath other fractions:

$$
a_0+\cfrac{1}{a_1 +\cfrac{1}{a_2 +\cfrac{1}{
      \begin{array}{@{}c@{}c@{}c@{}}
        a_3 + {}\\ &\ddots\\ &&{}+ \cfrac{1}{a_n}
      \end{array}
}}}
$$

For ease of writing, this is often written as:

$$
a_0 + \dfrac{1}{a_1 +} \quad \dfrac{1}{a_2 +} \quad \dfrac{1}{a_3 + } \quad \dots \quad \dfrac{1}{a_{n-1} + } \quad \dfrac{1}{a_n}
$$

or, even shorter,

$$
[a_0; a_1, a_2, a_3, \dots]
$$

These variables $a_i$ are called the terms of the continued fraction.
Continued fractions can be used to represent rational numbers, in which case the continued fraction
representation terminates after a finite number of terms. For example, $\dfrac{125}{3} = [41; 1, 2]$, 

$$
\dfrac{125}{3} = 41 +\cfrac{1}{1 +\cfrac{1}{2}} 
$$

Continued fractions can also be used to represent irrational numbers, 
in which case the continued fraction representation is a repeating pattern
of variable length. For example, $\sqrt{14} = [3; \overline{1,2,1,6}]$, where
the line over the last digits indicates that the pattern repeats infinitely as
$1, 2, 1, 6, 1, 2, 1, 6, 1, 2, 1, 6, \dots$:

$$
3 + \cfrac{1}{
	1 + \cfrac{1}{
		2+\cfrac{1}{
			1+\cfrac{1}{
				6+\cfrac{1}{
					\begin{array}{@{}c@{}c@{}c@{}}
						1 + {}\\ &\ddots\\ &&{}
	      			\end{array}
				}
			}
		}
	}
}
$$				

A few useful properties of these patterns, for square roots, are:

* First, the integer portion (3 in the case above) is the largest integer 
	whose square is less than the number (14).

* Second, the sequence of integers that repeats is always palindromic,
	and it always begins repeating once it reaches a value of $2 a_0$.

Here are a few more square roots represented as continued fractions, to help illustrate
the above properties:

$$
\begin{array}
_ \sqrt{19} &=& [4; \overline{2, 1, 3, 1, 2, 8}] \\
\sqrt{115} &=& [10; \overline{1, 2, 1, 1, 1, 1, 1, 2, 1, 20}] \\
\sqrt{988} &=& [31; \overline{2, 3, 4, 1, 20, 6, 1, 14, 1, 6, 20, 1, 4, 3, 2, 62}]
\end{array}
$$ 

## Convergents 

We will show an example of how to compute a continued fraction in the next section, 
but we will cover one additional topic first. In order to be useful, we need some way
to evaluate the continued fraction representation. One way to do this is to repeatedly
compute common denominators, perform the fraction addition, and inert the result. 
The fraction that results is equivalent to the continued fraction expression, but is 
a rational number and therefore easier to evaluate. 

It turns out that this rational number is a very important quantity called the **convergent** 
of $\sqrt{n}$. However, it is cumbersome to perform the operation of de-rationalizing 
the continued fraction. There is a useful shortcut that takes the form of a recurrence relation.

The $n^{th}$ convergent is defined as the rational number that results when the continued fraction
representation is carried out to $n$ terms, then expanded and simplified into a rational number.
If a number like $\sqrt{19}$ has an infinite continued fraction representation, it means we can compute
progressively more accurate rational approximations. 

For example, we know from the above that $\sqrt{19} = [4; \overline{2,1,3,1,2,8}]$. Using this fact,
we can use successive terms to write successive linear approximations:

$$
\begin{array}
_ \sqrt{19}	&\approx& 4 \\
\quad		&\approx& 4 + \frac{1}{2+0} \approx \frac{9}{2} \\
\quad 		&\approx& 4 + \cfrac{1}{2+\cfrac{1}{1}} \approx \frac{13}{3} \\
\quad 		&\approx& 4 + \cfrac{1}{2+\cfrac{1}{\cfrac{1}{3}}} \approx \frac{48}{11} \\
\end{array}
$$

If we continue this sequence, we get a slew of approximations (there are also additional approximations between
each of *these* terms...):

$$
\begin{array}
_ \sqrt{19}	&\approx& \frac{61}{14} \\
\quad 		&\approx& \frac{170}{39} \\
\quad 		&\approx& \frac{1421}{326} \\
\quad 		&\approx& \frac{3012}{691} \\
\quad 		&\approx& \frac{4433}{1017} \\
\sqrt{19}   &\approx& \frac{16311}{3742}
\end{array}
$$

The numerator and denominator of the $k^{th}$ convergent are denoted $P_k$ and $Q_k$, 
respectively, and can be computed through the recurrence relation:

$$
\dfrac{P_k}{Q_k} = \dfrac{a_k P_{k-1} + P_{k-2}}{a_k Q_{k-1} + Q_{k-2}}
$$

where the initial values are $P_{-1} = 1, P_{-2} = 0, Q_{-1} = 0, Q_{-2} = 1$
(making the first convergent equal to $\frac{a_0}{1}$).
This can be used to compute successive approximations.
Note that on a computational platform, you will quickly reach the end 
of your accuracy limit, so care must be taken for continued fraction
sequences of longer than about 10 terms.

<a name="cf-example-coeffs"></a>
## Example: Continued Fraction Coefficients of $\sqrt{14}$

Let's walk through an example of how to compute the continued fraction 
representation $[a_0; a_1, a_2, \dots, a_n]$ for a square root,
and how to compute the $k^{th}$ convergent.

Begin with the square root of a given number. For variety, we will use $\sqrt{14}$.
We begin by computing the nearest integer to 14's square root. If we don't have a 
square root routine, we can try integers by squaring them, and find the last integer
that, when squared, is less than 14. This is $a_0 = 3$. To interpret, $a_0$ is 
the largest integer portion of our square root, with the residual portion 
$\sqrt{14}-3$ the portion that will be represented by the continued fraction.

Here's what we have:

$$
\sqrt{14} = 3 + (\sqrt{14} - 3) \\
$$

We can drop the residual for an initial rational approximation of $\sqrt{14} \approx 13$,
but we can do better by going another step.

We recognize that the residual, which we want write in the form $\dfrac{1}{\mbox{something}}$,
can be written as $\dfrac{1}{\dfrac{1}{\sqrt{14}-3}}$: 

$$
\sqrt{14} = 3 + \dfrac{1}{ \frac{1}{\sqrt{14}-3} }
$$

Now examine the inverse residual term $\dfrac{1}{\sqrt{14}-3}$ for step 1,
which we will call $r_1$. 
Repeat the procedure we performed above: find the nearest integer 
portion to this quantity. In this case,

$$
\dfrac{1}{r_1} = \dfrac{1}{\sqrt{14}-3} = 1.34833...
$$

Now split this into its integer portion, which becomes $a_1$, 
and its remaining fractional portion, .34833...:

$$
a_1 = floor( \dfrac{1}{r_1} )
$$

and the new residual $r$ is written in terms of the old residual
and the coefficent $a_i$:

$$
r_2 = \dfrac{1}{r_1} - a_1
$$

Generalizing, we get an iterative procedure to determine the 
coefficients $a_i$:

$$
a_i = floor( \dfrac{1}{r_i} )
$$

followed by:

$$
r_{i+1} = \dfrac{1}{r_i} - a_i
$$

where the initial values $a_0, r_0$ are computed as mentioned above,
and the rest of the values in the sequence follow.

Continuing for $\sqrt{14}$, we get:

$$
\begin{array}
_ a_0 &=& 3 \\
r_1 &=& \dfrac{1}{\sqrt{14}-3} = 1.348331 \\
a_1 &=& 1 \\
r_2 &=& \dfrac{1}{.348331} = 2.870829 \\
a_2 &=& 2 \\
r_3 &=& \dfrac{1}{0.870829} = 1.1483311 \\
a_3 &=& 1 \\
r_4 &=& \dfrac{1}{0.1483311} = 6.741676 \\
a_4 &=& 6
\end{array}
$$

It is at this point that we see $2 a_0$ and know that our (palindromic) 
sequence will repeat. (When we evaluate the convergents, we will utilize
the palindromic nature of this sequence.)

Collecting these terms gives us the expected result: $\sqrt{14} = [3; 1, 2, 1, 6]$.

This gives us an algorithmic procedure for computing the 
continued fraction representation $[a_0; a_1, a_2, a_n]$ of a number -
with the important caveat, as mentioned above, that some integers
have sequences that are extremely long before they repeat, making it 
impossible to find the full continued fraction representation 
without arbitrary precision libraries.

That being said, if you are only interested in the first 10 or so
terms of the continued fraction representation, here is a 
static Java method to compute them:

```java
	/** Find the (shorter than 10) continued fraction sequence for sqrt(n). 
	 * This returns a list of integers, [a0, a1, a2, ...]
	 *
	 * @params n Number to compute the square root of.
	 */
	public static List<Integer> continuedFractionSqrt(int n) {
		if(isPerfectSquare(n)) {
			throw new IllegalArgumentException("Error: n cannot be a perfect square.");
		}
		int niters = 10; // handbrake

		int ai = 0;
		double val = 0;
		double remainder = 0;
		List<Integer> coeffs = new ArrayList<Integer>();

		// Fencepost
		remainder = 1.0/Math.sqrt(n);

		for(int i=0; i<niters; i++) {
			val = 1.0/remainder;
			ai = floor(val);
			remainder = val - ai;
			coeffs.add(ai);
			if(coeffs.get(i) == 2*coeffs.get(0)) {
				break;
			}
		}
		return coeffs;
	}

	/** Check if x is a perfect square. */
	public static boolean isPerfectSquare(int x) { 
		int s = (int)(Math.round(Math.sqrt(x)));
		return x==(s*s);
	}

	/** Find the floor of a double. */
	public static int floor(double j) {
		return (int)(Math.floor(j));
	}
```

Here is a short program that uses this routine to compute 
the continued fraction representation of $\sqrt{14}$:

```java
public class SquareRootCF {
	public static void main(String[] args) {
		System.out.println("sqrt(14) = "+Convergents.continuedFractionSqrt(14));
		System.out.println("sqrt(19) = "+Convergents.continuedFractionSqrt(19));
	}
}
```

and the corresponding output:

```plain
$ javac SquareRootCF.java && java SquareRootCF
sqrt(14) = [3, 1, 2, 1, 6]
sqrt(19) = [4, 2, 1, 3, 1, 2, 8]
```

<a name="cf-example-convergents"></a>
## Example: Convergents of $\sqrt{14}$

We now turn to the task of computing the convergents of the continued fraction,
which will yield successive rational numbers that are progressively better approximations
to $\sqrt{14}$. 

We start with the expression given above for the $k^{th}$ convergent: 

$$
\dfrac{P_k}{Q_k} = \dfrac{a_k P_{k-1} + P_{k-2}}{a_k Q_{k-1} + Q_{k-2}}
$$

with initial values $P_{-1} = 1, P_{-2} = 0, Q_{-1} = 0, Q_{-2} = 1$. This yields 
the first "real" convergent:

$$
\dfrac{P_1}{Q_1} = \dfrac{a_0 + 0}{0 + 1} = 4
$$

Successive approximations will use the values $P_1$ and $Q_1$ to compute
the next convergents.

$$
\dfrac{P_2}{Q_2} = \dfrac{P_1 a_1 + P_0}{Q_1 a_1 + Q_0} = \frac{11}{3}
$$

Continuing in this fashion gives:

$$
\begin{array}
\quad \dfrac{P_2}{Q_2} &=& \dfrac{15}{4} \\
\dfrac{P_3}{Q_3} &=& \dfrac{11}{3}
\end{array}
$$

and so on. This recurrence relation is easy to code up. It starts with 
the continued fraction coefficients for the given square root, 
and computes successive values of P and Q. The number of terms computed
is specified by the user. Once it reaches the end of the sequence of 
continued fraction coefficients, it can start at the beginning again 
(the sequence is palindromic). 

Finally, it returns the values of $P_k$ and $Q_k$, and of the 
successive convergents:

$$
\begin{array}
_ \sqrt{14} &\approx& 3 \\
&\approx& 4 \\
&\approx& 11/3 \\
&\approx& 15/4 \\
&\approx& 101/27 \\
&\approx& 116/31 \\
&\approx& 333/89 \\
&\approx& 449/120 \\
&\approx& 3027/809 \\
&\approx& 3476/929 \\
&\approx& 9979/2667 
\end{array}
$$

Here is a static method in Java that will compute the convergents
of a square root:

```java
	/** 
	 * Compute the convergents (rational representation of
	 * continued fraction).
	 *
	 * This uses the recurrence relation:
	 *
	 * P_n     a_n P_n-1  + P_n-2
	 * ---- = -----------------
	 *  Q_n    a_n Q_n-1  + Q_n-2
	 */
	public static long[] convergents(int n, int nterms) {
		long[] convergents = new long[2];

		List<Integer> cfrepr = continuedFractionSqrt(n);

		// Initial values for convergent recurrence relation
		long Pnm2 = 0; // P_{n-2}
		long Pnm1 = 1;
		long Qnm2 = 1;
		long Qnm1 = 0;
		long P = 0;
		long Q = 0;

		// Term 0 is the constant value a0.
		int accessindex = 0;
		for(int i=0; i<=nterms; i++) { 
			int an = cfrepr.get(accessindex);

			P = an * Pnm1 + Pnm2;
			Q = an * Qnm1 + Qnm2;

			Pnm2 = Pnm1;
			Pnm1 = P;

			Qnm2 = Qnm1;
			Qnm1 = Q;

			if(accessindex+1>=cfrepr.size()) { 
				// Ensure we keep repeating the sequence
				// if the sequence has fewer terms than
				// the user asks for.
				// This allows us to get really good
				// approximations for numbers.
				// This only works because the sequence
				// is palindromic.
				accessindex = 1;
			} else {
				accessindex++;
			}
		}

		convergents[0] = P;
		convergents[1] = Q;

		return convergents;
	}
```

Here is a simple driver program that prints out several
convergents for $\sqrt{14}$:

```java
public class SquareRootCF {
	public static void main(String[] args) {
		for(int i=1; i<=10; i++) {
			long[] conv = Convergents.convergents(14,i);
			System.out.println("Convergent "+i+": "+conv[0]+"/"+conv[1]);
		}
	}
}
```

and the corresponding console output:

```plain
$ javac SquareRootCF.java && java SquareRootCF
Convergent 1: 4/1
Convergent 2: 11/3
Convergent 3: 15/4
Convergent 4: 101/27
Convergent 5: 116/31
Convergent 6: 333/89
Convergent 7: 449/120
Convergent 8: 3027/809
Convergent 9: 3476/929
Convergent 10: 9979/2667
```

<a name="cf-sqrt-refs"></a>
# References

1. Hardy, G. H. <u>A Course of Pure Mathematics.</u> 
Cambridge University Press, Tenth Edition (1908-1967).

2. Knuth, Donald. <u>The Art of Computer Programming, Volume 2: Seminumerical Algorithms.</u> 
Addison-Wesley Publishing Company, Second Edition (1975).



