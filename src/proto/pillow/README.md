# PillowProto
This will be a spot to update anything we do that is worth knowing. Please
attribute to yourself whatever section you write so we can figure out who write
it!

## framegen.py
(author Ben Kushigian)

This basically just creates a 24 fps (frames per second) sequence of frames.
This uses numpy because the list operation in Python is sloooooooow. It has at
LEAST a 100x time improvement.

The basic interface is 

    f = FrameGenerator(...options...)
    iter(f)       # Get an iterator (computation time is spread out)
    list(f)       # Get a list; this will cause a hang in the program and
                  # need a lot of memory up front (though this might not be
                  # more than Pillow or PIL needs using an iter


