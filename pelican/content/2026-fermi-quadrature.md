Title: Fermi Problems Are Quadrature Problems
Date: 2026-09-03 12:00
Category: Mathematics
Tags: mathematics, fermi problems, quadrature, numerical methods, chocolate

Here's a Fermi problem you'll run into sooner or later, usually in a job
interview, sometimes over drinks with someone who wants to see how you think:

> How many chocolate bars are eaten each year in the United States?

The provenance goes back to Enrico Fermi's Chicago physics classes, where he'd
ask students to estimate the number of piano tuners in the city, or the width
of a nail's head in miles, or anything else where the point wasn't the number
but the *decomposition*. That habit of mind has since been laundered through
McKinsey and Google into the standard interview format, but the underlying
move is Fermi's: break a hard question into smaller questions you can each
guess within a factor of two, and let the errors mostly cancel.

## Does Size Matter?

Before we start estimating, there's an elephant in the room that deserves to
be named and then, deliberately, ignored. What counts as "a chocolate bar"?
A fun-size Snickers you get in a Halloween bucket? A king-size Twix? A
square of a Hershey's bar? A Costco-sized Toblerone? The answer changes the
final count by an arbitrary factor of 1/2 or 2 or worse - it's the single
variable this whole problem is most sensitive to, and it's not really a
quantitative question at all. It's a *linguistic* knob. Turning it doesn't
teach us anything about populations or quadrature; it just relabels what
we're counting.

So we're going to do what physicists do when a problem has a knob like this:
we're going to assume a spherical cow. In the spirit of Fermi, "eating a
chocolate bar" is an idealized, dimensionless *event* - a discrete unit of
chocolate consumption, roughly the size of whatever the reader pictures when
they hear the phrase. We're not going to quibble about grams or servings or
whether a Reese's cup counts. If your definition differs from mine by a
factor of two, your final answer differs from mine by a factor of two, and
that's fine. The interesting structure of this problem lives in the
population and its interactions, not in the definition of the counting unit,
and the machinery we're about to build works the same way whichever
definition you pick.

With that noted and set aside, on to the actual estimation.

## The Naive Approach and What It's Secretly Assuming

The textbook approach to the chocolate question looks like this. Guess that
the average American eats maybe one chocolate bar every few days - call it
0.3 per day. Multiply by the population, roughly 340 million. Multiply by
365. You get something on the order of **40 billion chocolate bars per year**. 

That's your answer, and if you've picked reasonable numbers it's probably 
within a factor of two or three of the truth.

But look at what that multiplication is quietly assuming: one average
American, one average day, one average rate. Every source of variation in the
real population has been smoothed into a single number. If you push on the
estimate, the assumption starts to feel thin. A five-year-old on Halloween is
not eating the same amount of chocolate as an fifty-year-old on Halloween.
Neither of them is eating the same amount on Halloween as they are in March.
And it gets worse when you notice that the *seasonal spike itself depends on
who you are*: kids own Halloween, adults own Valentine's Day, families with
young children own Easter. (We can pretty safely assume that seniors will be
flat across all of it.)

You can try to refine the estimate by splitting into age buckets, or by
splitting into seasonal buckets. Either helps a little. But do them
separately and you still miss the thing that actually matters, which is that
age and season interact. A "seasonal multiplier" averaged over the whole
population says everyone eats three times more chocolate on Halloween. That's
false in a specific and important way: kids eat ten times more, adults eat
only slightly more, and the average is a fiction that lives in neither group.

The interaction is real, and no amount of separately-refined marginal
averages will recover it. We need a formalism that lets us write the joint
structure down directly.

## Population as a Joint Density (or, A Little Quadrature Never Hurt Anyone)

Here's the reframe. Think of the population as a *density* over some space of
coordinates. Each person has internal coordinates $\xi$ - age, income, dietary
preferences, whatever matters for the problem - and lives in the external
coordinate of time $t$. Let $n(\xi, t)$ be the number density of people:
$n(\xi, t)\, d\xi$ is how many people have coordinates in a little box around
$\xi$ at time $t$. Let $r(\xi, t)$ be the per-capita consumption rate:
chocolate bars per person per unit time, for a person with coordinates $\xi$
at time $t$.

Then the total number of chocolate bars eaten in a year is just the integral
of the product:

$$
\text{CBE} = \int_0^{1\,\text{yr}} \int_\xi r(\xi, t) \, n(\xi, t) \, d\xi \, dt
$$

Two objects, cleanly separated. $n$ says who exists. $r$ says what they do.
The product $r \cdot n$ is chocolate bars per unit coordinate per unit time,
and integrating it over the whole domain gives the total. (This is the
[population balance
equation](https://en.wikipedia.org/wiki/Population_balance_equation), a
workhorse in chemical engineering, particle dynamics, and demography.
We're borrowing the machinery, not reinventing it.)

Now the key observation: any numerical evaluation of that integral is a
*quadrature*. Pick a grid of abscissae $(\xi_i, t_j)$, assign each grid cell
a weight $w_{ij}$ (in the simplest case, just the cell's width), and sum:

$$
\text{CBE} \approx \sum_{i,j} w_{ij} \, r(\xi_i, t_j) \, n(\xi_i, t_j)
$$

That's the whole game. The naive Fermi estimate we started with -
rate × population × 365 - is exactly this sum with a single term: one
$\xi$-bin covering everyone, one $t$-bin covering the whole year, one
average rate. It's a one-point quadrature over the joint density.
*Refining a Fermi estimate is refining a quadrature grid.* Everything from
the back-of-envelope guess up to a full numerical integration lives on the
same continuum.

And crucially, this formulation does not require $r$ to factor as an
age-dependent piece times a seasonal piece. You fill in each grid cell
independently, so any interaction between coordinates is preserved by
construction. That's exactly the structure the marginal-average approach
destroys.

There's one more idea worth borrowing from numerical analysis here. The
whole art of Gaussian quadrature is that abscissae should not be evenly
spaced - they should cluster where the integrand varies fastest. The same
instinct applies to Fermi estimation: **a good quadrature grid matches the
shape of what you're integrating, not the shape of the axis you're
integrating over.** For the chocolate problem, the "time" axis has twelve
months, but the *integrand* has three spikes: Halloween, Valentine's,
Easter. Using twelve evenly-spaced monthly bins would spend most of your
resolution on quiet months where the integrand is flat and boring.
Concentrating your grid on the three candy-heavy windows plus one bin for
"everything else" captures almost all the structure with a quarter of the
work. That reduction - twelve bins to four - is not a shortcut; it's the
correct grid for this integrand.

There's a subtlety worth naming here, though. When we collapse twelve
evenly-spaced months into four unevenly-sized "seasons," we're doing
something a little sneaky: we're letting the *content* of the year (which
holiday, which age group's spike) reshape the time axis itself. What
was a pure **external dimension** - clock time, marching uniformly forward -
is being warped into an **internal dimension** that carries information about 
the integrand. That works cleanly here because there's no other process on 
the time axis we care about. As problems gain dimensions, though, that 
alignment can break. 

(As a more involved example, if we were trying to approximate number of chocolate
bars eaten by a population, but under conditions of continuous changes in population
or demographics, then integrating the total population over time would
need a properly-resolved time axis - lumping 46 weeks into one bin would
be throwing away real information. The seasonal grid works for our problem,
because the integrand's structure and external axis's structure happen to
coincide. If they don't, keep them separate, and "pay" for the extra abscissas
(with a bit more bookkeeping).

## Working the Chocolate Problem With Interactions

With the framework in hand, the estimate becomes a table. Rows are age
buckets, columns are seasonal windows, each cell holds the number of bars
eaten by that group in that window.

For the age axis, four buckets are enough: kids (0-12), teens (13-19),
adults (20-64), and seniors (65+). Population is roughly uniform over
these bands, so with 340 million Americans we can allocate roughly 55M
kids, 30M teens, 190M adults, and 65M seniors. (Uniform-in-age is a lie,
but a small enough one that the drama of this problem lives in $r$, not
in $n$. That itself is a useful diagnostic - it tells us where refining
would and wouldn't help.)

For the time axis, four bins: a Halloween window (~2 weeks around Oct 31),
a Valentine's window (~2 weeks around Feb 14), an Easter window (~2 weeks
around the spring holiday), and the remaining ~46 weeks of the year lumped
into "rest of year." Numbers below are bars per person per day, and we'll
multiply through by bucket population and bin length at the end.

|              | Halloween (14d) | Valentine's (14d) | Easter (14d) | Rest (312d) |
|--------------|-----------------|--------------------|--------------|-------------|
| Kids (55M)   | 3.0             | 0.4                | 1.5          | 0.3         |
| Teens (30M)  | 2.0             | 0.6                | 0.4          | 0.4         |
| Adults (190M)| 0.5             | 1.5                | 0.3          | 0.25        |
| Seniors (65M)| 0.2             | 0.3                | 0.2          | 0.15        |

Look at that matrix for a second. The kids row peaks on Halloween. The
adults row peaks on Valentine's. Easter has a bump for kids and almost
nothing for anyone else. Seniors are flat and low. **No product of a
row-vector and a column-vector produces this pattern** - the matrix is not
rank-1, and any factorization $r(\xi, t) = r_{\text{age}}(\xi) \cdot s(t)$
would flatten these ridges into a smooth surface that gets every cell
wrong. This is precisely the structure the joint formulation preserves and
the marginal-refinement approach loses.

Summing (population × rate × days) cell by cell:

$$
\text{CBE} \approx \sum_{i,j} n_i \cdot r_{ij} \cdot w_j \approx 44 \text{ billion bars/year}
$$

Which is, satisfyingly, in the same order of magnitude as the naive
estimate from the first section (40 billion for the naive approach, 44 billion
for the quadrature estimate). That's the usual outcome, and it's not a
knock on the framework - it's a reminder that averaging over correlated
variables often lands close to the truth by luck. What the framework buys
you isn't necessarily a better number; it's a *legible* number. Every
approximation is named and located in a specific cell. If you wanted to
sharpen the estimate, you'd know exactly where to add resolution - split
Halloween into "trick-or-treat night" and "the week after," split kids
into "young enough to trick-or-treat" and "too cool for it" - and you'd be
adding grid points to the ridges, which is exactly what a higher-order
quadrature scheme does automatically.

That's the transferable idea, and it generalizes beyond chocolate.
Any Fermi problem about a population - how many haircuts per year, how
many gallons of coffee consumed per week, how many miles driven per day -
is an integral of a per-capita rate against a number density over some
joint coordinate space. The reason the standard "multiply the averages"
trick works at all is that most people's mental $r$ is smooth enough that
a one-point quadrature suffices. When it isn't - when the coordinates
interact, when the ridges matter - the framework tells you exactly where
to add resolution and why. You stop guessing a single average and start
choosing a grid.

## References

- Wikipedia, [Population balance equation](https://en.wikipedia.org/wiki/Population_balance_equation).
- Wikipedia, [Fermi problem](https://en.wikipedia.org/wiki/Fermi_problem).
- Wikipedia, [Gaussian quadrature](https://en.wikipedia.org/wiki/Gaussian_quadrature).
