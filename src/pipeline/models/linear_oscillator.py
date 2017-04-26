'''
linear_oscillator.py: defines a ModelledRepr extension that begins with a
discretized line (i.e., n points) across the screen and is perturbed by pushing
the points up and down. Each point is connected to its neighbors by rubber band
and to its inital position by some other band. Thus at each point in time a
point is acted upon by force

        F = F_l + F_r + F_b

where F_l is the force acted upon it by
_______________________________________________________________ LINE
._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._. DISCRETIZED LINE

This will be the test case for the initial extension of ModelledRepr. We will
update/expand/tweak ModelledRepr based on this implementation to make further
extensions easier.
'''

from pipeline.ir import ModelledRepr
import numpy as np
from numpy import ndarray, full, zeros
from math import sin, cos, sqrt, atan, pi

# Don't know what we'll need...
from itertools import count, cycle, repeat

class LinearOscillatorModel(ModelledRepr):
    # TODO: include params for ModelledRepr

    def __init__(self, 
                 pir,                      # A Parametric Representation
                 sampleRate       = 24, 
                 sampleRange      = (None, None),
                 dataIn           = None, 
                 dataInFPS        = 48,
                 parameters       = None, 
                 number_of_points = 512,
                 hook             = 121.0,
                 data_shape       = (256,),
                 damping          = 0.95):
        '''
        sampleRate: number of samples per second to be _emmited_
        sampleRange: (min,max) of possible values
        dataIn: generator/iterator/array for input data. Expected to be 
                a list of aubio.cvecs.
        dataInFPS: number of samples per second that that dataIn is emitting
        parameters: dictionary of parameters to be passed in
        number_of_points: how many points on our line?
        hook: constant in Hooks Constant
        data_shape: (number of points in data, data item size)
        damping: multiplicative factor to dampen velocities
        '''


        shape = (number_of_points, 2)              # Shape of points
        self.number_of_points = number_of_points   # How many points in the line
        self.points = zeros(shape = shape, dtype = float)
        self.data_in_fps = dataInFPS  # Frames Per Second for input data
        self.fps        = sampleRate  # frames per second for OUR data
        self.hook       = hook        # hooks constant
        self.data_shape = data_shape
        self.damping    = damping     # 0 = max damping; 1.0 = no damping
        self.dataIn     = iter(pir)
        self.pir        = pir


        # Set up data-in

    def __iter__(self):
        '''Create an iterator that outputs data that is calculated from data
        input. Each instance in time outputs a line with (position, velocity)
        data. These are stored in a numpy array.
        '''

        dt          = 1.0 / self.fps          # delta t
        didt        = 1.0 / self.data_in_fps  # delta t for datain
        simTime     = 0.0  # Current time in simulation
        dataInTime  = 0.0  # Current time in data extraction
        hook        = self.hook
        N           = self.number_of_points
        damping     = self.damping
        dshape      = self.data_shape
        print( "Hook: {}, dt: {}, didt:{}, damping:{}".format(hook, dt, didt, damping))

        # A1: Current Data
        # A2: Working Copy

        A1 = self.points
        A2 = zeros(shape = (N, 2), dtype = float)
        while True:
            # This is an aubio.cvec and has data.norm and data.phas
            # These will both return vectors of complex values
            data = next(self.dataIn)
            data = zip(data.norm, data.phas)

            # First, update A1
            for i, (norm, phase)in enumerate(data):
                freq = int(10 * (N / (dshape[0] + 1)) * i) % N
                # print ("i = {}, freq = {}, val = {}".format(i, freq, val))
                # We update our current data's velocity at the appropriate place
                A1[freq][1] += 90 * cos(phase) * norm * didt   # velocity += acceleration * delta t


            # Update velocity of points
            for i in range(N):  

                # Get y_left, y_right and y position values
                y_l = A1[i-1][0] 
                y   = A1[ i ][0]
                y_r = A1[(i+1) % N][0]

                F_l = hook * (y_l - y)  # Force Right
                F_r = hook * (y_r - y)  # Force Left
                F_v = -0.15 * hook * y  # Vertical Force
                F = (F_l + F_r + F_v)

                delta_v = F * didt
                
                # Update the velocity, storing in A2
                A2[i][1] = (A1[i][1] + delta_v)*damping
                # Update position
                A2[i][0] = A1[i][0] + didt * A2[i][1]

            # Now update the points locations
            dataInTime += didt
            if dataInTime > simTime:
                simTime += dt
                # input("Yielding A2:\n{}".format( A2))
                yield A2

            # Now, update self.points to point at our new array of points
            # A1 = A2
            # A2 = zeros(shape = (self.number_of_points, 2), dtype = float)
            A1, A2 = A2, zeros(shape = (N, 2), dtype = float)
            # input()

    def get_frames(self, width = 720, height = 512):
        '''Return a list of numpy frames'''
        pt_list  = list(iter(self))
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
