# matrix.py  03/10/2016  D.J.Whale
#
# An in-memory model/abstraction of the tone matrix.
# This is the data structure that maintains the current matrix state.
# It also, for performance reasons, contains the link to the tone player.

#TODO: Make this a class, so we could have multiple instances in an orchestra

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
    global num_cols, num_rows

    if cols > MAX_COLS or cols < 1:
        raise ValueError("Invalid cols:%d, allowed:1..%d" % (cols, MAX_COLS))
    if rows > MAX_ROWS or rows < 1:
        raise ValueError("Invalid rows:%d, allowed:1..%d" % (cols, MAX_COLS))

    num_cols = cols
    num_rows = rows

def set_cell(col, row, state):
    matrix[col][row] = state

def get_fingering(col):
    return matrix[col]

def next_index(col):
    return (col + 1) % num_cols

def clear():
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            matrix[i][j] = 0

def set_col(col, data):
    # overlay data, may be partial, incuding None for 'no change' placeholders
    for r in range(len(data)):
        s = data[r]
        if s is not None and s == 1:
            matrix[col][r] = 1



#----- MAIN -------------------------------------------------------------------


# END
