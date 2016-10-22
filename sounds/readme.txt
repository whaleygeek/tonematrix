Tones C-B with sharps were generated using the 'pluck'
generator in Audacity. Thus they are royalty free.

They all have precisely the same play length, intentionally.

The chord playback engine works better if all notes are the same length,
otherwise you might have your BPM limited by the code to prevent
glitching in playback. 

i.e. if you try to load 5 0.5s notes every 0.5s, the loop overhead of 
triggering  the playback is finite but non zero.

e.g. 0.5s later the previous notes are still playing and you try to
load them again (the playback engine then blocks until the existing notes
stop playing), and you get a 'hiccup' in the sound playback as a result.

