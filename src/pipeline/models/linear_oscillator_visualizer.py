from pipeline.ir import VisualizableMixin
from numpy import zeros
import numpy as np
from math import sin, cos, atan, pi

class LinearOscillatorVisualizer(VisualizableMixin):
    def __init__(self, linear_oscillator):
        self.losc = linear_oscillator

    def visualize(self, width = 720, height = 512):
        '''Return a list of numpy frames'''
        pt_list  = list(iter(self.losc))
        pt_width = len(pt_list[0])      # width of each points instance

        if pt_width > len(pt_list[0]):
            raise Exception('width of video must be greater than width of points')

        result   = []

        for points in pt_list:
            arr = zeros(shape = (height, width, 3), dtype=np.uint8)
            for i, (point, vel) in enumerate(points):
                # Weird offsets are to allow a 2x2 pixel (+/- 1...)
                x = int(i * (width-2) / pt_width + 2)
                # HEY! So the following y value works like this:
                #  -pi/2 <= arctan(x) <= pi/2, so dividing out by pi we get
                # -1/2 <= arctan(x) / pi <= 1/2, and the result below is that
                # we get a value between 0 and height
                y = int( (height / 2) + atan(5.0 * point) * (height)/ (pi))
                if y >= height - 1:
                    y = height - 2
                if y < 1:
                    y = 1
                arr[y][x][0]     = 255
                arr[y-1][x][0]   = 255
                arr[y-2][x][0]   = 255
                arr[y][x-1][0]   = 255
                arr[y-1][x-1][0] = 255
                arr[y-2][x-1][0] = 255
                arr[y][x-2][0]   = 255
                arr[y-1][x-2][0] = 255
                arr[y-2][x-2][0] = 255

                arr[y][x][1]     = 255
                arr[y-1][x][1]   = 255
                arr[y-2][x][1]   = 255
                arr[y][x-1][1]   = 255
                arr[y-1][x-1][1] = 255
                arr[y-2][x-1][1] = 255
                arr[y][x-2][1]   = 255
                arr[y-1][x-2][1] = 255
                arr[y-2][x-2][1] = 255

                arr[y][x][2]     = 255
                arr[y-1][x][2]   = 255
                arr[y-2][x][2]   = 255
                arr[y][x-1][2]   = 255
                arr[y-1][x-1][2] = 255
                arr[y-2][x-1][2] = 255
                arr[y][x-2][2]   = 255
                arr[y-1][x-2][2] = 255
                arr[y-2][x-2][2] = 255

            result.append(arr)
        return result
        
        
