# How to Examine a Circuit Board

*Material for a [UC Irvine](https://uci.edu/) course offered by the [Department of Physics Astronomy](https://www.physics.uci.edu/) and developed by [David Kirkby](https://faculty.sites.uci.edu/dkirkby/).*

## Introduction

In this course, we have focused on designing and building circuits from scratch using components and modules that are intended for easy prototyping. We use jumper wires and a breadboard to make electrical connections and use a USB connection to provide power and support firmware program development.

The electronics that surrounds us looks very different however, with traces on a [printed circuit board (PCB)](https://en.wikipedia.org/wiki/Printed_circuit_board) replacing our jumper wires and bread board. Even the resistors and capacitors look completely different in their tiny [surface mount packages](https://en.wikipedia.org/wiki/Surface-mount_technology).

In this activity, you will learn how to examine a printed circuit board to discover its overall organization and basic functions. You may either use the circuit board in a device you bring from home (with the understanding that some destructive disassembly will likely be required) or else one provided by the instructor. Follow the steps below to examine your board and record your results in a google doc using the headings below.

## Appearance

Take a photo of your PCB including a ruler for scale and insert it into your document. Give the approximate dimensions.

If the PCB is not rectangular, what might be the purpose of its custom shape?

Are there any cutouts or holes in the PCB? What is their purpose?

## Identification

Record any identifying information on the silkscreen. Are you able to identify the purpose of this circuit using this information?

Look for identifying information on any large chips on the PCB. Look these up and make a note of what type of part they are, if possible.

## Construction

What fraction of the components use [surface-mount technology (SMT)](https://en.wikipedia.org/wiki/Surface-mount_technology)? The alternative to SMT is through-hole mounting, where leads pass through a hole drilled in the PCB. Do you see any through-hole components on your PCB?

Can you determine how many layers the printed circuit board has? (Hint: look for [vias](https://en.wikipedia.org/wiki/Via_(electronics))).

Can you identify [ground plane](https://en.wikipedia.org/wiki/Ground_plane) areas or wider traces on the PCB that likely carry significant current?

Your circuit might have some components that are sealed in epoxy. This technique, known as "potting" can serve several different purposes:
 - to improve safety by isolating high-voltage connections,
 - to eliminate mechanical vibrations from a nearby speaker or motor that could wear out connections,
 - to protect sensitive components from dust or liquids,
 - to protect the intellectual property of the circuit designer.

## Power

Where does power enter the circuit? Is it powered by a battery (DC) or wall power (AC) or both? Since almost all circuits use low-voltage DC power internally, an AC-powered device will likely include an AC-to-DC [transformer](https://en.wikipedia.org/wiki/Transformer)). If your circuit uses a battery what voltage does it provide and how much capacity (mA-hours) does it have? Are the batteries rechargeable or replaceable?

Can you determine what voltage your PCB operates at? The majority of digital circuits operate at 5V or 3.3V so that is always a good guess. Circuits often include a [voltage regulator](https://en.wikipedia.org/wiki/Voltage_regulator) to provide a reliable low-voltage DC output. You can look up their part number to determine what this voltage is.

Where is the power conditioning section of the circuit? (Hint: look for large [electrolytic capacitors](https://en.wikipedia.org/wiki/Electrolytic_capacitor))

Does the circuit control any high powered devices? (Hint: look for [relays](https://en.wikipedia.org/wiki/Relay) or [power switching transistors](https://en.wikipedia.org/wiki/Power_semiconductor_device)).

## Connections

What external connections does the circuit have?

Do you recognize any standard connectors? (e.g. USB)

## Interactions

How does the user interact with the circuit?

Identify any buttons, switches, potentiometers, etc

Identify any LEDs or other display elements.

## Wireless Communication

Can you identify an antenna connection or else a section of PCB trace that forms an antenna?

Is part of the circuit shielded against RF interference by enclosing it with metal? Components within such a shield often carry radio or microwave frequency signals associated with wireless communications.

## Processing

Can you identify any programmable chips or memory chips on the PCB? These will usually have a large number of pins and markings that you can google.

A programmable chip usually requires a nearby [crystal oscillator](https://en.wikipedia.org/wiki/Crystal_oscillator) to establish the timing of its instructions. Can you find one?
