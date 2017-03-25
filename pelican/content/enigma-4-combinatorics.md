Title: Enigma Cipher Implementation: Part 4: Combinatorics
Date: 2017-03-22 19:00
Category: Enigma
Tags: ciphers, enigma, encryption, java

In this, the fourth article in a series on implementing the Enigma cipher in Java,
we use some big number libraries to explore the combinatorics of the Enigma encryption scheme
and better understand the Enigma's strengths and weaknesses. 

## Table of Contents

* [The Key Space](#keyspace)
* [The Switchboard](#switchboard)
	* [One Cable](#onecable)
  	* [More Cables](#morecables)
  	* [Many Cables](#manycables)
  	* [Accounting for Duplicates](#dupes)
  	* [Final Combination Count for Switchboard](#finalswitchboard)
* [The Rotors](#rotors)
	* [Final Combination Count for Rotors](#finalrotors)
* [The Reflector](#reflector)
	* [Final Combination Count for Reflector](#finalreflector)
* [Final Enigma Combination Count](#finalcount)
	* [Java BigInteger Combinations Program](#javabigint)


<a name="keyspace"></a>

## The Key Space

Basically, what the Enigma did was to encrypt each character of a message one at a time, using a different, unique key for each character. 
One key corresponded to one particular scrambled version of the alphabet (one possible set of substitutions). 
The huge number of possible initial settings for the machine - the rotors, wiring, and reflector - meant that finding the very first key was extremely difficult. 
Furthermore, as the operator entered additional characters into the Enigma, the machine would rotate the rotor wheels, 
sequentially stepping through the space of possible keys in a totally random but deterministic way. 
Any operator with a matching Enigma machine and matching settings could replicate this "random walk" through the key space.

What we will do below is look at each component of the Enigma and determine the total number of 
unique settings for each component. A single machine setting corresponds to a single key, 
so the total number of possible settings of the machine yields the total number of possible keys for the Enigma.

<a name="switchboard"></a>

## The Switchboard

The switchboard at the front of the Enigma consisted of a set of plugs, one for each letter, connected by wires.
The operator would connect pairs of wires to swap pairs of letters. If the letters A and K were connected, 
any A signal entering the keyboard would become a K signal leaving the keyboard, 
and any K signal entering the keyboard would become an A signal leaving the keyboard.
Letters could not be connected to themselves, and a wire could only connect two letters together.

From these constraints, we can get the total number of cable configurations on the front of the machine.
For a machine with $S$ symbols (typically 26) and $N$ patch cables, the total number of configurations is:

$$
C_{sw} = \dfrac{ S! }{ N! \times (S - 2N)! \times 2^N }
$$

Let's break down where those terms are coming from.

<a name="onecable"></a>

### One Cable 

Let's consider a single cable connecting two letters. 

There are S (or, 26) places to plug in the left end, and S places to plug in the right end, for a total of $S^2$ combinations.
But no cable can connect to itself, so there are actually $S (S-1)$ possible combinations. 
Furthermore, each plug is symmetric (if A connects to B, then B connects to A), so half of the plug combinations are simply mirror images of the other half.

For a single plug, we start from a total of $26 \times 26 = 676$ possible configurations.
Ruling out any combinations that connect letters to themselves eliminates 26 possibilities (A connects to A, B connects to B, etc.)
for a total of $26 \times 25 = 650$ possible configurations.
But half of those configurations are mirror images of the other half (if we connect A to B, by implication we connect B to A),
so our number of choices is actually half that, or $\frac{26 \times 25}{2} = 350$.


<a name="morecables"></a>

### More Cables

If we plug in a second cable, there are now 2 choices occupied by the first letter, 
so there are $S-2$ possible places to plug in the left end,
and $S-3$ possible places to plug in the right end,
but each having half duplicate solutions, since the wires are two-way,
for a total of $\frac{(S-2)(S-3)}{2 \times 2}$ combinations.

<a name="manycables"></a>

### Many Cables

Once $N$ wires have been plugged in, there are $S - 2N$ spaces remaining, and $2N$ spaces occupied by plug ends. 
That is, we are reducing the number of choices by 2 letters with each wire placed.

Taking the product of these numbers explains part of the expression given above: 

$$
S \times (S-1) \times (S-2) \times \dots \times (S - 2N + 1) = \dfrac{ S! }{ (S - 2N) ! }
$$ 

<a name="dupes"></a>

### Accounting for Duplicates

But where did the $2^N$ and $N!$ terms come from? They come from the fact that many choices of wiring configurations are duplicates.

Dividing by $2^N$ comes from the fact that the wires are doubled up: if A connects to B, B connects to A.
This means that when we choose our pair and connect A to B using a wire, we also connect B to A. 
Even though it looks like two choices, it is only one!

Meanwhile, the $N!$ term accounts for the fact that order is not important when we select pairs and place wires -
making the choice to connect A to B and then making the choice to connect C to D 
is entirely equivalent to connecting C to D, then connecting A to B.
This means that $N!$ of the $S!$ possible solutions are duplicate configurations 
with the same connections chosen in a different order.

<a name="moreinteresting"></a>

### Switchboard Combinations

Here's how the number of possible combinations that result when we plug in various numbers of wires in: 

```plain
S = 2		N = 1		C = 1
S = 26		N = 1		C = 325
S = 26		N = 2		C = 44,850
S = 26		N = 3		C = 3,453,450
S = 26		N = 4		C = 164,038,875
S = 26		N = 5		C = 5,019,589,575
S = 26		N = 6		C = 100,391,791,500
S = 26		N = 7		C = 1,305,093,289,500
S = 26		N = 8		C = 10,767,019,638,375
S = 26		N = 9		C = 53,835,098,191,875
S = 26		N = 10		C = 150,738,274,937,250
S = 26		N = 11		C = 205,552,193,096,250
S = 26		N = 12		C = 102,776,096,548,125
S = 26		N = 13		C = 7,905,853,580,625
```

Notice the bump in the shape of the distribution, meaning the use of 11 wires is much more secure than the use of 13 wires.
Let's explore that.

### More Interesting Observations About the Switchboard

Notice how the switchboard expression is *not* proportional to $N$,
it is inversely proportional to two different terms, each changing differently
as $N$ changes.

We are looking at the denominator of this expression:

$$
C_{sw} = \dfrac{ S! }{ N! \times (S - 2N)! \times 2^N }
$$

The term $N!$ on the bottom will increase as $N$ increases, thereby decreasing the total number of possible keys $C_{sw}$.
However, the term $(S - 2N)!$ will decrease as $N$ increases, thereby increasing the total number of possible keys $C_{sw}$.
The tradeoff can be visualized just by printing it out - here are the total number of combinations that are possible
for an alphabet of $S = 26$ symbols, using $N = 1 \dots 13$ wires:

This pattern holds for other alphabet sizes. Here's a 52-character alphabet:

```plain
S = 52		N = 1		C = 1,326
S = 52		N = 2		C = 812,175
S = 52		N = 3		C = 305,377,800
S = 52		N = 4		C = 79,016,505,750
S = 52		N = 5		C = 14,949,922,887,900
S = 52		N = 6		C = 2,145,313,934,413,650
S = 52		N = 7		C = 239,049,266,977,521,000
S = 52		N = 8		C = 21,006,454,335,649,657,875
S = 52		N = 9		C = 1,470,451,803,495,476,051,250
S = 52		N = 10		C = 82,492,346,176,096,206,475,125
S = 52		N = 11		C = 3,719,654,882,122,156,219,242,000
S = 52		N = 12		C = 134,837,489,476,928,162,947,522,500
S = 52		N = 13		C = 3,920,659,309,406,065,045,704,885,000
S = 52		N = 14		C = 91,015,305,396,926,509,989,577,687,500
S = 52		N = 15		C = 1,674,681,619,303,447,783,808,229,450,000
S = 52		N = 16		C = 24,178,215,878,693,527,378,731,312,684,375
S = 52		N = 17		C = 270,227,118,644,221,776,585,820,553,531,250
S = 52		N = 18		C = 2,296,930,508,475,885,100,979,474,705,015,625
S = 52		N = 19		C = 14,506,929,527,216,116,427,238,787,610,625,000
S = 52		N = 20		C = 66,006,529,348,833,329,743,936,483,628,343,750
S = 52		N = 21		C = 207,449,092,239,190,464,909,514,662,831,937,500
S = 52		N = 22		C = 424,327,688,671,071,405,496,734,537,610,781,250
S = 52		N = 23		C = 516,572,838,382,173,884,952,546,393,613,125,000
S = 52		N = 24		C = 322,858,023,988,858,678,095,341,496,008,203,125
S = 52		N = 25		C = 77,485,925,757,326,082,742,881,959,041,968,750
S = 52		N = 26		C = 2,980,227,913,743,310,874,726,229,193,921,875
```

For a 52-symbol alphabet the optimum number of pairs is 23 keys.

Okay, here we go with an alphabet of 100 characters:

```plain
S = 100		N = 1		C = 4,950
S = 100		N = 2		C = 11,763,675
S = 100		N = 3		C = 17,880,786,000
S = 100		N = 4		C = 19,539,228,901,500
S = 100		N = 5		C = 16,358,242,436,335,800
S = 100		N = 6		C = 10,919,126,826,254,146,500
S = 100		N = 7		C = 5,971,202,498,700,124,686,000
S = 100		N = 8		C = 2,728,093,141,593,619,465,916,250
S = 100		N = 9		C = 1,056,681,410,177,261,939,798,227,500
S = 100		N = 10		C = 350,923,896,319,868,690,206,991,352,750
S = 100		N = 11		C = 100,810,864,760,980,460,095,826,606,790,000
S = 100		N = 12		C = 25,227,918,906,435,360,138,980,608,349,197,500
S = 100		N = 13		C = 5,530,736,067,949,290,492,007,287,215,016,375,000
S = 100		N = 14		C = 1,067,037,008,537,930,972,779,405,911,982,802,062,500
S = 100		N = 15		C = 181,823,106,254,863,437,761,610,767,401,869,471,450,000
S = 100		N = 16		C = 27,443,925,100,343,450,137,143,125,204,719,673,346,984,375
S = 100		N = 17		C = 3,677,485,963,446,022,318,377,178,777,432,436,228,495,906,250
S = 100		N = 18		C = 438,233,743,977,317,659,606,613,804,310,698,650,562,428,828,125
S = 100		N = 19		C = 46,498,906,729,382,757,987,733,338,394,229,919,975,466,132,500,000
S = 100		N = 20		C = 4,396,471,631,263,139,767,740,187,145,174,438,933,680,322,827,875,000
S = 100		N = 21		C = 370,559,751,777,893,208,995,244,345,093,274,138,695,912,924,063,750,000
S = 100		N = 22		C = 27,842,512,258,584,430,657,688,131,929,053,734,148,379,275,612,608,125,000
S = 100		N = 23		C = 1,864,237,777,313,914,052,732,161,876,988,815,242,978,438,454,061,587,500,000
S = 100		N = 24		C = 111,155,177,472,342,125,394,155,151,915,458,108,862,589,392,823,422,154,687,500
S = 100		N = 25		C = 5,895,670,613,133,026,330,905,989,257,595,898,094,071,741,395,354,311,084,625,000
S = 100		N = 26		C = 277,776,788,503,382,971,359,993,724,636,729,814,047,610,892,665,731,964,564,062,500
S = 100		N = 27		C = 11,604,896,941,919,110,803,484,182,273,712,267,786,877,966,182,479,468,741,787,500,000
S = 100		N = 28		C = 428,966,726,245,938,560,057,361,737,617,578,469,979,239,107,102,366,076,705,359,375,000
S = 100		N = 29		C = 13,993,190,449,264,064,752,216,007,027,111,352,848,288,282,597,201,320,984,940,343,750,000
S = 100		N = 30		C = 401,604,565,893,878,658,388,599,401,678,095,826,745,873,710,539,677,912,267,787,865,625,000
S = 100		N = 31		C = 10,104,889,077,329,850,114,293,791,397,061,765,963,283,274,007,127,379,728,028,210,812,500,000
S = 100		N = 32		C = 221,991,781,917,590,144,698,391,729,754,200,671,005,879,425,844,079,623,400,119,756,287,109,375
S = 100		N = 33		C = 4,238,024,927,517,630,035,151,114,840,762,012,810,112,243,584,296,065,537,638,649,892,753,906,250
S = 100		N = 34		C = 69,927,411,304,040,895,579,993,394,872,573,211,366,852,019,140,885,081,371,037,723,230,439,453,125
S = 100		N = 35		C = 990,971,314,480,122,405,933,620,681,622,751,795,370,245,756,967,971,438,858,134,592,065,656,250,000
S = 100		N = 36		C = 11,974,236,716,634,812,405,031,249,902,941,584,194,057,136,230,029,654,886,202,459,654,126,679,687,500
S = 100		N = 37		C = 122,331,391,321,296,191,597,346,282,792,214,022,306,853,986,350,032,690,459,041,344,574,591,484,375,000
S = 100		N = 38		C = 1,046,255,320,511,085,849,187,830,050,196,567,296,045,461,725,362,121,694,715,485,183,861,637,695,312,500
S = 100		N = 39		C = 7,404,268,422,078,453,701,944,643,432,160,322,402,783,267,594,870,399,685,678,818,224,251,589,843,750,000
S = 100		N = 40		C = 42,759,650,137,503,070,128,730,315,820,725,861,876,073,370,360,376,558,184,795,175,245,052,931,347,656,250
S = 100		N = 41		C = 198,154,476,246,965,446,938,018,536,730,193,018,450,096,106,548,086,489,149,050,812,111,220,901,367,187,500
S = 100		N = 42		C = 721,848,449,185,374,128,131,353,240,945,703,138,639,635,816,710,886,496,185,827,958,405,161,854,980,468,750
S = 100		N = 43		C = 2,014,460,788,424,299,892,459,590,439,848,473,875,273,402,279,193,171,617,262,775,697,874,870,292,968,750,000
S = 100		N = 44		C = 4,166,271,176,059,347,504,859,607,500,595,707,332,951,809,259,240,423,117,520,740,647,877,572,651,367,187,500
S = 100		N = 45		C = 6,110,531,058,220,376,340,460,757,667,540,370,754,995,986,913,552,620,572,363,752,950,220,439,888,671,875,000
S = 100		N = 46		C = 5,977,693,426,519,933,376,537,697,718,246,014,869,017,813,284,997,128,820,790,627,886,085,212,934,570,312,500
S = 100		N = 47		C = 3,561,179,062,607,619,883,894,798,640,657,200,347,499,973,871,913,183,127,279,522,995,965,658,769,531,250,000
S = 100		N = 48		C = 1,112,868,457,064,881,213,717,124,575,205,375,108,593,741,834,972,869,727,274,850,936,239,268,365,478,515,625
S = 100		N = 49		C = 136,269,606,987,536,475,149,035,662,270,045,931,664,539,816,527,290,170,686,716,441,172,155,310,058,593,750
S = 100		N = 50		C = 2,725,392,139,750,729,502,980,713,245,400,918,633,290,796,330,545,803,413,734,328,823,443,106,201,171,875
```

Optimum number of pairs? 45.


<a name="finalswitchboard"></a>

### Final Combination Count Switchboard

For a switchboard with holes for each of $S$ symbols, with $N$ unique pairs of letters chosen from among the symbols to be swapped by the switchboard,
the number of possible combinations of ciphers with $N$ wires is:

$$
C_{sw} = \dfrac{ S! }{ N! \times (S - 2N)! \times 2^N }
$$

<a name="rotors"></a>

## The Rotors

Typical Enigma machines had three rotors, with each rotor implementing a different scrambled alphabet.
Assuming there are P possible rotors to choose from, the number of choices
when selecting R rotors from P possible rotors is given by:

$$
C_{rot} = \dfrac{P!}{(P-R)!}
$$


If the rotors are known, $P$ and $R$ are small numbers like 8 and 3, 
yielding a modest number of possible rotor combinations (336).
If the number of rotors is unknown, however, P becomes the set of all possible rotors
(the set of all possible alphabet scrambles), which is S!. Then we take the factorial of this number,

$$
C_{rot} = \frac{(S!)!}{(S!-R)!}
$$

Note that the numerator $(S!)!$ is a double factorial. [Here's how Wolfram Alpha describes 26 double-factorial (26!)!](http://www.wolframalpha.com/input/?i=(26!)!)

$$
10^{10^{28}}
$$

This can also be written as $403291461126605635584000000!$.
This is a number with 10^28 digits. That's *probably* the biggest number you've ever seen in your life. 
The denominator is also pretty big, though. For small values of R, this is approximately $(S!)^R$.
For a 26-character alphabet with 3 rotors, that's approximately

$$
(403,291,461,126,605,635,584,000,000)^3 = 65,592,937,459,144,468,297,405,473,968,303,761,468,794,234,820,105,359,750,856,704,000,000,000,000,000,000
$$

which is a key space with more keys than there are [protons in the universe (the Eddington number)](https://en.wikipedia.org/wiki/Eddington_number).

In addition, each wheel had notches at different locations. The notches change the path the Enigma takes through the key space. 
For $R$ rotors containing $S$ symbols, the total combinations increases by a factor of ${S}^{R-1}$.
If each wheel has $M$ notches, that factor is ${(MS)}^{R-1}$.
(The $R-1$ comes from the fact that the location of the notch on the last wheel has no effect.)

<a name="finalrotors"></a>

### Final Combination Count for Rotors

The total number of combinations for $R$ rotors with $S$ symbols and $M$ notches (which advance the neighboring left wheel by one), 
chosen from among $P$ possible choices of rotors, is given by:

$$
C_{rot} = S^{R-1} \dfrac{P!}{(P-R)!}
$$

**NOTE:** For a very large set of possible rotors $P$, ($P >> R$), 

$$
\dfrac{P!}{(P-R)!} \approx P^R
$$

so it follows that 

$$
C_{rot} \approx S^{R-1} P^R \qquad P >> R
$$

(For example, if $P = S!$, the set of all possible rotors.)

<a name="reflector"></a>

## Reflector 

Like the switchboard on the front of the Enigma, the reflector connected pairs of letters.
It could only be changed by swapping it out like a rotor, so there were a small number of mechanically produced reflectors
chosen from the set of all possible reflectors.

If a reflector pairs all letters with another letter, it makes $N = \frac{S}{2}$ possible pairs. 
Using the analysis we performed above for the switchboard, and plugging that in, and using $0!=1$:

$$
C_{rfl} = \dfrac{ S! }{ (\frac{S}{2})! \times (S - 2(\frac{S}{2}))! \times 2^S } = \dfrac{S!}{(\frac{S}{2})! 2^S}
$$

For the 26 characters in the English alphabet, that's:

$$
C_{rfl} = \frac{26!}{13! * 2^26 } = 965,070,017
$$

This is the total number of *possible* reflectors. (Curiously enough, the number of possible keys goes down as N goes from 11 to 12 and 12 to 13, 
making the switchboard on the front, which swapped 10 pairs of letters, more secure than the rotor, which swapped 13 pairs of letters.

However, like the rotors, there were a finite number of reflectors in use.
Supposing there were Q reflectors in use, that would make for Q possible sets of the 13 letter pairings.
Since the reflectors did not rotate, this would lead to only 1 possible reflector position, meaning a choice from among
Q reflectors only multiplied the number of possible combinations by Q.

### Final Combination Count for Reflector

Here is the final expression for the total number of combinations resulting from all possible rotors:

$$ 
C_{rfl} = \dfrac{S!}{(\frac{S}{2})! 2^S} 
$$ 

and here is the final expression for the total number of combinations if there is 1 rotor chosen from among $Q$ rotors:

$$
C_{rfl} = Q
$$


## Final Enigma Combination Count

Putting all of this together results in the following monstrosity of an expression for the Enigma's *complete* key space:

$$
C_{enigma-full} = 
\left( \dfrac{S!}{N! (S-2N)! 2^N} \right) 
\left( \dfrac{(S!)!}{(S!-R)!} \right) 
\left( \dfrac{ S! }{ \left( \dfrac{S}{2} \right)! 2^S } \right)
$$

Note that this assumes the attacker has no idea which rotors or reflectors are actually used. If instead the attacker has knowledge that $R$ rotors out of $P$ possible rotors 
and 1 reflector out of $Q$ possible reflectors are being used, this key space reduces to:

$$
C_{enigma-small} = \left( \dfrac{S!}{N! (S-2N)! 2^N} \right) \left( S^{R-1} \dfrac{P!}{(P-R)!} \right) Q
$$

When you evaluate the above expressions for the following values of $N$, $P$, $Q$, $R$, and $S$, 
here are the actual numbers you get:

```
N = 10; // number of switchboard wires
P = 5;  // number of possible rotors
Q = 5;  // number of possible reflectors
R = 3;  // number of rotors
S = 26; // number of symbols
```

For the case of utilizing the $P$ known rotors and $Q$ known reflectors, the key space is:

$$
C_{enigma-small} = 537,293,436,636,253,096,800,000
$$

For the completely unknown case of all possible rotors and reflectors, the key space increases to an astronomical number:

$$
C_{enigma-full} = 422,732,921,460,335,478,939,047,043,039,799,222,455,533,136,281,221,092,624,796,865,514,111,348,059,884,989,972,480,000,000,000,000,000,000,000,000
$$

There are plenty of additional big numbers related to the Enigma, and more math around the weaknesses in the system and how it was cracked.
There is also yet more math around how Alan Turing managed to crack the German Navy's Enigma cipher, which utilized various protective steps like bigram replacement
that made cracking via frequency analysis much more difficult.

But that's enough for one post!

Below you can find a Java program that uses the BigInteger class, part of the Java API, to perform calculations with extremely large numbers.

### Java BigInteger Program

```java

import java.math.BigInteger;
import java.text.*;

/** Cryptanalysis of the Enigma Machine.
 *
 * This program uses combinatorics and big integers
 * to analyze the cryptographic strength of the Enigma machine.
 *
 * Author: Charles Reid
 * Date: March 2017
 */

public class Combos {
    public static void main(String[] args) { 

		// This involves a double factorial. PREPARE YOUR CPU
		boolean doBig = true;



		/////////////////////////////////
		// Git Ready

        DecimalFormat formatter = new DecimalFormat("#,###");

        BigInteger small_combos = new BigInteger("1");
        BigInteger big_combos = new BigInteger("1");

		/// Useful temp variable 
		BigInteger next;



		/////////////////////////////////
		// Constants

        int N = 10; // number of switchboard wires
        int P = 5;  // number of possible rotors
        int Q = 5;  // number of possible reflectors
        int R = 3;  // number of rotors
        int S = 26; // number of symbols




		/////////////////////////////////
		// Plugboard combinations

		BigInteger plugboard = new BigInteger("1");

		// S!/(S-2N)!
		BigInteger num = BigInteger.valueOf(1);
		for(int i=S; i>(S-2*N); i--) {
			next = BigInteger.valueOf(i);
			num = num.multiply(next);
		}

		// divided by 2^N
		BigInteger pdenom = BigInteger.valueOf(2);
		pdenom = pdenom.pow(N);

		// divided by N!
		for(int j = N; j>1; j--) { 
			next = BigInteger.valueOf(j);
			pdenom = pdenom.multiply(next);
		}

		plugboard = num.divide(pdenom);



		/////////////////////////////////
		// Rotor combinations

		BigInteger small_rotors = new BigInteger("1");
		BigInteger big_rotors = new BigInteger("1");

		// -----------------
		// Small case:
		// R rotors selected from P possible known rotors

		// Rotor wheel combinations
        for(int j=P; j>(P-R); j--) { 
            next = BigInteger.valueOf(j);
            small_rotors = small_rotors.multiply(next);
        }

        // Rotor wheel notch positions (assume 1 per wheel). 
        // Ignore left-most wheel.
        for(int k=0; k<(R-1); k++ ) {
            next = BigInteger.valueOf(S);
            small_rotors = small_rotors.multiply(next);
        }

        // Rotor wheel starting positions
        for(int k=0; k<R; k++ ) {
            next = BigInteger.valueOf(S);
            small_rotors = small_rotors.multiply(next);
        }

		// -----------------
		// Big case:
		// R rotors selected from S! possible rotors

		if(doBig) { 
			BigInteger s_rm1 = BigInteger.valueOf(S).pow(R-1);
			BigInteger sfact_r = BigInteger.valueOf(1);
			for(int j=S; j>=1; j--) { 
				next = BigInteger.valueOf(j);
				sfact_r = sfact_r.multiply(next);
			}
			sfact_r = sfact_r.pow(R);
			big_rotors = s_rm1.multiply(sfact_r);
		}

		/////////////////////////////////
		// Reflector combinations

		BigInteger small_reflector = BigInteger.valueOf(Q);
		BigInteger big_reflector = new BigInteger("1");

		// (S!)/((S/2)!)
		for(int j=S; j>(S/2); j--) {
			next = BigInteger.valueOf(j);
			big_reflector = big_reflector.multiply(next);
		}

		// divided by 2^N
		BigInteger rfldenom = BigInteger.valueOf(2);
		rfldenom = rfldenom.pow(N);

		if(doBig) { 
			big_reflector = big_reflector.divide(rfldenom);
		}



		/////////////////////////////////
		// Final combinations

		small_combos = small_combos.multiply(plugboard);
		small_combos = small_combos.multiply(small_rotors);
		small_combos = small_combos.multiply(small_reflector);

		if(doBig) {
			big_combos = big_combos.multiply(plugboard);
			big_combos = big_combos.multiply(big_rotors);
			big_combos = big_combos.multiply(big_reflector);
		}

        System.out.println("Final number of (small) Enigma combinations: ");
        System.out.println(formatter.format(small_combos));

		if(doBig) { 
			System.out.println("Final number of (big) Enigma combinations: ");
        	System.out.println(formatter.format(big_combos));
		}

    }
}

```




## Sources

1. "The Enigma Cipher". Tony Sale and Andrew Hodges. Publication date unknown. Accessed 18 March 2017.
<[https://web.archive.org/web/20170320081639/http://www.codesandciphers.org.uk/enigma/index.htm](https://web.archive.org/web/20170320081639/http://www.codesandciphers.org.uk/enigma/index.htm)>




