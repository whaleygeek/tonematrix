# matrix.py  03/10/2016  D.J.Whale
#
# An in-memory model/abstraction of the tone matrix.
# This is the data structure that maintains the current matrix state.
# It also, for performance reasons, contains the link to the tone player.


#----- CONFIG -----------------------------------------------------------------

MAX_COLS = 10 # 0..9
MAX_ROWS = 10 # 0..9

DEFAULT_COLS = 5
DEFAULT_ROWS = 5


#----- STATE ------------------------------------------------------------------

# stored rotated ([col][row]) for easy indexing later
matrix = [ [0 for i in range(MAX_ROWS)] for j in range(MAX_COLS) ]

num_cols    = DEFAULT_COLS
num_rows    = DEFAULT_ROWS
present_col = 0

##def set_note(col, row, state):
##    pass # TODO set note at col,row to state (on or off)
##    #TODO re-calculate the tone pattern for that column, for fast playback later
##    #Note, would be good to be able to cache actual note references in tone.py
##    #on a change, so it doesn't have to keep recalculating from a list of strings
##    #each time round the loop


#----- NOTE GENERATION --------------------------------------------------------

##def play_notes(idx):
##    col_data = matrix[idx]
##
##    # trigger all notes to play simultaneously
##    # all positions that are set to 1, play that note
##    #TODO: Check in reality, whether pygame.mixer plays a chord or an arpeggio?
##    for i in range(len(notes)):
##        if col_data[i] == 1:
##            #notes[i].play()
##            pass # TODO


def get_index():
    return present_col


def get_next_chord():
    global present_col
    # Try to minimise the computation by returning memoized patterns
    # if the pattern has not changed since last time.

    chord = ['A','D','E'] #TESTING

    present_col = (present_col + 1) % num_cols

    return chord


#----- MAIN -------------------------------------------------------------------


# END
