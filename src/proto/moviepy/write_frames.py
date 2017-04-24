from moviepy.editor import *
import proto.moviepy.framegen as fg

class FrameWriter(object):
    def __init__(self, frames, output = 'output.mp4'):
        self.output = output
        self.frames = frames

    def generate(self):
        isc = ImageSequenceClip(self.frames, fps = 24)
        isc.write_videofile('movie.mp4', fps=24)



if __name__ == '__main__':
    frames = fg.get_frames()
    fw = FrameWriter(frames)
    fw.generate()
