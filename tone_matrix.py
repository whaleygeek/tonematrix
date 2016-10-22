# tone_matrix.py  20/10/2016  D.J.Whale
#
# The main application of the tone matrix demonstration

import user_interface
import matrix
import tones
from Timer import Timer


#----- CONFIG -----------------------------------------------------------------

DEFAULT_BPM  = 120 # must be longer than the longest sample length, to prevent glitching
# A pentatonic tone matrix
MATRIX_COLS  = 5
MATRIX_ROWS  = 5

#NOTE: This must match the size of the matrix
#scale = ['C', 'C#', 'D', 'D#', 'E', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'C']
#scale = ['C','D','E','F','G','A','B']
scale = ['C#', 'D#', 'F#', 'G#', 'A#'] # One of many pentatonic scales
tones.set_scale(scale)


#----- STATE ------------------------------------------------------------------

bpm          = DEFAULT_BPM
timer        = Timer(60.0/bpm)
colidx       = 0


#----- TEST DATA --------------------------------------------------------------

matrix.change_size(MATRIX_COLS, MATRIX_ROWS)
matrix.clear()
##matrix.set_col(0, [0,1])
##matrix.set_col(2, [0,2,4])


#----- MAIN -------------------------------------------------------------------

def main():
    global bpm, colidx

    # start beat timer
    timer.sync()

    # loop forever
    while True:
        # maintain timing
        if timer.check():
            user_interface.send_sync_beat(colidx)
            fingering_mask = matrix.get_fingering(colidx)
            ##print("fingering_mask:%s" % str(fingering_mask))

            tones.play_chord(scale, fingering_mask)
            colidx = matrix.next_index(colidx)

        # process incoming and outgoing messages from/to the user interface
        change_rec = user_interface.process()

        # action any matrix reconfiguration messages or time change messages
        if change_rec != None:
            cmd = change_rec[0]

            if cmd == "BPM":
                # change timer rate
                print("BPM:change:%s" % str(change_rec))
                cmd, new_bpm = change_rec
                bpm = new_bpm
                timer.config(60.0/bpm)
                timer.sync()

            elif cmd == "STATE":
                # change matrix state
                print("STATE:change:%s" % str(change_rec))
                cmd, col, row, state = change_rec
                matrix.set_cell(col, row, state)

            elif cmd == "SIZE":
                # change num_cols and num_rows
                cmd, cols, rows = change_rec
                matrix.change_size(cols, rows)
                colidx = 0 # restart from left in case now smaller
                timer.sync() # restart timing

            else:
                print("warning: unhandled cmd:%s" % str(change_rec))


if __name__ == "__main__":
    main()


# END