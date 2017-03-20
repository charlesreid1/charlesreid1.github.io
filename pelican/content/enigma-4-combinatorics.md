Title: Enigma Cipher Implementation: Part 4: Combinatorics
Status: draft
Date: 2017-03-21 16:00
Category: Enigma
Tags: ciphers, enigma, encryption, java

In this, the fourth article in a series on implementing the Enigma cipher in Java,
we use some big number libraries to explore the combinatorics of the Enigma encryption scheme
and better understand the Enigma's strengths and weaknesses. 

## The Keyspace

Basically, what the Enigma did was to encrypt each character of a message one at a time, using a different, unique key for each character. 
One key corresponded to one particular scrambled version of the alphabet (one possible set of substitutions). 
The huge number of possible initial settings for the machine - the rotors, wiring, and reflector - meant that finding the very first key was extremely difficult. 
Furthermore, as the operator entered additional characters into the Enigma, the machine would rotate the rotor wheels, 
sequentially stepping through the space of possible keys in a totally random but deterministic way. 
Any operator with a matching Enigma machine and matching settings could replicate this "random walk" through the key space.

What we will do below is look at each component of the Enigma and determine the total number of 
unique settings for each component. A single machine setting corresponds to a single key, 
so the total number of possible settings of the machine yields the total number of possible keys for the Enigma.

## The Switchboard

The switchboard at the front of the Enigma consisted of a set of plugs, one for each letter, connected by wires.
The operator would connect pairs of wires to swap pairs of letters. If the letters A and K were connected, 
any A signal entering the keyboard would become a K signal leaving the keyboard, 
and any K signal entering the keyboard would become an A signal leaving the keyboard.
Letters could not be connected to themselves, and a wire could only connect two letters together.

From these constraints, we can get the total number of cable configurations on the front of the machine.
For a machine with $S$ symbols (typically 26) and $N$ patch cables, the total number of configurations is:

$$
C = \dfrac{ S! }{ N! \times (S - 2N)! \times 2^N }
$$

Let's break down where those terms are coming from.

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

### More Cables

If we plug in a second cable, there are now 2 choices occupied by the first letter, 
so there are $S-2$ possible places to plug in the left end,
and $S-3$ possible places to plug in the right end,
for a total of $(S-2)(S-3)$ combinations.

### Many Cables

Once $N$ wires have been plugged in, there are $S - 2N$ spaces remaining, and $2N$ spaces occupied by plug ends. 
That is, we are reducing the number of choices by 2 letters with each wire placed.

Taking the product of these numbers explains part of the expression given above: 

$$
S \times (S-1) \times (S-2) \times \dots \times (S - 2N + 1) = \dfrac{ S! }{ (S - 2N) ! }
$$ 


### Accounting for Duplicates

But where did the $2^N$ and $N!$ terms come from? They come from the fact that many choices of wiring configurations are duplicates.

The $2^N$ term comes from the fact that the wires are doubled up, so that if A connects to B, B connects to A.
This means that when we choose our pair and connect A to B using a wire, we also connect B to A. 
Even though it looks like two choices, it is only one!

Meanwhile, the $N!$ term accounts for the fact that order is not important when we select pairs and place wires -
making the choice to connect A to B and then making the choice to connect C to D 
is entirely equivalent to connecting C to D, then connecting A to B.
This means that $N!$ of the $S!$ possible solutions are duplicate configurations 
with the same connections chosen in a different order.


## The Rotors

Typical Enigma machines had three rotors, with each rotor implementing a different scrambled alphabet.
Assuming there are P possible rotors to choose from, the number of choices
when selecting R rotors from P possible rotors is given by:

$$
C = \dfrac{P!}{(P-R)!}
$$

If the rotors are known, $P$ and $R$ are small numbers like 8 and 3, 
yielding a modest number of possible rotor combinations (336).
If the number of rotors is unknown, however, P becomes the set of all possible rotors
(the set of all possible alphabet scrambles), which is S!. Then we take the factorial of this number,

$$
C = \frac{(S!)!}{(S!-R)!}
$$

Note that the numerator $(S!)!$ is a double factorial. For $S=26$, the numerator can be written as 
$403291461126605635584000000!$, which is *probably* the biggest number you've ever seen in your life. 
The denominator is also pretty big, though. For small values of R, this is approximately $(S!)^R$.
For a 26-character alphabet with 3 rotors, that's

$$
403,291,461,126,605,635,584,000,000^3 = 65,592,937,459,144,468,297,405,473,968,303,761,468,794,234,820,105,359,750,856,704,000,000,000,000,000,000
$$

which is a keyspace with more keys than there are [protons in the universe (the Eddington number)](https://en.wikipedia.org/wiki/Eddington_number).

In addition, each wheel had notches at different locations. The notches change the path the Enigma takes through the key space. 
For $R$ rotors containing $S$ symbols, the total combinations increases by a factor of ${S}^{R-1}$.
If there are $M$ notches, that factor is ${MS}^{R-1}$.
(The $R-1$ comes from the fact that the location of the notch on the last wheel has no effect.)

This makes the total number of rotor combinations:

$$
C = S^{R-1} \dfrac{P!}{(P-R)!}
$$



## Sources

1. "The Enigma Cipher". Tony Sale and Andrew Hodges. Publication date unknown. Accessed 18 March 2017.
<[https://web.archive.org/web/20170320081639/http://www.codesandciphers.org.uk/enigma/index.htm](https://web.archive.org/web/20170320081639/http://www.codesandciphers.org.uk/enigma/index.htm)>

