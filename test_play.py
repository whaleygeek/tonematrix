# test the reliability/latency of multi channel mixing and play() in pygame

import pygame
import time

pygame.mixer.init()

note_names = ['C#', 'D#','F#','G#','A#']
notes = []
for name in note_names:
    note = pygame.mixer.sound("%s.wav" % name)
    notes.append(note)

while True:
    print("PLAY")
    for note in notes:
        note.play()
    print("PLAY END")

    time.sleep(1)

# END

