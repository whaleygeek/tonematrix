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
        pass#print(str(chord))


scale = ['C', 'C#', 'D', 'D#', 'E', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'C']
driver = DummyTone(scale)

def play_chord(chord):
    print("play_chord: %s" % str(chord))
    driver.play_chord(chord)


#----- TEST HARNESS -----------------------------------------------------------

if __name__ == "__main__":
    # C = C D E F G A B
    # C:  C E G
    # B7: B D F A
    # A:  A D E
    sequence = [
        ['C',  'E',  'G'],      # A part
        ['C',  'E',  'G'],      # A part
        ['B',  'D',  'F', 'A'], # B part
        ['C',  'E',  'G'],      # A part
    ]
    DELAY = 0.75 # must be longer than any of the recorded notes plus a bit of overhead
    #TODO: could pre-validate length of all used wav files by doing get_length() on
    # each one when loading the driver class, and then asking via a method what the
    # shortest play duration is and validating against the timer setup.

    timer = Timer(DELAY)
    i = 0

    while True:
        if timer.check():
            play_chord(sequence[i])
            i = (i + 1) % len(sequence)

# END

