# user_interface.py  20/10/2016  D.J.Whale
#
# The interface to a canvas of micro:bit devices

##import microbit #will auto connect?

#TODO: Add parser exceptions for invalid data received

#----- MESSAGE RECEPTION ------------------------------------------------------

def poll_message():
    return None # TODO
    #   (non blocking)
    #   if a whole line is in the buffer waiting to be processed,
    #       return it
    #   else
    #       return None

def decode_and_handle(msg):
    # First char is cmd, rest is data
    #TODO:parser exception
    cmdchar = msg[0]
    comma   = msg[1]
    data    = msg[2:]

    if comma != ',':
        print("warning: malformed message:%s" % msg)
        return None

    if cmdchar == 'T': # timing change
        return handle_bpm_change(data)

    elif cmdchar == 'S': # size change
        return handle_size_change(data)

    elif cmdchar == 'C': # state change
        return handle_state_change(data)

    else:
        print("warning: unknown command received:%s" % msg)
        return None

def handle_bpm_change(msg):
    # time change handler
    #   [T,]NNN
    #   (note, no ack)

    #TODO: parser exception
    bpm = int(msg)

    return ("BPM", bpm)

def handle_size_change(msg):
    # size change handler
    #   [S,]NN,NN
    #   (note, no ack)

    fields = msg.split(',')
    cols, rows = fields #TODO: number of params exception

    return ("SIZE", cols, rows)

def handle_state_change(msg):
    #  state change handler
    #   [C,]{0-8},{0-8},(1,0) #NOTE: Why single digit when others are double digit??

    fields = msg.split(',')
    col, row, state = fields #TODO: number of params exception
    #TODO: parse exception
    col   = int(col)
    row   = int(row)
    state = int(state)

    ack_msg = get_ack_state_change_msg(col, row, state)
    send_msg(ack_msg)

    return ("STATE", col, row, state)


#----- MESSAGE TRANSMISSION ---------------------------------------------------

def get_beat_command_msg(idx):
    # form beat command
    #   B,NN
    return "B,%02d" % idx

def get_ack_state_change_msg(col, row, state):
    # form ack state change command
    #   A,NN,NN,N
    return "A,%02d,%02d,%1d" % (col, row, state)

def send_msg(msg):
    print("send_msg:%s" % str(msg))
    #TODO: Knit up to microbit.send()

def send_sync_beat(col):
    msg = get_beat_command_msg(col)
    send_msg(msg)

def process():
    """Poll and process one message"""
    req = poll_message()
    rsp = None
    if req != None:
        rsp = decode_and_handle(req)

    return rsp

# END
