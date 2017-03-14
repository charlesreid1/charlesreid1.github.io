---
title: Arduino for Visual Thinkers - Hello World!
date: 2015-06-10 20:53:59 -0700
status: draft
category: InternetOfThings
tags: programming, visual, arduino, arduino nano, microcontrollers, science, electricity
---

This tutorial gives a rundown of a simple "Hello World" circuit with Arduino,
presented in a way that caters to visual thinkers.

<img
width="500px" 
alt="Arduino Hello World"
src="/img/arduino20150610/photo_HelloWorld.jpg">

Before we dive into our Arduino hello world circuit, let's talk about power lines.

We all know power lines are dangerous. Working on power lines requires special equipment,
and downed power lines pose an electrocution hazard. But what is it that makes those power lines
so dangerous? 

Voltage is what makes them dangerous. But why? Voltage is dangerous because it's a form of energy.

# Voltage is Electrical Potential

## Potential Energy

Voltage is electrical potential energy. There are other forms of potential energy, too.
Mechanical devices (like springs) can store mechanical potential energy (by winding the spring).
Systems can also store chemical potential energy, like a barrel full of gasoline, or 
gravitational potential energy, like a piano perched precariously on a tenth floor balcony. 
What each of these tyeps of potential have in common is, they are storing energy. 
The energy has to come from somewhere - the spring must be coiled, the piano 
must be hauled up ten flights of stairs, and fossil fuels must be formed with geologic forces.
Electrical potential energy is no different. The energy must be generated by a battery,
a generator, or a power plant. 

In all of these systems, energy is generated in one form, then captured and converted to 
another form for storage. The stored energy can then be released - by letting go of the spring,
by pushing the piano off the balcony, by dropping a match into the barrel of gasoline - 
and it will be converted to yet another form of energy.

So, what makes voltage so dangerous? The same thing that makes a large coiled spring,
a large piano hoisted high up, or a barrel of gasoline dangerous: the *potential* that 
the the stored energy could release itself all at once, injuring or killing people. 

## Creating a Visual Analogy: Voltage and Flow 

One of the problems with electrical potential is that it is an abstract concept.
Most people haven't developed an intuition for how to think about electricity.
So we want to create a visual analogy for voltage, to serve as an inutition pump
and give us some basic tools for thinking about circuits visually.

To visualize flow of electrons, we can think about the flow of water in a system 
of pipes. The water represents the electrons, with the flow of water through pipes
like the flow of electrons through wires. Like electrons, water can be controlled,
channeled, diverted, and stored for use later. 

If we put a valve into our pipe system, and we open the valve, water will spill out
with a certain amount of energy. If we have a "high voltage" fluid circuit, i.e.,
a fluid circuit that is at a high elevation, the water will come out with more energy
than if we have a "low voltage" fluid circuit, at a low elevation.

When we open a valve in our pipe system, water will immediately seek lower ground.
In the same way, when we "open the valve" on our electric circuit, the electrons
will immediately seek "lower" ground, in the form of something neutrally charged.

This is the concept of "ground." Just like all water flows to the sea, 
all electrons flow toward ground. Think of it as a giant sea, with an infinite
capacity for electrons, whose charge is always neutral, and whose potential 
never changes.

In fact, in hydraulics the term for the amount of potential available is 
"pressure head." A pipe of water raised 10 feet off the ground is said to 
have "10 feet of head."

# The Hello World Circuit

Now that we've covered voltage in general terms, let's talk about how voltage works 
in the context of our Arduino "Hello World" circuit.

## The LED

Our Hello World circuit will be extremely simple. We will connect a single component,
a small light-emitting diode (LED), a.k.a. a little blinky light, to our Arduino,
and use voltage from the Arduino board to activate the LED.

Let's return to our pipe flow analogy. What we're doing is using the flow of electrons
to create a "Hello World" component, in the form of a light that we can see.
This is like using the flow of water from a higher elevation out of a valve 
to move a water wheel. 

As the elevation of our water circuit increases, there is more energy available 
to turn the water wheel. The water wheel will turn faster with higher voltages.
But at some point, voltage can simply be too high, forcing the water wheel to 
turn faster than it was made to, and breaking it.

## Changing Voltages

The Arduino has a fixed voltage on board: 5 volts. This keeps the circuitry simple,
but it also presents us with a problem: we may not want 5 volts. We may add a component 
to our circuit that can only handle 1 or 2 volts - 5 volts would be too much energy 
and could fry our component. So we also need to think about how to modify the voltages.

Let's explore the fluid flow analogy a bit. We can't change the elevation of our 
water circuit - that's a given, just like the available voltage on the Arduino.
But we can add an extra segment of pipe before our valve, one that drops the valve down
to a lower elevation and puts a bend in the pipe before it gets to the valve.

```
(High Head/Voltage) ------------+------------
                                |
                                |
                                |
                                |
                                |
(Low Head/Voltage)              +---(Valve)
                                       .
                                       .
                                       .
                                       .
(Ground)                               .
```

By lowering the valve, we have lowered the amount of head available at the valve
when we open it. Also note that the energy we spent raising the water to its original
elevation is wasted when we lower the potential.


## The Resistors

We can use resistors as components in any circuit to reduce the voltage before we 
run electrons through other components. 
Just as adding a segment of pipe before our valve in our water circuit lets bleed off
some gravitational potential energy, adding resistors before our LED lets us 
bleed off some electrical potential energy, lowering the voltage drop
across our LED component.

A small resistor would reduce the voltage slightly:

```
(High Elevation/Voltage) -------+
                                |
(Lower Elevation/Voltage)       +-------




(Ground)                                .
```

While a large resistor would reduce the voltage significantly:

```
(High Elevation/Voltage) -------+
                                |
                                |
                                |
                                |
(Low Elevation/Voltage)         +-------
(Ground)                                .
```

## The Breadboard

Before we set to work building the circuit, we should also talk about breadboards.

And to understand breadboards, we can talk about pipes.

Let's say you're building your fluid circuit, complete with pipes, reservoirs, and pumps. 
If you know exactly what you want to build, and what parts go where, you only need to build it once;
you could potentially weld pipes and fuse parts together permanently. 
But if you're going through the process of assembling the circuit, 
you want more flexibility in how things are connected together. You want 
pipes with consistent diameters and standard fittings. You want valves and joints
that are designed to fit the pipes you're using. This makes everything interchangable.
If a part needs to be changed out, or a segment of pipe replaced, you can do it
without tearing apart the entire system.

Breadboards provide a way of rapidly building prototypes to work out
our final circuit layout. They're pretty simple, and are arranged to provide
groups of holes, designed for pins and wires, that are connected together
on a single "bus" (a piece of conducting metal) so that they are all at 
the same voltage. 

<img
width="500px" 
alt="Plain Breadboard"
src="/img/arduino20150610/photo_Breadboard.jpg">

The left and right sides of the board have positive and negative buses.
These are convenient because as long as you connect one hole in the plus 
column to a power source, and one hole in the minus column to a ground,
you can use the entire column of pluses and minuses as a power source.

The other group of holes, marked with letters and numbers, are groups of holes
connected by horizontal buses. This means that any wires connected to a given row
will all be at the same voltage.

If we plug one end of a pair of red and black wires into a 5 volt power source 
(like an Arduino) and its ground, respectively, then our breadboard would 
look like this:

<img
width="500px" 
alt="Breadboard With Power"
src="/img/arduino20150610/photo_BreadboardPower.jpg">

Under this configuration, the entirety of the plus and minus buses on the left side 
of the breadboard now have a 5 volt potential across them. Now, we can connect any hole
on the positive bus to any hole in the center of the breadboard (the lettered columns), 
and all the holes on the horizontal row containing that hole will be at the same voltage.

(Note that the left and right sides of the breadboard are isolated, so we could either connect
the plus and minus buses on the right side to another power source, or connect them to the plus and minus
buses on the left side of the board.)

# Assembling the Circuit

## The Setup 

Based on our discussion of LEDs and resistors, the first thing we'll want to do 
is check the voltage rating of our LED. We'll find most LEDs are rated for a maximum of 1-3 volts
(it depends on the manufacturer; sometimes different LED colors indicate the maximum voltage).

Using some math that we won't go into here (Ohm's Law),
we can determine that a resistance of anywhere between 200 ohms and 1 kilo-ohm
will be sufficient to keep from frying our LED.
Now, we can go on down to the resistor store and buy ourselves the right size resistor.

## Resistors in Series

But what if, like the aspiring hackers we are, we're too lazy to go to the 
resistor store, and we want to use our materials on hand instead?
Let's say all we have is a pack of 180 ohm resistors. Too small to 
work. Bummer, guess we're out of luck.

But wait! We're not out of luck at all! 
The beauty of bread boards is that it's really easy to add new components - like more resistors. 
And the beauty of resistors is that when resistors are put in series, their resistance
is additive (revisit the analogy of water flowing through a pipe to convince yourself
that this is true). While there are mathematical reasons for this, 
they are beyond the scope of what we're covering here.
All we really need to know is that we can put two resistors in series, 
and their resistance is additive. When we put two 180 ohm resistors in series,
we get the equivalent of a 360 ohm resistor. 

That's good news - it means we can be lazy!

Now let's get to the circuit diagram!

## Diagramming the Circuit

Now we can construct our circuit. We have 5 volts starting at the Arduino. 
Those electrons travel through the circuit to the two resistors,
through the two resistors (where their voltage drops), 
and into the LED, where the lowered voltage will light up our LED.
(If we only added one resistor, the voltage would be too high, 
and we would fry our LED.)

Here is a stylized circuit diagram that shows our "Hello World" circuit:

<img
height="400px" 
alt="Hello World Circuit Diagram With Power And Connection"
src="/img/arduino20150610/diagram_HelloWorldPowerConnections.jpg">

It is absolutely critical to understand the path that electrons take through the system.
The circuit always begins at the source of voltage. The direction the circuit travels 
is from higher voltage to lower voltage, or to the ground. In our diagram, the circuit
starts at the red wire connected to the Arduino Nano. The electrons travel through the 
circuit and toward the Arduino Nano's ground pin. 

(The final leg of the circuit, the black wire connecting the Arduino's ground 
to a "universal" ground, is not actually implemented on the breadboard; it is 
part of the Arduino's power cable. That way, we don't have to worry about whether the 
Arduino's ground pin is actually grounded.)

Converting this to a breadboard design is straightforward, 
although it will (inevitably) look different. We start by hooking up
the Arduino's 5 volt and ground pins to the breadboard's power bus:

<img
width="500px" 
alt="Hello World Breadboard With Power"
src="/img/arduino20150610/bb_HelloWorldPower.png">

Now we can use the power buses on the side of the breadboard to get some voltage
to power our components! Now we hook up our LED circuit to the power bus. The elctrons
start at the red positive junction, then travel through the resistors, through the LED,
and escape to ground:

<img
width="500px" 
alt="Hello World Breadboard With Power And Connection"
src="/img/arduino20150610/bb_HelloWorldPowerConnections.png">

(Note that the funny arrangement of LED legs is just a matter of convention,
the drawing program draws LEDs right-to-left while our circuit is laid out 
left-to-right.)

The long, or bent, leg of the LED is the positive side. That's the side
that connects with the resistors. 

The short leg of the LED is the negative side. That's the side that hooks up
to the ground.

<img
height="400px" 
alt="LED Diagram with Positive and Negative Labeled"
src="/img/arduino20150610/diagram_LED.png">

The breadboard uses a red and black wire to connect the Arduino's positive and negative pins
to the breadboard's positive and negative buses. The yellow wires then connect the positive 
voltage bus to the resistors, then to the LED, and finally to the ground, giving the electrons
a complete path that they can follow.

Here's how this maps onto the real Hello World circuit:

<img
width="800px"
alt="Parallel Hello World Photograph Circuit Diagram"
src="/img/arduino20150610/diagram_HelloWorldPowerConnectionsParallel.png">

The first thing you should look for is the source of voltage - those are the red and black wires. 
Those connect from the Arduino's positive and ground pins, to the breadboard's bus.
The first yellow wire connects the positive bus to the resistors, then to the LED,
and the other yellow wire connects the LED to ground, giving the electrons a complete path 
that they can follow.

Here's a picture of the finished circuit:

<img
width="500px" 
alt="Hello World Photograph"
src="/img/arduino20150610/photo_HelloWorldPowerConnections.jpg">

# Stay Tuned for Code

You may find it strange that this post does not contain 
a single line of code. In fact, that is intentional!
This post keeps things simple, by talking about the circuitry
independent of any microcontroller programming.
Arduino microcontrollers are complicated devices,
so it's important to tackle one thing at a time.

The circuit does not utilize any code, because the circuit
is connected to the Arduino's 5 volt pin, which is always
at 5 volts, so long as the microcontroller is plugged in.
So really, there's nothing to explore (yet).

We have a lot left to discuss, but for now, 
we've covered plenty. 

First, we introduced circuits by talking about voltage,
the principle concept in circuit design. 
We introduced the fluid flow analogy to help give 
the reader an intuition pump for thinking about voltage.

We then covered the details of the Hello World
circuit itself. We talked about what role the resistors 
play - and the role that resistance in general plays.
We covered the details of the LED. 

Finally, and importantly, we introduced various 
visual notation for describing circuits to the reader.

In future posts, we will expand on each of these concepts,
fill in missing details, and cover other key topics,
like current and its relationship to voltage.
