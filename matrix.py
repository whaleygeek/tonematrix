# matrix.py  03/10/2016  D.J.Whale

"""A simple tone-matrix note player"""

# PLATFORM SPEC
# This code will eventually run on a Raspberry Pi.
# Initial version will probably run (with text trace, not sound) on Mac for testing
# pyserial used with portfinder tool and buffer handler from anyio project
# pygame.mixer used to play sounds (8 sounds max, preloaded, mixed on the fly)
# test sounds to be generated initially in Audacity, all the same length.
# 5 tones pentatonic, but might auto generate all 12 semitones for completeness
# so that any of the pentatonic scale roots could be used.


# FUNCTIONAL SPEC
# N micro:bit sensors send commands via radio. Each has unique address.
# A micro:bit gateway (over serial) sends configuration commands to the Pi.
# The pi sends back acknowledgements, and beat timing.
# gateway re broadcasts all incoming serial data to radio interface
# The pi mixes and plays notes, based on the current tonematrix configuration.
# There is no user interface on the Pi, the gateway bit and sensor bits are the UI.


# PSEUDO-CODE

# init matrix state data store
#   define list of lists of max size
#   set col and row size constants to same default as micro:bit gateway uses

# open serial port
#   use whaleygeek's anyio port finder from anyio to discover or reuse serial port
#   fail if serial port cannot be opened

# start beat timer
#   using Timer() class, set up the beat interval to default bpm

# received message
#   (non blocking)
#   if a whole line is in the buffer waiting to be processed,
#       return it
#   else
#       return None

# decode and handle message
#   strip out first char, this is the command
#   dispatch command to appropriate handler
#   if T send to time change handler
#   if S send to size change handler
#   if C send to state change handler
#   anything else, drop with a warning

# time change handler
#   T,NNN
#   (note, no ack)

# size change handler
#   S,NN,NN
#   (note, no ack)

# state change handler
#   C,{0-8},{0-8},(1,0)
#   send ack: A,{0-8},{0-8},(1,0)

# time for a beat
#   use whaleygeek's Timer() class from pyenergenie demos
#   uses time horizons, decide what happens if late

# send beat sync
#   get present column index
#   form beat command
#   send beat command (non blocking)
#   increment column modulo size
#   restart timer with current BPM value
#   decide note to play from matrix configuration
#   mix and play the note (duration is fixed?)

# form beat command
#   B,NN

#----- MAIN -------------------------------------------------------------------

def main():
    pass
    # init matrix state data store
    # open serial port
    # start beat timer
    # forever
    #   if received message
    #       decode and handle message
    #   if time for beat
    #       send beat sync

if __name__ == "__main__":
    main()

# END
