Title: Approximating Pi (Happy Pi Day)
Date: 2019-03-14 16:20
Category: Mathematics
Tags: pi, continued fractions, number theory, mathematics, python, irrational numbers

## Favorite Pi Approximations

What's your favorite $\pi$ approximation?

Some of my favorite approximations of $\pi$ come from
[Ramanujan-Sato series](https://en.wikipedia.org/wiki/Ramanujan%E2%80%93Sato_series).
These are mathematical series that generalize from 
a remarkable formula for $\pi$ given by [Srinivasa Ramanujana](https://en.wikipedia.org/wiki/Srinivasa_Ramanujan),
an Indian mathematician:

$$
\pi^{-1} = \dfrac{\sqrt{8}}{99^2} \sum_{k \geq 0} \dfrac{ (4k)! }{ \left( 4^k k! \right)^4 } \dfrac{ 1103 + 26390k }{ 99^{4k} } 
$$

This completely novel formula opened up new branches of mathematics
and provided a whole new class of $\pi$ approximations (the Ramanujan-Sato
series) and approximations that are extremely accurate, making them
very useful for computer applications. (Each term of the above sequence 
yields 8 additional decimal points of accuracy of $\pi$.) These 
approximations have also enabled world record calculations of 
numbers of digits of $\pi$.

But those are not the $\pi$ approximations that this blog post is about. 

This blog post is about another set of $\pi$ approximations
that I like - these come from another field Ramanujan had mastery
over, continued fractions. 

Continued fractions provide a whole alternative way of representing
all the real numbers - rational and irrational.


## Continued Fractions and Convergents

Back in [July of 2017](https://charlesreid1.github.io/computing-square-roots-part-2-using-continued-fractions.html), 
we wrote a blog post about how to find rational approximations
of square roots using continued fractions and convergents, and we
implemented a Java program to represent the irrational number 
$\sqrt{n}$ (where $n$ is not a perfect square).

In short, continued fractions are a way of expressing numbers, 
rational and irrational, in terms of recursive fractions, which 
look something like this:

$$
a_0+\cfrac{1}{a_1 +\cfrac{1}{a_2 +\cfrac{1}{
      \begin{array}{@{}c@{}c@{}c@{}}
        a_3 + {}\\ &\ddots\\ &&{}+ \cfrac{1}{a_n}
      \end{array}
}}}
$$

denoted

$$
[a_0; a_1, a_2, a_3, \dots]
$$

and called the convergents of the continued fraction.

In the denominator of the above representation, we have
a 1 in each position, which makes the continued fraction
a _simple_ continued fraction. If the denominators are 
not 1, the continued fraction is a _general_ continued
fraction.

The continued fraction expansion of any rational number
(or equivalently, the sequence of convergents) must 
terminate at some point (even if the number of terms
ends up being very large).

The convergents always terminate if a number is rational.
Conversely, if you can prove a number's continued fraction
representation is a repeated sequence or continues forever,
you can prove a number is irrational (a strategy employed in
several proofs about properties of $\pi$).

## Simple Continued Fractions to Approximate Pi

For $\pi$, the convergents of the simple continued fraction
(there is a single unique simple continued fraction representation 
of $\pi$) are unpredictable; the first few are:

$$
\pi = [3; 7, 15, 1, 292, 1, 1, 1, 2, 1, 3, 1, 14, 2...]
$$

Each additional term leads to increasingly precise
fractional approximations for $\pi$; they are:

$$
[3;7] = \dfrac{22}{7} = 3.\overline{142857}
$$

$$ 
[3;7,15] = \dfrac{333}{106} = 3.1415094...
$$

$$ 
[3;7,15,1] = \dfrac{355}{113} = 3.1415929...
$$

$$ 
[3;7,15,1,292] = \dfrac{103993}{33102} = 3.14159265...
$$

## General Continued Fractions to Approximate Pi

We mentioned above that each irrational number has a unique
representation as a simple continued fraction, equivalently a
series of convergents of that continued fraction.

However, a single number can be expressed in many different
ways as a general continued fraction. We use two variants
to generate many $\pi$ approximations:

## Odd Squares and Twos

$$
\dfrac{4}{\pi} = 1 + \cfrac{1^2}{
                        2 + \cfrac{3^2}{
                            2 + \cfrac{5^2}{
                                2 + \cfrac{7^2}{
                                    2 + \cfrac{9^2}{
                                        2 + \dots
                                    }
                                }
                            }
                        }
                    }
$$

which can be turned into $\pi$ by finding the 
convergents of the above continued fraction,
then reversing the numerator and denominator
and multilpying the new numerator by 4.

Implementing a recurrence to turn the above
into convergents and printing the first 24
terms and their approximate value:

```
                                      Pi
Convergent                                                          Approx 
--------------------------------------------------------------------------------
8 / 3                                                       	    2.6666666666666665
52 / 15                                                     	    3.4666666666666668
304 / 105                                                   	    2.8952380952380952
3156 / 945                                                  	    3.3396825396825398
30936 / 10395                                               	    2.9760461760461761
443748 / 135135                                             	    3.2837384837384835
6115680 / 2027025                                           	    3.0170718170718169
112074660 / 34459425                                        	    3.2523659347188758
1991580840 / 654729075                                      	    3.0418396189294024
44442113940 / 13749310575                                   	    3.2323158094055926
967171378320 / 316234143225                                 	    3.0584027659273318
25444221030900 / 7905853580625                              	    3.2184027659273320
655370553511800 / 213458046676875                           	    3.0702546177791836
19859578238549700 / 6190283353629375                        	    3.2081856522619421
590885791980523200 / 191898783962510625                     	    3.0791533941974261
20266826271207308100 / 6332659870762850625                  	    3.2003655154095472
684008280009204381000 / 221643095476699771875               	    3.0860798011238333
26194878742247361184500 / 8200794532637891559375            	    3.1941879092319412
988797092817095519958000 / 319830986772877770815625         	    3.0916238066678385
41820004752592427401540500 / 13113070457687988603440625     	    3.1891847822775947
1745807922530722423852479000 / 563862029680583509947946875  	    3.0961615264636411
80816804632604843113153342500 / 25373791335626257947657609375	    3.1850504153525301
3696894652389922594527576660000 / 1192568192774434123539907640625	3.0999440323738066
```

(16 decimal points are printed for decimal approximations above.)

This exhibits a pattern seen with general
continued fractions, which is that they tend
to jump above and below the value they approximate,
depending on whether there are an even or odd
number of terms in the continued fraction
being included.


## Odd Squares, Threes, and Sixes

Another related continued fraction, this one for
$\pi$ and with a more predictable pattern,
is given by:

$$
\pi = 3 + \cfrac{1^2}{
                6 + \cfrac{3^2}{
                    6 + \cfrac{5^2}{
                        6 + \cfrac{7^2}{
                            6 + \cfrac{9^2}{
                                6 + \dots
                            }
                        }
                    }
                }
            }
$$

Implementing a computer program to evaluate
the convergents from the above patterns yields
even more Pi approximations:

```
                                Even More Pi
Convergent                                                          Approx 
--------------------------------------------------------------------------------
19 / 6                                                      	    3.1666666666666665
141 / 45                                                    	    3.1333333333333333
1321 / 420                                                  	    3.1452380952380952
14835 / 4725                                                	    3.1396825396825396
196011 / 62370                                              	    3.1427128427128426
2971101 / 945945                                            	    3.1408813408813407
50952465 / 16216200                                         	    3.1420718170718169
974212515 / 310134825                                       	    3.1412548236077646
20570537475 / 6547290750                                    	    3.1418396189294020
475113942765 / 151242416325                                 	    3.1414067184965018
11922290683065 / 3794809718700                              	    3.1417360992606653
322869019821075 / 102776096548125                           	    3.1414796890042549
9388645795842075 / 2988412653476250                         	    3.1416831892077552
291703390224616125 / 92854250304440625                      	    3.1415189855952756
9646071455650881825 / 3070380543400170000                   	    3.1416533941974261
338203386739761387075 / 107655217802968460625               	    3.1415419859977827
12533792135642378629875 / 3989575718580595893750            	    3.1416353566793886
489501901570061970946125 / 155815096120119939628125         	    3.1415563302845726
20095772843114788169975625 / 6396619735457555416312500      	    3.1416238066678388
865107029346752986828909875 / 275374479611447760672253125   	    3.1415657346585473
38971636325356476834702484875 / 12404964652972837218854831250	    3.1416160719181865
1833412715214285133654869268125 / 583597200719403932796125015625	3.1415721544829651
89918039850132576392201747480625 / 28621636626586418964957783375000	3.1416106990404735
```

## When to Use Simple Vs. General Continued Fractions

While general continued fractions are more flexible,
allowing a given rational or irrational number to be
expressed in a wider variety of ways, it is important
to point out how much faster the simple continued
fractions converge - with 15 terms, we arrive
at around 15 accurate decimal places, versus the 1-3
decimal places of accuracy from over 20 terms in the
above approximations.

Using the simple continued fraction representation of $\pi$,

$$
\pi = 3 + \cfrac{1}{
                7 + \cfrac{1}{
                    15 + \cfrac{1}{
                        1 + \cfrac{1}{
                            292 + \cfrac{1}{
                                1 + \dots
                            }
                        }
                    }
                }
            }
$$

and implementing it with a computer, we get the 
following table of convergents and their approximate 
values:


```
                               Pi Simple
Convergent                                                          Approx 
--------------------------------------------------------------------------------
22 / 7                                                      	3.1428571428571428
333 / 106                                                   	3.1415094339622640
355 / 113                                                   	3.1415929203539825
103993 / 33102                                              	3.1415926530119025
104348 / 33215                                              	3.1415926539214212
208341 / 66317                                              	3.1415926534674368
312689 / 99532                                              	3.1415926536189365
833719 / 265381                                             	3.1415926535810779
1146408 / 364913                                            	3.1415926535914038
4272943 / 1360120                                           	3.1415926535893890
5419351 / 1725033                                           	3.1415926535898153
80143857 / 25510582                                         	3.1415926535897927
165707065 / 52746197                                        	3.1415926535897936
```

## A Note on the Program

We implemented a program to convert terms in a continued fraction
representation (simple or general) into convergents (rational 
approximations).

We covered how to do this with Java in a previous blog post,
but this time we re-implemented it in Python and used some
basic object-oriented Python techniques and class decorators
(class methods, memoized functions, etc.)

You can find the code here: <https://git.charlesreid1.com/cs/python/src/branch/master/math/pi_continued_fraction_convergents.py>

We will return to the topic of continued fractions and cover 
general continued fractions (and importantly, the recurrence
relation used to convert them into convergents in the above
program) in a future blog post.


