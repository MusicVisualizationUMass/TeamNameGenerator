from pipeline.ir import ModelledRepr, VisualizableMixin
import numpy as np
import matplotlib.pyplot as plt
from math import atan, pi       # arctan normalizes
#from moviepy.editor import *
from PIL import Image

class SubSandpileVisualizer(VisualizableMixin):
    def __init__(self, sandpile_model):
        self.model = sandpile_model

    def make_frame(self, frame):
        '''Create a width x height x 3 ndarray'''
        width, height = self.width, self.height
        size = self.model.size
        A = np.zeros(shape=( height, width, 3), dtype=np.uint8 )
        h, w = 0, 0    # How far have we tiled our _output_?
        # Get scaling factors for height and width
        hsf, wsf = height // size, width // size # height scaling factor, etc
        for i in range(size): # traverse top to bottom
            for j in range(size): # traverse left to right
            # The following line _normalizes_ our input from 0 < val < ???
            # to 0 <= val <= 255, and gives it type int.
                #print ("frame[i][j] =", frame[i][j])
                val = int(255 * (2/pi)*atan(frame[i][j])) #     ^          ^     ^ #     |          |     atan ranges from 0 to pi/2
                #     |          ranges from 0 to 1 
                #     ranges from 0 to 255
                for y in range(hsf):
                    for x in range(wsf):
                        A[h + y][w + x][0] = val   # Red
                        A[h + y][w + x][1] = val   # Green 
                        A[h + y][w + x][2] = val   # Blue
                w += wsf
            h += hsf
            w = 0

        return A

    def visualize(self, width = 100, height = 100):
        self.width, self.height = width, height
        result = []

        #I = list(iter(self.model))
        I = iter(self.model)
        for frame in I:
            result.append(self.make_frame(frame))

        #isc = ImageSequenceClip(result, fps = 24)
        #isc.write_videofile('movie.mp4', fps=24)

        return result


