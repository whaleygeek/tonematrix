# user_interface.py  20/10/2016  D.J.Whale
#
# The interface to a canvas of micro:bit devices

import time
##import microbit #will auto connect?


#----- MESSAGE RECEPTION ------------------------------------------------------

def poll_message():
    return None # TODO
    #   (non blocking)
    #   if a whole line is in the buffer waiting to be processed,
    #       return it
    #   else
    #       return None

def decode_and_handle(msg):
    pass # TODO
    # decode and handle message
    #   strip out first char, this is the command
    #   dispatch command to appropriate handler
    #   if T send to handle_bpm_change
    #   if S send to handle_size_change
    #   if C send to handle_state_change
    #   anything else, warning, and drop
    # return return result of called function to allow a rec to be passed back

def handle_bpm_change(msg):
    pass # TODO
    # time change handler
    #   T,NNN
    #   (note, no ack)
    # change bpm variable

def handle_size_change(msg):
    pass # TODO
    # size change handler
    #   S,NN,NN
    #   (note, no ack)
    # change num_cols and num_rows
    # init present_col to zero
    # resync timer

def handle_state_change(msg):
    pass # TODO
    #  state change handler
    #   C,{0-8},{0-8},(1,0) ### Why single digit when others are double digit??
    #   send ack: A,{0-8},{0-8},(1,0)
    # matrix[col][row] = state
    # just return this as a rec, process will pass up to main driver to action


#----- MESSAGE TRANSMISSION ---------------------------------------------------

def get_beat_command_msg(idx):
    # form beat command
    #   B,NN
    pass #TODO

def get_ack_state_change_msg(col, row):
    # form ack state change command
    #   A,NN,NN,N
    pass # TODO

def send_msg(msg):
    pass #TODO: Knit up to microbit.send()

def send_sync_beat(col):
    now = time.time()
    print("BEAT %d" % now) #TODO
    msg = get_beat_command_msg(col)
    send_msg(msg)

def process():
    """Poll and process one message"""
    msg = poll_message()
    if msg != None:
        decode_and_handle(msg)

    #TODO: If it is a matrix reconfig, return rec(col, row, state)

# END
