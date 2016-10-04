# test the reliability/latency of multi channel mixing and play() in pygame

import pygame
import time

pygame.mixer.init()

note_names = ["C", "E", "G"]
notes = []
for name in note_names:
    note = pygame.mixer.Sound("sounds/%s.wav" % name)
    notes.append(note)

from Timer import Timer

timer = Timer(0.75)

while True:
    if timer.check():
        #TODO: if any sounds are still playing, that is bad
        #if sound length is 0.5, need timer to be slightly longer
        #else sounds will sometimes double queue up and you get
        #an extra beat, due to python being a bit slow
        print("PLAY")
        for note in notes:
            note.play()
        print("PLAY END")


# END

