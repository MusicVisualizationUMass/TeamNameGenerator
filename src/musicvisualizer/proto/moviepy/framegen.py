import numpy as np
from numpy import uint8, ndarray, full, zeros

class FrameGenerator(object):
    def __init__(self, fps = 24, duration = 60.0, width = 512,
                 height = 512, style = 'blink'):
        # TODO: Implement options
        self.fps = fps
        self.duration = duration
        self.total_frames = int(fps * duration)
        self.width = width
        self.height = height
        self.style = 'blink'   # Unused...
    
    def __iter__(self):
        frames = 0
        while frames < self.total_frames:
            frames += 1
            print("generating frame", frames, "of", self.total_frames)
            n = 256 - 10*(frames % self.fps)
            yield np.full(shape = (self.height, self.width, 3), 
                          dtype = uint8, fill_value = n)


def get_frames(fps = 24, duration = 60.0, width = 32, height = 32):
    f = FrameGenerator(fps = fps, duration = duration, width = width,
                       height = height)
    return list(f)

def get_frames_iter(fps = 24, duration = 60.0, width = 32, height = 32):
    f = FrameGenerator(fps = fps, duration = duration, width = width,
                       height = height)
    return iter(f)
