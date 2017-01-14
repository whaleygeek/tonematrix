# tones.py  20/10/2016  D.J.Whale
#
# A simple abstract interface to playing tones
# This is mainly to allow testing on a non pygame platform (while travelling!)

#----- CONFIG -----------------------------------------------------------------

# Time overhead to load notes to play a chord of a reasonable length
# Note, this is driver specific, and also changes with the number of notes
# in a chord. It is just an estimate at the moment, we might make this a
# bit cleverer later so we can find out a dynamic value based on the size
# of the scale loaded (worst case all notes playing, so it takes
# 5 loop iterations to start 5 notes playing)

NOTE_LOAD_OVERHEAD = 0.001

#----- PYGAME TONE ------------------------------------------------------------

class PygameTone():
    """A tone player driver that uses PyGame"""

    def __init__(self, note_names):
        self.note_names = note_names

        # Init the sound driver
        import pygame
        pygame.mixer.pre_init(22050, -16, 2, 4096)
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
        self.max_length = 0 #max_length
        self.min_length = min_length

        self.tests = [
            [notes[0]],
            [notes[1]],
            [notes[2]],
            [notes[3]]
        ]
        self.testidx = 0

    def get_longest_time(self):
        """Get the longest length of any note/wav file"""
        return self.max_length

    def play_chord(self, fingering):
        print(fingering)
        sounds = []
        for ni in range(len(fingering)):
            if fingering[ni] == 1:
                sounds.append(self.notes[ni])
        for note in sounds:
            note.play()

#----- DUMMY TONE -------------------------------------------------------------

class DummyTone():
    """A tone player driver, that just prints the notes it would play"""

    def __init__(self, note_names):
        pass

    def play_chord(self, fingering):
        print("play_chord:%s" % str(fingering))

    def get_longest_time(self):
        """Get the longest time (and hence fastest BPM) tolerable"""
        return 0.1 # 0.5 second, this is just for testing
        # we can use this to test that a warning occurs and BPM message
        # rejected if it would cause glitching on playback


#----- STATE ------------------------------------------------------------------

scale = None
driver = None


#------------------------------------------------------------------------------

def set_scale(scale_data):
    global scale, driver
    scale = scale_data
    #driver = DummyTone(scale) #TESTING
    driver = PygameTone(scale) #REAL
    
def get_longest_time():
    """Get the time duration in seconds of the longest .wav file in the scale.
        This is the longest time (and hence related to the fastest BPM achievable without glitching)
    """
    return driver.get_longest_time()

def get_fastest_BPM():
    """Get the fastest BPM tolerable without glitching"""
    lt = get_longest_time() + NOTE_LOAD_OVERHEAD

    fastest_bpm = 60.0 / lt
    return fastest_bpm

def play_chord(scale, fingering_mask):
    ##print("play_chord: %s with fingering_mask %s" % (str(scale), str(fingering_mask)))

    # build the fingered chord from the scale
    #TODO the fingering needs to be cached so that we don't keep regenerating it each call.
    #use a memoize pattern here
    #Also want the tones module to memoize, so that it uses a fast-lookup that maps to actual sound objects
    #chord = []
    #for i in range(len(scale)):
    #    if fingering_mask[i] == 1:
    #        chord.append(scale[i])

    ##import time
    ##print(time.time())
    driver.play_chord(fingering_mask)


#----- TEST HARNESS -----------------------------------------------------------

if __name__ == "__main__":
    from Timer import Timer

    scale = ['C', 'D', 'E', 'F', 'G', 'A', 'B']

    # C = C D E F G A B
    # C:  C E G      (root)
    # G7: G B D F
    # F:  F A C

    part = [
        [1,0,1,0,1,0,0,0,0,0,0], # A part
        [1,0,1,0,1,0,0,0,0,0,0], # A part

        [0,0,0,0,1,0,1,0,1,0,1], # B part
        [1,0,1,0,1,0,0,0,0,0,0]  # A part
    ]
    DELAY = 0.75 # must be longer than any of the recorded notes plus a bit of overhead

    set_scale(scale)
    timer = Timer(DELAY)
    i = 0

    while True:
        if timer.check():
            fingering = part[i]
            play_chord(scale, fingering)
            i = (i + 1) % len(part)

# END

