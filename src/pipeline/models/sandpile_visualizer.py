from pipeline.ir import ModelledRepr, VisualizableMixin
import numpy as np
from matplotlib import cm as cm, pyplot as plt, colors
from math import atan, pi       # arctan normalizes


class SubSandpileVisualizer(VisualizableMixin):
    def __init__(self, sandpile_model):
        self.model = sandpile_model
        self.n = 0

    def make_frame(self, frame, cmap=None, norm = None):
        '''Create a width x height x 3 ndarray'''

        #width, height = self.width, self.height
        width, height = len(frame), len(frame)
        size = len(frame)   #self.model.size
        A = np.zeros(shape=( height, width, 3), dtype=np.uint8 )

        h, w = 0, 0    # How far have we tiled our _output_?
        # Get scaling factors for height and width
        hsf, wsf = height // size, width // size # height scaling factor, etc
        for i in range(size): # traverse top to bottom
            for j in range(size): # traverse left to right
            # The following line _normalizes_ our input from 0 < val < ???
            # to 0 <= val <= 255, and gives it type int.
                val = int(255 * (2/pi)*atan(frame[i][j]))
                for y in range(hsf):
                    for x in range(wsf):
                        #val_c = cmap(val)
                        #print("val2[0] =", val_c[0], "val2[1] =", val_c[1],"val2[2] =", val_c[2])
                        A[h + y][w + x][0] = val   # Red
                        A[h + y][w + x][1] = val   # Green
                        A[h + y][w + x][2] = val   # Blue
                w += wsf
            h += hsf
            w = 0
        print("n: ", self.n)
        self.n+=1
        return A

    def visualize(self, width = 720, height = 512):
        self.width, self.height = width, height
        result = []

        cmap = cm.get_cmap('jet')
        norm = colors.Normalize(vmin=0.0, vmax=255.0)

        I = list(iter(self.model))
        for frame in I:
            '''
            plt.imshow(frame, interpolation='bilinear', aspect='auto')
            plt.pause(0.01)  # Pause
            plt.cla()  # Clear
            '''
            result.append(self.make_frame(frame=frame, cmap=cmap, norm=norm))

        return result


