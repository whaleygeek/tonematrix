# user_interface.py  20/10/2016  D.J.Whale
#
# The interface to a canvas of micro:bit devices

import time

##microbit = DummyMicrobit()
import microbit #will auto connect



#----- DUMMY MICROBIT ---------------------------------------------------------

class DummyMicrobit():
    def __init__(self):
        self.testdata = [
            # time offset in seconds, command
            (5, "C,0,0,1"),
            (5, "C,0,2,1"),
            (5, "C,0,4,1"),
            (6, "T,240"),
            (10,"S,2,5")
        ]
        self.start_time = time.time()
        self.next_test_idx = 0

    def get_next_message(self):
        if self.next_test_idx < len(self.testdata):
            # There are still tests to run
            time_offset, msg = self.testdata[self.next_test_idx]
            target_time = self.start_time + time_offset
            now = time.time()

            if now >= target_time:
                # Advance to next test
                self.next_test_idx += 1
                return msg # message will be processed

        return None # No message

    def send_message(self, message):
        print("to_microbit:%s" % str(message))
        microbit.send_message(message)



#----- MESSAGE RECEPTION ------------------------------------------------------

def poll_message(): #TESTED OK
    return microbit.get_next_message()
    #   (non blocking)
    #   if a whole line is in the buffer waiting to be processed,
    #       return it
    #   else
    #       return None

def decode_and_handle(msg): # TESTED OK
    # First char is cmd, rest is data
    #TODO:parser exception
    # First find what kind of message we have
    if ":" in msg:
        # We're dealing with the pxt 'data:value' pair
        cmdchar = msg.split(":")[0]
        data = msg.split(":")[1]
    else:
        cmdchar = msg[0]
        comma   = msg[1]
        data    = msg[2:]
        if comma != ',':
            print("warning: malformed message:%s" % msg)
            return None

    if cmdchar == 'bpm': # timing change
        return handle_bpm_change(data)

    elif cmdchar == 'rows': # size change
        return handle_rows_change(data)

    elif cmdchar == 'cols': # size change
        return handle_cols_change(data)

    elif cmdchar == 'C': # state change
        return handle_state_change(data)

    else:
        print("warning: unknown command received:%s" % cmdchar)
        return None

def handle_bpm_change(msg): # TESTED OK
    # time change handler
    #   [T,]NNN
    #   (note, no ack)

    #TODO: parser exception
    bpm = int(msg)

    return ("BPM", bpm)

def handle_cols_change(msg):
    # change just the cols
    #   (note, no ack)
    cols = int(msg) #TODO: number format exception
    return ("COLS", cols)

def handle_rows_change(msg):
    # change just the rows
    #   (note, no ack)
    rows = int(msg) #TODO: number format exception
    return ("ROWS", rows)

def handle_size_change(msg): # TESTED OK
    # size change handler
    #   [S,]NN,NN
    #   (note, no ack)

    fields = msg.split(',')
    cols, rows = fields #TODO: number of params exception
    cols = int(cols) #TODO: number format exception
    rows = int(rows) #TODO: number format exception

    return ("SIZE", cols, rows)

def handle_state_change(msg): # TESTED OK
    #  state change handler
    #   [C,]{0-8},{0-8},(1,0)

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

def get_beat_command_msg(idx): # TESTED OK
    # form beat command
    #   B,NN
    return "B,%d" % idx

def get_ack_state_change_msg(col, row, state): # TESTED OK
    # form ack state change command
    #   A,NN,NN,N
    return "A,%d,%d,%d" % (col, row, state)

def send_msg(msg): # TESTED OK
    if msg[-1] != '\n':
        msg += '\n'
    microbit.send_message(msg)

def send_sync_beat(col): # TESTED OK
    msg = get_beat_command_msg(col)
    send_msg(msg)

def process(): # TESTED OK
    """Poll and process one message"""
    req = poll_message()
    rsp = None
    if req != None:
        rsp = decode_and_handle(req)

    return rsp

# END
