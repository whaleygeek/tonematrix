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


#----- ACTIONS ----------------------------------------------------------------

def change_size(cols, rows):
    pass # TODO

def set_note(col, row, state):
    matrix[col][row] = state

def get_fingering(col):
    return matrix[col]

def next_index(col):
    return (col + 1) % num_cols


#----- MAIN -------------------------------------------------------------------


# END
