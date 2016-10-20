# tones.py  20/10/2016  D.J.Whale
#
# A simple abstract interface to playing tones
# This is mainly to allow testing on a non pygame platform (while travelling!)

from Timer import Timer



class PygameTone():
    def __init__(self, note_names):
        self.note_names = note_names

        # Init the sound driver
        import pygame
        pygame.mixer.init()

        # Cache all sound files, ready to mix/play
        notes = []
        min_length = 9999
        max_length = 0

        for name in note_names:
            note = pygame.mixer.Sound("sounds/%s.wav" % name)
            notes.append(note)

            # Work out longest and shortest play time, for later
            length = note.get_length()
            if length > max_length:
                max_length = length
            if length < min_length:
                min_length = length

        self.notes  = notes
        self.chords = []
        self.max_length = max_length
        self.min_length = min_length

    def play_chord(self, chord):
        # Memoise a set of note instances references for this chord pattern
        if not chord in self.chords:
            sounds = []
            for note in chord:
                sounds.append(self.notes[note])
            self.chords.append(sounds)
        else:
            sounds = self.chords[chord]

        # Play the required chord pattern
        for note in sounds:
            note.play()


class DummyTone():
    def __init__(self, note_names):
        pass

    def play_chord(self, chord):
        print("play_chord:%s" % str(chord))


scale = None
driver = None

def set_scale(scale_data):
    global scale, driver
    scale = scale_data
    driver = DummyTone(scale)

def play_chord(scale, fingering_mask):
    print("play_chord: %s with fingering_mask %s" % (str(scale), str(fingering_mask)))

    # build the fingered chord from the scale
    #TODO the fingering needs to be cached so that we don't keep regenerating it each call.
    chord = []
    for i in range(len(scale)):
        if fingering_mask[i] == 1:
            chord.append(scale[i])

    driver.play_chord(chord)


#----- TEST HARNESS -----------------------------------------------------------

if __name__ == "__main__":
    scale = ['C', 'D', 'E', 'F', 'G', 'A', 'B']

    # C = C D E F G A B
    # C:  C E G      (root)
    # G7: G B D F
    # F:  F A C

    part = [
        [1,0,1,0,1,0,0,0,0,0,0], # A part
        [1,0,1,0,1,0,0,0,0,0,0], # A part

        [0,0,0,0,1,0,1,0,1,0,1], # B part
        [1,0,1,0,1,0,0,0,0,0,0] # A part
    ]
    DELAY = 0.75 # must be longer than any of the recorded notes plus a bit of overhead
    #TODO: could pre-validate length of all used wav files by doing get_length() on
    # each one when loading the driver class, and then asking via a method what the
    # shortest play duration is and validating against the timer setup. See above.

    set_scale(scale)
    timer = Timer(DELAY)
    i = 0

    while True:
        if timer.check():
            fingering = part[i]
            play_chord(scale, fingering)
            i = (i + 1) % len(part)

# END

