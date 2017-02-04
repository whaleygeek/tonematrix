# micro:bit Tone Matrix

Note, please use Python 2 for this.

It is not yet ported to Python3, and you will get errors in the serial
module if you use Python 3

# What's this?

The ToneMatrix is an instrument, a demonstration and a hobby project! We built it to demonstrate the way the micro:bit could talk to:

 * Other micro:bits using the wireless 'Radio' protocol
 * A Raspberry Pi over serial

And also we wanted something that would make nice sounds

In the simplest form, it's a grid of 40 micro:bits, each of which can be 'on' or 'off'. These talk to a 'bridge' micro:bit connected to a Raspberry Pi. The bridge sends out anything that it receives on the radio over serial, and vice versa. The bridge is also responsible for provisioning the micro:bits when you first power everything on.

Here's a video to help explain.
[![Youtube video of the Tone Matrix](https://img.youtube.com/vi/nzg_t5WtEk4/0.jpg)](https://www.youtube.com/watch?v=nzg_t5WtEk4&feature=youtu.be&t=76)


Each micro:bit represents a note in a song, and we arrange the micro:bits into rows and columns:

![The tone matrix](graphics/overview.png)

Rows represent pitch, from low pitch to high pitch
Columns represent beats in a bar, (we have 8 beats in a bar here)
[Here's a larger example of the same idea.](http://tonematrix.audiotool.com/)

# Overview

There are 41 microbits and one Raspberry Pi. 40 micro:bits in the matrix itself, one as the radio<-->serial bridge connected to the Raspberry Pi

    Unformated text
	Grid of micro:bits                           +---+ Bridge
	                                   <-------> | B | micro:bit
	+---+---+---+---+---+---+-------+   Radio    +-+-+
	|   |   |   |   |   |   |   |4,7|              |
	+-------------------------------+              |USB
	|   |   |   |   |   |   |   |   |            +----------+
	+-------------------------------+            |          |
	|   |   |   |   |   |   |   |   |            |Raspberry |
	+-------------------------------+            |Pi        |
	|1,0|   |   |   |   |   |   |   |            |          |
	+-------------------------------+            +----------+
	|0,0|0,1|   |   |   |   |   |   |            +----------+
	+---+---+---+---+---+---+---+---+            | Speaker  |
	                                             +----------+


# Controls and UI

When things are in full swing (See 'Setup' and 'Provisioning' below) the following controls 

When a micro:bit is 'off' it shows nothing on the screen normally. It will show a single dot on the screen when the column that this micro:bit is in is played (so, the single dots should process around/across the tone matrix)

When a micro:bit is 'on' it has a central 3x3 square illuminated. When the column that this microbit is in is played, the whole screen lights up.

The following controls exist

## For the grid nodes

* Button A: Turn a micro:bit in the grid off
* Button B: Turn a micro:bit in the grid on
* Buttons A+B: Report grid position (flashes up row number then col number)

* Pin 0 shorted to ground: Increase col number
* Pin 1 shorted to ground: Increase row number
* Pin 2 shorted to ground: Reset row and col number to (0,0)

After micro:bits have been manually provisioned into the grid, they show a '?' on the screen until you set their state using the A or B button.

**(Notice this seems 'backwards' compared to the order we report things when pressing AB - TODO: fix this)**

* Shake: Toggle on/off state

## For the bridge

* Button A: Increase tempo
* Button B: Decrease tempo

**Note that the default tempo on the bridge is lower than the default on the Pi so the first use of the tempo change buttons will reduce the tempo no matter which button is pressed. I tend to avoid using these**


When the micro:bits are turned off, they lose all information about where in the grid they are.

Therefore, before using the tone matrix you have to provision each micro:bit to tell it the position it should have in the matrix.

# Provisioning

The provisioning is handled by the 'bridge' micro:bit. Perform the folowing steps

 * Power off all micro:bits in the grid
 * Power on the bridge
 * Ensure that the tone matrix software is not running on the Pi
 * Plug in/reset each micro:bit in turn, starting in the bottom left hand corner and running along the rows then up the columns
 * as each micro:bit is provisioned it will flash up its column/row so that you can check it has been allocated the right spot. If for some reason a micro:bit is not allocated to the right spot (this uses a broadcast radio, so packets can be dropped) then there are two possible outcomes
   * The bridge didn't see the provisioning request. In this case, just power cycle the micro:bit
   * The bridge tried to provision the micro:bit but the micro:bit didn't receive the message. In this case, the next micro:bit that is provisioned will be the next position in the grid, so you should 
     * Leave a gap where the failed micro:bit should have been
     * Reset the micro:bit, and when it provisions correctly put it in the next slot
     * Come back at the end and manually provision a micro:bit to the gap by using pins 2,1,0 to manually provision it.
 * once all micro:bits are provisioned, turn on the tone_matrix program


# Troubleshooting

If a micro:bit ends up provisioned to something outside the valid grid (for example, if someone touches the pins and increases the row or column number) that may cause the code on the Pi to crash (TODO: fix this!). Ideally, try to find out which micro:bit is the problem, use P2,1,0 to reprovision it and restart the python software

If the software on the Pi crashes (and it does sometimes... sorry) then there is no way currently programmed to reset all the micro:bits, so the state gets out of sync. The easiest thing to do is to turn off all the micro:bits in the grid manually at this point.

Sometimes the 'ack' of the state change is not received by one of the micro:bits. IE the Pi will change it's state but the micro:bit display won't update. This is an inevitable result of using a very simple broadcast radio. It's a great learning opportunity to ask kids how you might deal with this (retransmission, packet loss counts, slots for send/recieve, etc!).  The best way to workaround the issue when the matrix says "all off" but there is still sound playing is to turn on a micro:bit in a known position (I usually use (0,0)) and then try to work out which micro:bit is stuck on relative to that. This is often an iteritive process, but works in the end

Sometimes the 'change state' command is not received by the Pi. Just press the button again!

# Physical Display Stand

There are files for a physical display stand in the `graphics` directory. This has ben designed to be cut out of two sheets of 600x400mm sheet of 3mm ply. 

The SVGs were generated in Inkscape and you will need to use 'Outline' view mode to understand them properly (View-->Display Mode-->Outline).

These laser cutter files are redistributeable under a CC-BY-SA 4.0 license. This license does not apply to the rest of the repository.

[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](http://creativecommons.org/licenses/by-sa/4.0/)
Author: Jonathan Austin

