# matrix.py  03/10/2016  D.J.Whale

"""A simple tone-matrix note player"""

#import microbit #will auto connect at moment, might change this later
from Timer import Timer
import time
#import pygame

# PLATFORM SPEC
# This code will eventually run on a Raspberry Pi.

# Initial version will probably run (with text trace, not sound) on Mac for testing
# pyserial used with portfinder tool and buffer handler from anyio project
# pygame.mixer used to play sounds (8 sounds max, preloaded, mixed on the fly)
# test sounds to be generated initially in Audacity, all the same length.
# 5 tones pentatonic, but might auto generate all 12 semitones for completeness
# so that any of the pentatonic scale roots could be used.


#----- CONFIG -----------------------------------------------------------------

MAX_COLS = 10 # 0..9
MAX_ROWS = 10 # 0..9

DEFAULT_COLS = 5
DEFAULT_ROWS = 5
DEFAULT_BPM  = 120

#TODO:preload all sounds
#TODO: make this data driven so easy to use other scales
#pygame.mixer.init()
#note_cs = pygame.mixer.Sound("C#.wav")
#note_ds = pygame.mixer.Sound("D#.wav")
#note_fs = pygame.mixer.Sound("F#.wav")
#note_gs = pygame.mixer.Sound("G#.wav")
#note_as = pygame.mixer.Sound("A#.wav")
#notes = [note_cs, note_ds, note_fs, note_gs, note_as]
notes = ["Cs", "Ds", "Fs", "Gs", "As"]


#----- STATE ------------------------------------------------------------------

# stored rotated ([col][row]) for easy indexing later
matrix = [ [0 for i in range(MAX_ROWS)] for j in range(MAX_COLS) ]

bpm         = DEFAULT_BPM
num_cols    = DEFAULT_COLS
num_rows    = DEFAULT_ROWS
present_col = 0

timer       = Timer(60.0/bpm)


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


#----- MESSAGE TRANSMISSION ---------------------------------------------------

def get_beat_command(idx):
    # form beat command
    #   B,NN
    pass #TODO

def get_ack_state_change(col, row):
    # form ack state change command
    #   A,NN,NN,N
    pass # TODO

def send_msg(msg):
    pass #TODO: Knit up to microbit.send()

def send_sync_beat():
    now = time.time()
    print("BEAT %d" % now) #TODO
    msg = get_beat_command(present_col)
    send_msg(msg)


#----- NOTE GENERATION --------------------------------------------------------

def play_notes(idx):
    col_data = matrix[idx]

    # trigger all notes to play simultaneously
    # all positions that are set to 1, play that note
    #TODO: Check in reality, whether pygame.mixer plays a chord or an arpeggio?
    for i in range(len(notes)):
        if col_data[i] == 1:
            #notes[i].play()
            pass # TODO


#----- MAIN -------------------------------------------------------------------

def main():
    global present_col
    # start beat timer
    timer.sync()

    # loop forever
    while True:
        # maintain timing
        if timer.check():
            send_sync_beat()
            play_notes(present_col)
            present_col = (present_col + 1) % num_cols

        # process incoming config messages
        msg = poll_message()
        if msg != None:
            decode_and_handle(msg)

if __name__ == "__main__":
    main()

# END
