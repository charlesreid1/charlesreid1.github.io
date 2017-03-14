---
title: Fair Tosses with Unfair Coins
date: 2015-03-24 20:35:16 -0700
category: Personal
tags: programming, algorithms, math, science
---

I came across the following puzzle while perusing code interview questions,
and upon digging deeper, found it was an excellent illustration of 
the kind of deeper thinking that can be brought to bear on such questions,
if only one stops looking for a "right answer."

The question is this:

**Given a biased coin (i.e., probability of heads != 50%), 
how would you use the coin to generate a random sequence 
of 0s and 1s (that is, to perform a sequence of fair tosses)?**

This question is a perfect illustration of my principle about 
the divergence of "traditional," discrete computer science thinking
and the more fundamental, mathematical way of thinking about problems
that comes from training in chemical engineering.

The two approaches are what we'll call the "puzzlemaster" approach,
which seeks a quick implementation of a clever solution,
and the "rigorous" approach, which clearly defines and generalizes
the problem, and allows us to classify the problem, 
search for solutions to similar problems, and 
tackle the problem in a much more powerful way.

## The Puzzlemaster Approach

The puzzlemaster approach seeks a quick implementation 
of a clever solution to solve an interview question.
Typically there is a repository of questions, each with 
"correct" or "best" answers, and interviewees study these questions
the same way a high school student studies SAT questions. 

Ultimately, the purpose of asking
an interviewee these questions is so that interviewers can see their 
thinking process, see how they arrive at the "correct" solution, 
and identify exceptional candidates.

In the case of the coin toss, the "right answer," or "most clever solution,"
actually originates with [John von Neumann](http://en.wikipedia.org/wiki/John_von_Neumann),
who published a 1951 paper entitled 
["Various techniques used in connection with random digits"](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&ved=0CCQQFjAA&url=https%3A%2F%2Fdornsifecms.usc.edu%2Fassets%2Fsites%2F520%2Fdocs%2FVonNeumann-ams12p36-38.pdf&ei=hvkQVYOKO4O3oQSthoHIDQ&usg=AFQjCNHb-1CDMWWXrtoH1g3NJZhJPtGhVw&sig2=4q0A1hp-k6uBkLshfSYXhw)
in which he discussed a method for generating
truly random variables from pseudo-random 
phenomena - bias in random numbers was an 
important problem with early computers.

Von Neumann's solution to the problem utilizes the fact 
that there are only two outcomes in a coin toss. 
He then reasons that the probability of flipping
heads, then tails, is the same as the probability
of flipping tails, then heads. That is,

$$
P(H) \times P(T) = P(T) \times P(H)
$$

This can be used to generate two outcomes 
of equal probability: heads-then-tails,
and tails-then-heads.

But what to do with heads-then-heads and 
tails-then-tails outcomes?

The probability of these events is not important - 
so we can throw out these results. All that matters 
is that the probability of heads-then-tails is equal to
tails-then-heads.

<img 
style="background: #aaa; padding: 20px;"
src="/img/CoinFlip.png">

As von Neumann notes, this increases the cost of 
generating random numbers by a factor of **at least** 2.

## The Breakdown of the Puzzlemaster Approach

The puzzlemaster approach has its weaknesses, though.

For example, von Neumann was focused on a particular 
application: random numbers for early computers. 
In this case, von Neumann **literally** needed 
random sequences of 0s and 1s. He wasn't concerned with 
recasting the problem in more general terms, or 
adding additional constraints. Had he done so,
had he pursued the problem further, he would likely
have abandoned the discrete, puzzlemaster-based approach
in favor of a probabilistic approach.

As an example of complexity that this approach can't handle:
What would happen if we were not using a biased coin but a loaded die, 
with independent probabilities for all 6 possible outcomes?
What if we had a 20-sided die?

What if, instead of having a biased generator of discrete 0s and 1s,
we had a biased generator of continuous values of random numbers
between 0 and 1? Or drawn from a Gaussian distribution?

The rigorous approach generalizes the problem 
that has been posed and re-casts it in a framework
that is capable of accounting for these additional 
compliations.

Thinking about a solution in terms of **distributions** is far more 
powerful than thinking about a solution in terms of **discrete states/outcomes**.

## The Rigorous Approach

A more general and more rigorous approach occurred to me almost 
immediately upon reading the problem statement. The solution 
was obvious because of a homework problem from a turbulence class
I took at the University of Utah, where we were learning about the
probability distribution of eddy sizes in turbulence.

The probability distribution of an eddy size in a turbulent flow
can be derived following [Pat McMurtry's turbulence lecture notes](http://www.eng.utah.edu/~mcmurtry/Turbulence/turblem.pdf),
(from whom I took the class), 
which concludes with the CDF of eddy size, that is, the probability
that an eddy will have a size $l \leq L$:

$$ 
F(l) = \int_{\eta}^{l} f(l) dl
$$

where $\eta$ is the Kolmogorov length scale, below which 
kinetic energy is dissipated by the fluid and turbulence 
ceases to have its effect. This becomes:

$$
F(l) = \dfrac{5}{3} \dfrac{1}{\eta^{-\frac{5}{3}} - L^{-\frac{5}{3}}} \int_{\eta}^{l} l^{-\frac{8}{3}} dl
$$

This distribution of eddy sizes leads to the turbulent
kinetic energy spectrum scaling of $-\frac{5}{3}$ that 
Kolmogorov famously showed.

Now, here's why this immediately jumped out at me when I 
read the problem: 

In order to implement a computational algorithm to simulate 
turbulent mixing, for one of the homework problems in the class,
we had to use a random number generator to sample the 
eddy size distribution and pick eddies of random sizes 
(needing to be random, but also needing to be distributed 
correctly!)

To do this, I started by generating a random number between
0 and 1. I would then map this domain (0 to 1) to the value
of the distribution domain (in this case, the minimum and maximum
eddy sizes, $\eta$ to $L$, respectively),
by going from the y-axis of the CDF to the x-axis of the CDF.
This gave me the value of a random variable distributed according to a 
prescribed distribution, obtained from a random variable distributed
uniformly between 0 and 1.

We can use the same principle in reverse to map one distribution
onto another - in this case, map a biased random process to an
unbiased random process.

Here's our solution: **use the cumulative distribution function
to map any distribution onto a uniform distribution over the domain
$[0,1]$.** 

We can then use this in reverse to generate uniform
random numbers from any given distribution (e.g., a skewed one).

## Applying to the Coin Problem

Applying this algorithm to our coin problem, 
we can visualize the CDF as a two-part step function.

The first step is the first outcome, heads,
with probability $p$. 

The second step is the second outcome, tails,
with probability $(1-p)$ and cumulative probability 1.

Now our algorithm to produce a random number 
from a biased coin flip is as follows:

* Flip a coin

* If heads, there are two possible cases: generate a 0, or generate a 1. Generating a 0 has probability $\frac{0.5}{p}$,
while generating a 1 has probability $\frac{p-0.5}{p}$. Pick a random number $z$ between 0 and 1; 
if $z \lt \frac{0.5}{p}$, return 0; else, return 1.

* If tails, generate a 1.

(If the probability of heads is lower than 50%, you can swap out heads for tails and the above explanation will hold.)

**But wait!** you exclaim. You are designing an algorithm to generate random numbers,
so how can you use a random number in your algorithm?

The answer is, I'm not implementing a random number generator. I don't need to! 
It has already been done before, by people far more qualified than I.

Rather, the algorithm we are designing is solving the more 
general case of mapping distributions onto one another.

## Why the Coin Problem is Clunky

Admittedly, our solution is a bit clunky when applied to the coin toss problem.
But that's because the coin toss problem uses a discrete distribution. 
The solution becomes much more elegant when we try to map one continuous distribution
onto another.

If we think of the CDF as giving us the quantiles of each value of our random variable,
we can see that the transformation works because the probability is bounded by the definition,

$$
\int_{-\infty}^{+\infty} P(x) dx = 1
$$

which means the cumulative probability
always ranges from 0 to 1 in uniform intervals
(quantiles).

## Applying to More Complex Problems

I threw together a short script to test out this principle 
by putting it into practice. The problem got really interesting 
really fast.

Let me start by walking through how the script is structured.

### The Weibull Distribution

To simulate a "biased" process, I simply used a Weibull distribution with $k=5$,
which is shown in green on the [Weibull distribution Wikipedia page](http://en.wikipedia.org/wiki/Weibull_distribution).
The Weibull distribution is centered at 1 but is skewed to the left. The distribution is given by:

$$
f(x) = k x^{k-1} \exp \left( -x^k \right)
$$

and the corresponding cumulative density function is given by:

$$
F(x) = 1 - \exp \left( -x^k \right)
$$

The intention was to map this skewed, non-normal, simulated-biased distribution 
onto the uniform domain $[0,1]$, and create a random process from it.

### The Empirical CDF

I begin by constructing an empirical CDF by picking a bunch of random samples
from the Weibull distribution. Fortunately, numpy has random number generators
for just about every distribution imaginable, so this is as simple as 
a call to numpy.

```python
from numpy.random import weibull

# generate a weibull distribution
k=5
z = weibull(k,(Nsamples,))
```

We can then compute the CDF with the following handy trick
(via [StackOverflow](http://stackoverflow.com/questions/3209362/how-to-plot-empirical-cdf-in-matplotlib-in-python)):

```python
Nsamples = 1000
Nsamples_new = 300

zsrt = np.sort(z)
cdf = np.arange(len(zsrt))/float(len(zsrt))
```

Why the two sample sizes?

The algorithm first generates an empirical CDF with 1,000 samples -
not necessary, strictly speaking, since we have an analytical expression
for the CDF for Weibull distributions - but the general case is for 
empirical distributions, and we want to make as few assumptions as possible.

It then generates a new sample of 300 points, which it then transforms
into the domain $[0,1]$ using the empirical CDF constructed above.

Now we can transform a value of z into a value of the CDF 
(which is just a uniformly-distributed random variable 
between 0 and 1) by running:

```python
normed = np.array([ cdf[find_nearest_index(zsrt,zz)] for zz in z])
newnormed = np.array([ cdf[find_nearest_index(zsrt,zz)] for zz in newz])
```

## The Output

I plotted up a couple of quantities to illutrate how this distribution 
transformation looks. First, I have the CDF on the left side, which 
visually shows the mapping of one domain (x) onto another (y).

The second column shows jitter plots of values of random numbers
taken from the Weibull distribution (top) and the corresponding
transformed values on $[0,1]$ (bottom).

Finally, the third column shows the PDF of the random samples,
and shows the transformation of the Weibull distribution 
(top) into a uniformly random distribution (bottom).

<img
src="/img/weibull.png">

## Analysis of Results

The above figure illustrates the two-step process involved in
transforming distributions for random processes. 

The first step is to use samples from the random process to 
construct an empirical CDF.

The second step is to use the empirical CDF to transform numbers 
from the domain of the original distribution to the domain $[0,1]$.

Notice from the blue-and-green jitter plot that the values drawn from the 
Weibull distribution have much wider scatter and more outliers than randomly-distributed
variables. But because we're using the CDF, which is naturally bounded between 0 and 1,
we don't have to worry about handling the outliers. 

From visual inspection of the red-purple jitter plot, it is clear 
that we are generating numbers that fully cover the domain $[0,1]$ 
in a random and uniform way. 

Also shown, on the right, are the distributions of the random variable
before (Weibull distribution) and after (random zero-to-one distribution)
the transformation to the domain $[0,1]$. While there is some noise in the uniform 
distribution, this could be adjusted with a wider bandwidth or 
a larger number of samples.

## Conclusions

It isn't often that you get the chance to revisit classic problems in old 
scientific papers, and it is even more rare to get the chance to expand on the
results from those papers to generalize a procedure or approach to work for
more complicated circumstances. 

Fortunately, when John von Neumann tackled this problem, he stopped at the
special case of a discrete distribution (coin toss), rather than continuing
to develop the more general case. 

And that, folks, is how you expand your thinking outside the "toy problem" box.

## Appendix: The Full Code

Included below is the full code that was used to generate the above plot.

```python
import numpy as np
import seaborn as sns
import matplotlib.pylab as plt
from numpy.random import weibull
from scipy.stats import cumfreq


Nsamples = 1000
Nsamples_new = 300


# generate a weibull distribution
k=5
z = weibull(k,(Nsamples,))


# useful function
def find_nearest_index(vec,val):
    ix = (np.abs(vec-val)).argmin()
    return ix


# nice trick for getting the empirical cdf:
# http://stackoverflow.com/questions/3209362/how-to-plot-empirical-cdf-in-matplotlib-in-python
zsrt = np.sort(z)
cdf = np.arange(len(zsrt))/float(len(zsrt))

normed = np.array([ cdf[find_nearest_index(zsrt,zz)] for zz in z])


# use the empirical distribution to transform
# from weibull domain into [0,1] domain
newz = weibull(k,(Nsamples_new,))

newnormed = np.array([ cdf[find_nearest_index(zsrt,zz)] for zz in newz])



f = plt.figure(figsize=(10,6))
ax1 = f.add_subplot(1,3,1)
ax2 = f.add_subplot(2,3,2)
ax3 = f.add_subplot(2,3,5)

ax4 = f.add_subplot(2,3,3)
ax5 = f.add_subplot(2,3,6)

with sns.color_palette("Set1"):

    # cdf
    sns.kdeplot(z, cumulative=True, ax=ax1)
    ax1.plot(zsrt,cdf)

    # scatter plot of weibull distributions
    sns.regplot(np.arange(len(z)),z, ax=ax2, fit_reg=True)
    sns.regplot(np.arange(len(newz))+len(z),newz, ax=ax2, fit_reg=True)
    ax2.set_xlim([0,len(newz)+len(z)])

    # scatter plot of uniform [0,1] distributions
    sns.regplot(np.arange(len(normed)),normed, ax=ax3, fit_reg=True)
    sns.regplot(np.arange(len(newnormed))+len(normed),newnormed, ax=ax3, fit_reg=True)
    ax3.set_xlim([0,len(normed)+len(newnormed)])

    # kde
    bw = 0.1
    sns.kdeplot(z,    bw=bw, lw=1.8, shade=True, ax=ax4)
    sns.kdeplot(newz, bw=bw, lw=1.8, shade=True, ax=ax4)
    ax4.set_xlim([min(min(z),min(newz)),
                  max(max(z),max(newz))])

    # kde
    bw = 10.0/Nsamples
    bwnew = 10.0/Nsamples_new
    sns.kdeplot(normed,    bw=bw,    shade=True, ax=ax5)
    sns.kdeplot(newnormed, bw=bwnew, shade=True, ax=ax5)
    ax5.set_xlim([min(min(normed),min(newnormed)),
                  max(max(normed),max(newnormed))])


plt.draw()
plt.show()

```







