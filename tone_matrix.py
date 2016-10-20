# tone_matrix.py  20/10/2016  D.J.Whale
#
# The main application of the tone matrix demonstration

import user_interface
import matrix
import tones

from Timer import Timer

DEFAULT_BPM  = 120 # must be longer than the longest note, to prevent glitching

bpm          = DEFAULT_BPM
timer        = Timer(60.0/bpm)
colidx       = 0

scale = ['C', 'C#', 'D', 'D#', 'E', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'C']
tones.set_scale(scale)

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
                timer.config(bpm)
                timer.sync()

            elif cmd == "STATE":
                # change matrix state
                print("STATE:change:%s" % str(change_rec))
                cmd, col, row, state = change_rec
                matrix.set_note(col, row, state)

            elif cmd == "SIZE":
                # change num_cols and num_rows
                # init present_col to zero
                # resync timer
                pass # TODO

            else:
                print("warning: unhandled cmd:%s" % str(change_rec))


if __name__ == "__main__":
    main()


# END