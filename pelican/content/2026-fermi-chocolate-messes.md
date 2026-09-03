Title: Fermi Problems Are Chocolate Messes All the Way Down
Date: 2026-09-03 13:00
Category: Mathematics
Tags: mathematics, fermi problems, chocolate

Status: draft

In a prior post [Fermi Problems are Quadrature Problems]({filename}2026-fermi-quadrature.md) 
we worked through
the classic Fermi problem *"how many chocolate bars are eaten each year in
the United States?"* twice - once as a naive one-point estimate (~40 billion
bars/year) and once as a refined 4×4 age-by-season quadrature that preserved
the age/season interaction (~44 billion bars/year). Both estimates hovered
in the same order of magnitude, which was satisfying but also unfalsified:
we worked from first principles and back-of-the-envelope estimates.
No published, macroeconomic data from the real world went into the estimates.

This post is the falsifiability check. It turned into a blog post because it
turned out to be much more interesting than "look up two or three published
numbers and back out the real answer" because "real" is hard to pin down, there
isn't actually an "answer," and the rabbit hole keeps going deeper, because
building out bounds for the original Fermi problem is itself a Fermi problem.
And the numbers that go into those Fermi problems pack in many assumptions that
can themselves be unpacked into Fermi problems.

It's Fermi problems all the way down.

## The Aggregator Trap

The obvious first move is to do a web search for "how much chocolate do Americans eat
per year" and take the top result. Do that (like a rube) and you get some variation of
these two claims, repeated across dozens of sites:

1. **Americans eat 2.8 billion pounds of chocolate per year (~11 lb/person).**
2. **The average American eats about 3 chocolate bars per week.**

Both numbers convert cleanly into "bars per year." Claim 1, at a standard
1.55 oz Hershey's bar (~10 bars/lb), gives 28 billion bars/year. Claim 2,
over 52 weeks × 340M people, gives 53 billion bars/year. That would be a
tidy [28B, 53B] corridor that both of our estimates sit inside. Post over.
Ship it. Except that **it is total bullsh-t**.

Sites using this claim are a giant Gordian knot of self-referential listicle
sites, paid aggregators, and misspelled/garbage URLs grifting as "legitimate"
sources.

Quality score: 1/10.

## The Actual Primaries

Two sources survive scrutiny:

**USDA Economic Research Service** publishes cocoa bean import volumes as
part of its agricultural trade tracking. Between 2000 and 2022, the US
imported an average of **~425,000 metric tons of cocoa beans per year**.
(2023 and 2024 were unusual crop-failure years and dropped to 269kt and
198kt respectively; we'll use the long-run average since the recent dip is
a supply shock, not a demand signal.) This is a real customs-derived
number with a known methodology.

(Side note: reporing an average consumption per year over TWENTY YEARS
reeks of Fermi sub-problems.)

**National Confectioners Association's State of Treating 2025/2026 report**,
compiled using Circana retail-panel data and Euromonitor market modeling,
reports **US chocolate sales of $28.4 billion in 2025** (51.7% of the $55B
total confectionery market). This is a real industry number with named
data providers.

To turn either one into "bars per year," we have to introduce multiple layers
of estimates (models). Which is to say, we have to do a Fermi problem.

## Lower-Bound Fermi Problem: Cocoa Tonnage to Bars

Starting from 425,000 metric tons/year of imported cocoa beans, the chain
of unit conversions goes something like:

1. **Bean → cocoa mass.** After shell removal, roasting, and winnowing,
   yield is roughly 80% of raw bean mass. ~340,000 t of usable cocoa
   mass.
2. **Cocoa mass → finished chocolate.** Finished chocolate is a *blend*.
   Milk chocolate is ~10–20% cocoa content by mass; dark is 50–85%; white
   is 0% solids. Weighted by US market mix (heavily milk), call the
   average cocoa content ~20% → 340,000 / 0.20 → **1.7 million metric
   tons of finished chocolate** → 3.75 billion pounds.
3. **Non-bar uses.** Some cocoa becomes baking cocoa, hot chocolate mix,
   cosmetic cocoa butter, ice cream inclusions - not bars. Call it 15–25%
   of cocoa mass. Subtract ~20%.
4. **Net trade in finished chocolate.** The US is a net importer of
   finished chocolate (Toblerone, Lindt, Cadbury via Canada, etc.), which
   adds back roughly the same order of magnitude as the non-bar leakage.
   Call these a wash to first order.
5. **Pounds → bars.** At 1.55 oz/bar → 10.3 bars/lb → 3.75 × 10e9 lb × 10.3 → **~39 billion bars/year**.

That five-step decomposition had at least a factor-of-two uncertainty at each step.
Bean yield could be 75% or 85%. Average cocoa content could be 15% or 25%.
Non-bar share could be 10% or 30%. Every arrow in that chain is a Fermi
sub-problem, and every one of its inputs is a number *someone else*
estimated by decomposing *their* problem into pieces they could each guess
within a factor of two.

If we swing the knobs pessimistically, we land at ~25B bars. Optimistically,
~55B. **The "lower bound from real primary data" is a range of ~25–55B**,
which is not really a bound at all - it's a Fermi estimate wearing a
lab coat.

## Upper-Bound Fermi Problem: Dollar Sales → Bars

Starting from $28.4B/year in US chocolate sales, the chain is shorter but
each step is fuzzier:

1. **Dollar sales → bar-equivalents.** We need an average retail price per
   "bar." Full-size checkout bar: ~$1.50–$2.00. Premium bar (Lindt,
   Ghirardelli): $3–$5. Fun-size piece from a Halloween bag: ~$0.15–$0.30.
   Bulk seasonal chocolate (Easter eggs, Valentine's boxes, advent
   calendars): wildly varying $/oz, but each *piece* often counts as an
   eating event.
2. **Weighted average.** If bar-form full-size chocolate dominates sales
   dollars, the average is close to $1.50/bar. If fun-size and bulk
   dominate the *count*, the average is closer to $0.50/piece.

That's not a factor of two; it's a factor of three, and the whole answer
sits on it:

| Average $/bar | Implied bars/year |
|---------------|-------------------|
| $0.50         | ~57 billion       |
| $1.00         | ~28 billion       |
| $1.50         | ~19 billion       |

**The "upper bound from real primary data" is anywhere from 19B to 57B**,
depending entirely on how we resolve one knob - which is itself the same
"what counts as a bar" linguistic knob we called out in the very first
section of the prior post. Primary data didn't retire the knob. It just
relocated it into the unit-conversion step.

## Fermi Problems All the Way Down

Here's the pattern. We started with a Fermi problem (bars/year). To
bound it, we went hunting for real data. The real data we found isn't
denominated in the units we want, so converting it into bars/year required
building another Fermi problem - a decomposition into estimated factors
each guessed to within a factor of two. And when we look at where those
factors come from, they are the outputs of other Fermi problems that
somebody else already solved:

- USDA's 425,000 metric tons of cocoa imports is itself the output of a
  chain: customs declarations aggregated across ports, unit conversions,
  imputations for missing data, seasonal adjustments. USDA analysts did
  their own Fermi decomposition to produce that number; we just don't see
  the pieces.
- NCA's $28.4B in chocolate sales is Circana's retail-panel extrapolation
  (some measured stores × a scaling factor for coverage) blended with
  Euromonitor's channel-mix model. Both of those are big decomposition
  chains ending in a single reported number.

There is no bedrock number that lives outside a Fermi decomposition.
Every "primary" figure is the leaf node where someone earlier in the chain
decided to stop decomposing and report a total. Push on any leaf hard
enough and you find yet another decomposition underneath.

And the decomposition doesn't just go *deeper*; it goes *sideways* into
whole other disciplines. Take the "$/bar" knob from the upper-bound
problem. We handwaved it as $0.50 to $1.50 depending on whether fun-size
or full-size dominates. But the honest way to attack that knob is to
estimate **the joint distribution of chocolate bar types across the US
market** - Hershey's checkout bars vs. Costco Toblerones vs. Halloween
fun-size vs. seasonal boxed chocolates vs. premium Lindt vs. bulk baking
chocolate - and that is an entirely different subclass of Fermi problem.
It lives in economics and finance, not in demography. It asks:

- Which manufacturers dominate US chocolate volume? (Hershey, Mars,
  Ferrero, Mondelez, Lindt, Nestlé, Ghirardelli, and a long tail.)
- What is each manufacturer's product mix, and what fraction of their US
  revenue is bar-form vs. boxed vs. seasonal vs. inclusions?
- What are their per-unit margins, wholesale prices, and retail markups?
- What's the channel distribution - grocery vs. drug vs. mass vs. club vs.
  convenience vs. specialty - and how does the price-per-bar-equivalent
  vary across those channels?

Each of those questions is *itself* a Fermi problem, and now the primary
data isn't customs tonnage or retail-panel dollar totals - it's public
companies' **10-K filings, segment reporting, investor decks, and gross
margin disclosures**, and you're reverse-engineering unit economics out
of consolidated financial statements that were never designed to answer
"how many bars." Hershey's 10-K tells you global net sales for the "North
America Confectionery" segment, but not how many kilograms it shipped,
and definitely not how many *bars*; you have to estimate the mapping
using industry-average margin data, competitor benchmarks, and public
price-per-unit surveys - each of which is another Fermi sub-problem
several layers down.

So the recursion isn't a single tree of decompositions; it's a *forest*.
Different branches recruit different fields - demography for the
population count, agronomy for cocoa yield, industrial chemistry for
processing losses, corporate finance for the manufacturer-and-margin
map. Each field has its own conventions for what counts as a "primary"
number and where the field stops decomposing. Cross-field, those
conventions don't line up, so when you try to reconcile a demographic
estimate with a financial one you're not just multiplying uncertainties -
you're translating between whole vocabularies of what "measured" means.

Which means our two bounds - the ~25–55B range from cocoa tonnage and the
~19–57B range from dollar sales - are not really bracketing the truth so
much as recording where two different chains of Fermi decompositions
happened to land. Union those ranges and we get roughly [19B, 57B], which
comfortably contains our two original estimates (40B and 44B). But we
should be honest about what that means: it doesn't mean the original
estimates were validated. It means every path we can take to an answer
inherits the same factor-of-two-per-knob budget, and those knobs *compose
multiplicatively*, so a five-step chain of factor-of-two knobs has a
factor-of-32 total spread even if every individual knob is honest.

The interesting thing isn't that our Fermi estimate landed in the middle
of the corridor. The interesting thing is that **the corridor is the same
width as the original problem**. We didn't tighten the answer by bringing
in real data. We just relocated the uncertainty from "what's the
per-capita rate?" into "what fraction of cocoa becomes bars?" and "what's
the average price per bar?"

## The Fractal Coastline

In a prior post [Fermi Problems are Quadrature Problems]({filename}2026-fermi-quadrature.md) 
took a one-sentence bar-trivia question and pulled on the
thread until it turned into the population balance equation - the same
formalism used to track particles in a turbulent jet, or precipitation of
ice particles in the atmosphere contributing to cloud seeding and growth -
but applied to Halloween candy and demographic distributions.

This post pulls on the *next* thread. The moment you try to bound the
answer against reality, the "reality" you were reaching for turns out to
be another Fermi problem, and each of *its* inputs is another Fermi
problem, and the branches recruit different fields - demography,
agronomy, industrial chemistry, corporate finance - each of which
terminates its own decomposition at whatever level of aggregation
happened to be convenient for its own purposes. There is no floor. The
"primary data" you were hoping to stand on is a platform someone else
built by decomposing *their* problem far enough to feel done, and if you
step on it and push, it decomposes further.

This is not a bug in Fermi estimation. It's a feature of *the world*.
Reality is a fractal coastline: the closer you look, the more structure
appears, and the total "length" you measure depends entirely on the size
of the ruler you brought. Every time we ask "how much chocolate?" we're
really asking "at what altitude?" A satellite photo says one thing; a
customs manifest says another; a Hershey 10-K says a third; a grocery
store receipt says a fourth; a five-year-old's Halloween pillowcase says
a fifth. None of them are wrong. They are measurements at different
scales, and the scales don't compose into a single tidy total because
the coastline doesn't have a single tidy length.

What the Fermi decomposition buys us is not a *number*. It's a *map of
the coastline at the altitude we chose to fly at*, with every landmark
labeled: here is where we assumed a population, here is where we assumed
a rate, here is where we assumed a cocoa content, here is where we
assumed a price per bar. Every landmark is a place we could descend and
zoom in further, and the map tells us exactly what we would gain (and
lose) by doing so. That's not a consolation prize for failing to find
the "real" answer. That *is* the real answer, at the altitude the
question was asked.

The aggregator's confident 2.8 billion pounds is a photograph of the
coastline with no scale bar. Our 40 billion bars is a photograph with
the scale bar drawn on it, plus a legend explaining what every marking
means and how the picture would change if you flew lower. The picture
isn't sharper - it's actually a little fuzzier, because we've been
honest about the fuzz - but for the first time it's a picture you can
navigate by.

And that's the whole thing. We aren't strolling along on solid ground
counting Snickers wrappers. We're traversing a fractal coastline, one
moment in time at a time, with a map we drew ourselves, at whatever
altitude we chose.

It is a chocolate mess. But it is a beautiful chocolate mess.

## References

- USDA Economic Research Service, [High cocoa prices on smaller global crops lead to decreased U.S. imports in 2023 and 2024](https://www.ers.usda.gov/data-products/charts-of-note/chart-detail?chartId=110921).
- USDA Economic Research Service, [Food Availability (Per Capita) Data System](https://www.ers.usda.gov/data-products/food-availability-per-capita-data-system/).
- National Confectioners Association, [State of Treating 2025](https://candyusa.com/state-of-treating-2025/).
- National Confectioners Association, [Confectionery Sales Climb to $55 Billion in 2025](https://candyusa.com/news/confectionery-sales-climb-to-55-billion-in-2025/).
- Prior post: [Fermi Problems Are Quadrature Problems]({filename}2026-fermi-quadrature.md).
