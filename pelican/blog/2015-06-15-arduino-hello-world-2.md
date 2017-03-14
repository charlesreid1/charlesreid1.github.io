---
title: Arduino for Visual Thinkers - Hello World from Nano, Leonardo, and Pi!
date: 2015-06-15 11:09:00 -0700
status: draft
category: InternetOfThings
tags: programming, visual, arduino, arduino nano, arduino leonardo, raspberry pi, microcontrollers, science, electricity
REMOVEME_status: draft 
---

<img
width="500px" 
class="center-block img-responsive"
alt="Arduino Hello World on a Pi"
src="/img/arduino20150615/photo_HelloWorld_Pi.jpg">

Let's revisit our [original Arduino Hello World walkthrough](charlesreid1.com/arduino-for-visual-thinkers-hello-world.html), 
but where we were using an Arduino Nano last time, this time we'll 
build the same circuit on a Leonardo and a Raspberry Pi.

Again, we're keeping it dead simple, to minimize the number of concepts you need to juggle in your brain.
What we're doing is building a circuit that uses the Arduino or Pi onboard power to light up a little 
LED bulb. This requires hooking up to the on-board voltage and ground that microcontrollers provide.

First, let's talk about the differences between these microcontrollers.

<img 
width="200px" 
src="/img/arduino20150615/default_Micro.png">
<img 
align="middle"
width="350px" 
src="/img/arduino20150615/default_Leo.png">
<img 
align="middle"
width="350px" 
src="/img/arduino20150615/default_Pi.png">


Revisiting Hello World on the Arduino, to show how to make the same circuit with other microcontroller devices.

Leonardo, Nano, and Pi - parallels between these microncontroller circuit designs, and replicating them

What the difference is between these different microcontrollers

The Outline:
* The hook
    * consusing world of many different types of microcontrollers
    * (but before we talk about) differences,
    * (let's talk about) similarities
* recap of hello world circuit: the nano
    * used a nano
    * used voltage from nano
    * cascade of water analogy
    * resistor to decrease voltage
    * LED
    * the ground
* building the hello world circuit on the Leonardo
    * what does the Leonardo have?
    * pinout diagram of what it looks like
    * the circuit, layout
    * the circuit, built
    * what's similar
        * the voltage is the same
        * can still use breadboard the same way
        * interchangeable, because of similar voltages
        * mainly just more pins
        * more pins leads into, what's the additional variable besides voltage
        * voltage is the energy level
        * current is the "how much"
    * powering the Leonardo: what's different
        * the power cord is not a USB cable
        * the voltage is the same
        * so what's different? 
        * CURRENT
        * providing voltage on more pins
        * ASIDE: Ohm's Law
        * ASIDE: AC vs DC
        * ASIDE: How a power adapter works
    * still no code? still no code.
* building the hello world circuit on the raspberry pi
    * what does the raspberry pi have
    * circuit layout
    * circuit built
    * similarities
        * voltage
        * can still use breadboard, can re-use same circuit
        * pins
        * more stuff
        * also, obviously, pins are just small part of much more complicated system
        * power cord - like leonardo, more stuff requires more current
    * the differences
        * bigger difference between arduino and raspberry pi
        * the pi is beefy enough to run a full operating system
        * more complex instruction sets are available
        * more complex (higher-level) languages can be used
        * side note - very useful vehicle for understanding how computers work
        * this is a full blog post in itself
        * more components means more circuitry
* mention: home and industrial tie-ins, higher voltages, higher currents
    * you can't do terribly useful things with 5 V and a few microamps
    * but with power, what can you do?
    * run a compressor to cool your fridge
    * run current through heating elements to toast bread
    * operate a pump to shoot water into your dishwasher
    * if you move to the industrial scale,
    * bigger motors, bigger compressors, 
    * more voltage and more current,
    * but the basic concept is still the same
    * operate door on ATM cash dispenser
    * if you replace the circuit so it has a much higher voltage/current, 
    * and you replace the LED with a high-power spotlight,
    * you'll get a regular home circuit.
* conclusion:
    * covered hello world circuit with 3 devices
    * showed parallels and differences between them
    * most important similarity is the voltage - each one provides same voltage
        * allows re-use of circuit and components
        * convenient! can develop circuits with nanos, then switch them all over to single Leonardo 
    * most important difference: more components, more current, so differences in power
        * voltage and current and resistance
        * fluid flow analogy, three critical pieces
    * later post, we'll talk about how voltage, current, resistance are related through ohm's law

