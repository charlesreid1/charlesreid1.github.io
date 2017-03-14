---
title: Algorithm for Battery Capacity
date: 2015-03-10 20:53:59 -0700
status: draft
category: Personal
tags: programming, algorithms, math, science
---

From [this book](http://elementsofprogramminginterviews.com/sample/):

**A robot needs to travel along a path that includes several ascents and descents. When
it goes up, it uses its battery to power the motor and when it descends, it recovers
the energy which is stored in the battery. The battery recharging process is ideal:
on descending, every Joule of gravitational potential energy converts to a Joule of
electrical energy which is stored in the battery. The battery has a limited capacity
and once it reaches this capacity, the energy generated in descending is lost.**

**Design an algorithm that akes a sequence of n three-dimensional coordinates to be traversed,
and returns the minimum battery capacity needed to complete the journey. The robot begins
with the battery fully charged.**

Here is my thought process for designing this algorithm:

First, I broke the problem up into two parts: a single-step analysis, and a whole-journey analysis.

## Single Step Analysis

I began by writing my two (abstract) coordinates:

$$
(x_{i-1}, y_{i-1}, z_{i-1}) \\
(x_{i}, y_{i}, z_{i}) 
$$

from which I can get delta values,

$$
\Delta x = x_i - x_{i-1} \\
\Delta y = y_i - y_{i-1} \\
\Delta z = z_i - z_{i-1}
$$

I know that the x-y directions will be treated differently 
from the z direction, so I make a note to myself.

I also want some way to transform my spatial coordinates into energy coordinates.
(This also gives me an alternative way of thinking about the problem: 
I am mapping a physical space to an energy space.)

But I am transforming in two directions, or two "modes," corresponding to the two
cases for my robot battery: energy consumption, and energy generation.

My consumption conversion factor is my fuel efficiency, f:

$$
f = \dfrac{\text{distance}}{-\text{energy}} 
$$

I can also define my generation conversion factor, which is 
my battery recharge efficiency, g:

$$
g = \dfrac{+\text{energy}}{\text{distance}} 
$$

Since my robot's battery recharging capabilities are perfect,

$$
g = - \dfrac{1}{f}
$$

Next, I want a measure of the absolute distance that my robot travels.
I can use the distance formula:

$$
L = \sqrt{ x^2 + y^2 }
$$

or, for a single step,

$$
\Delta L = \sqrt{ \Delta x^2 + \Delta y^2 }
$$

Now I know my energy generation or consumption for a single step.
If I am going uphill, I am consuming energy:

$$
\Delta e = \frac{\Delta L}{f}
$$

and if I am going downhill, I am generating energy:

$$
\Delta e = g \Delta L = \frac{\Delta L}{-f}
$$

Now I have my (very rough) pseudocode for a single step:

```
f = 1
g = 1/f

if dz > 0:
    # consume energy
    de = -L/f
elif dz < 0:
    # generate energy
    de = L/f
```

## Whole Journey Analysis

Now we can assemble the single-step analysis to give us
the total $$\Delta e$$ incurred over a journey.

We still need to incorporate one more piece of information:
the battery can't be charged if it is full.
And to know if the battery is full after a given step,
we need to know the battery capacity.

But this is precisely the information we are trying to determine!
The problem is implicit.

Let me discuss two approaches to this problem.

The first is what I'll call the "puzzlemaster approach": 
this approach reduces the problem down to simple rules,
not necessarily realistic but acceptable for back-of-the-envelope
calculations. 

The second is a more rigorous approach, one that is 
flexible enough to deal with additional complicating factors.

## The Puzzlemaster Approach

In the context of a coding interview, which was the context of the given problem,
there is usually a single or a couple of clever shortcuts or assumptions you can make
to make the problem tractable in an interview-question-amount-of-time.

In this case, we have a clever solution: compute the energy change for each step,
then determine the minimum energy change (corresponding to the maximum ascent).

Our battery capacity should always be large enough to provide this.
If we use this quantity, the battery will always be 
big enough to store the largest possible charge, 
and have enough juice for 
the largest possible ascent.

We can think about the shortcut approach this way:
our robot is taking a path through physical space that maps to an energy space,
or putting it another way, a battery capacity space. This space does not map
exactly to physical space, because sometimes a rover's battery capacity
is full so it cannot charge. So battery capacity space is constrained
by an upper bound, when the battery is at 100%:

$$
e(x,y,z) = B
$$

and a lower bound, when the battery is at 0%:

$$
e(x,y,z) = 0
$$

The shortcut approach is to find the battery capacity that will shift the 
bounds of the constraint so high, that the energy function will never reach
B - that is, the battery will always be large enough that it will have 
more capacity and be able to continue charging, or have enough energy 
for the largest ascents. 

## The Weakness of the Puzzlemaster Approach

What does this approach sacrifice? By oversimplifying the problem, 
a back of the envelope solution was arrived at; but suppose new 
constraints are introduced. 

Suppose the efficiency of recharging decreases as a function of elevation. 

Or suppose the efficiency of recharging decreases with distance traveled. 

Or both.

Suppose engineers present you data about battery tests. How do you 
incorporate that information?

Suppose the efficiency is a function of the azimuthal angle 
of the robot's on-board gyroscope.

Are these things important? Yes! Overdesigning or underdesigning 
by using engineering approximations can incur significant costs
down the line. It's important to have a solid understanding of 
how to solve a single problem at a variety of different
levels of complexity.

## The Rigorous Approach

Let's talk a little more about a more rigorous approach.
As our problems get more complex and more constrained,
shortcut approaches won't be so obvious. 
Sometimes, in order to reach such shortcuts, we must 
introduce gross assumptions that we aren't comfortable with.
So its important to also think about a more fundamental approach.

The rigorous approach solves the implicit equation for battery size
using a simple iterative algorithm. 

The net energy consumption of the journey depends on whether the battery will charge,
and whether the battery will charge is a function of battery size.
This means that our battery capacity (which we're trying to find)
affects how much energy the journey takes.

Before beginning the rigorous approach, let's re-cast the problem.

First, we define the battery capacity B as the total amount of energy 
the battery can hold. Then the battery charge b is:

$$
b = \frac{e}{B}
$$

Our objective is to find the battery capacity B for a given journey, 
subject to the constraint:

$$
b > 0
$$

The non-linearity of the problem is introduced by the fact
that, by definition, b is a function of B. 

Here, we basically add two parts: one is an outer loop
to iterate on values of B, the other is a calculation of 
the battery charge b to enforce the condition b > 0.

Here's some very rough, Python-ish pseudocode:

```
# ####################
# Rigorous Approach

xyz = [...] # our set of points
B = 20 # initial guess
B_step = 1.0
f = 1
g = 1/f


converged = False
while not converged:
    b = 1.0
    for each delta:
        if dz > 0:
            de = -L/f
        elif dz < 0:
            de = L/f
        db = de/B
        b += db
        if b <= 0:
            # battery capacity too small - 
            # increment B and start over
            B += B_step
            break
```

We could make the selection of step size more sophisticated, 
as well as transform the problem into something more fit for 
a root-finding algorithm like the Newton-Raphson method. 
But this is just an interview question, after all.

Taking more practical considerations into concern, batteries can't always
be made in step sizes; we could also modify our algorithm to test a set 
of discrete battery sizes to see which ones work for a given journey.

If our efficiencies are a function of distance traveled, or the total elevation gained,
we can modify our algorithm to keep track of those quantities, and 
re-compute the efficiency for each leg of the journey.

## Addendum: The Azimuthal Angle

This very interesting problem can be tied in with on-board navigation systems
for robots. Robots process data from their sensors (like on-board gyroscopes) 
that give them feedback on the terrain ahead of them. As the robot continuously
gathers information, it is performing calculations to determine normal 
gradients and paths of minimum gradient.

However, robots don't think in terms of (x,y,z). They think in terms of 
distance, direction, and azimuthal angle. That is, they think in polar coordiantes,

$$
(r,\theta,\phi)
$$

We can re-cast the way we are doing our calculations into radial coordiantes 
using the relationships:

$$
x = r \cos \theta \sin \phi \\
y = r \sin \theta \sin \phi \\
z = r \cos \phi 
$$

and the inverse relationships:

$$
\phi = \arccos \frac{z}{\sqrt{x^2 + y^2 + z^2}} \\
\theta = \arctan \frac{y}{x} \\
r^2 = x^2 + y^2 + z^2 
$$

We can then use the value of $$\phi$$ to determine if the robot's battery
is recharging or consuming power. Because \phi is defined to be 0 
when pointing straight up, the robot's battery will charge if

$$
\frac{\pi}{2} \lt \phi \lt \frac{3\pi}{2}
$$

and the robot's battery will be consumed if 

$$
\phi \leq \frac{3\pi}{2}
$$

or

$$
\phi \leq \frac{\pi}{2}
$$

## Conclusion

While the authors of the problem may have realized the curveball 
that the non-linear dependence in this problem would create, 
it may also be that they inadvertently tried to make a simple
toy problem that ended up being a bit hairy.

In any case, taking a systematic mathematical approach 
like the one I illustrated here will always uncover such 
inter-dependencies, because it is a fundamental way of looking
at the problem.

By using this approach, I was able to take a simple toy problem
and re-cast it into multiple forms, with multiple ways of thinking about 
the problem, each offering its own insights. 


