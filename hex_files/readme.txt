microbit-test-tonematrix.hex
  A simple PXT test.
  Shake it and it toggles col 1 row 1 state.
  When it receives B,1, if it is enabled, it flashes it's screen.


bridge.js:
  A radio bridge that echos over the radio anything sent over serial
  and vic versa.

  Buttons A and B cycle through the row and col count, using the px
  'send data' function, that gices 'cols:N' and "rows:N'

  It conversts to blocks

matrix-node.js
  This is the code for a node in the matrix. It currently uses A and B
  for 'Off' and 'On' respectively, or shake for toggle.

  Changes to the state are not made until the acknowledgement is sent 
  from the Pi.

  It also uses a 'provisioning' system whereby on startup it asks to be
  sent the row and col that it should belong to. This should make turning
  40 micro:bits on during the demo a lot easier. The pins P0 and P1 are
  used to manually override this provisioning data.


