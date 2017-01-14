# tonematrix

Note, please use Python 2 for this.

It is not yet ported to Python3, and you will get errors in the serial
module if you use Python 3

# Provisioning

The provisioning is handled by the 'bridge' micro:bit. Perform the folowing steps

 * Power off all micro:bits in the grid
 * Power on the bridge
 * Ensure that the tone matrix software is not running on the Pi
 * Plug in/reset each micro:bit in turn, starting in the bottom left hand corner and running along the rows then down the columns
 * as each micro:bit is provisioned it will flash up its column/row so that you can check it has been allocates the right spot.
 * once all micro:bits are provisioned, turn on the tone_matrix program

