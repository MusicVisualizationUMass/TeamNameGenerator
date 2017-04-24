from moviepy.editor import *
from moviepy.video.tools.drawying import color_split
import proto.moviepy.framegen as fg

class FrameWriter(object):
    def __init__(self, frames, output = 'output.mp4'):
        self.output = output
        self.frames = frames

    def generate(self):
        isc = ImageSequenceClips(self.frames, fps = 24)



