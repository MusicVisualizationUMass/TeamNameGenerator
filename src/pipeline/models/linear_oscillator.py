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
from math import sin, cos

# Don't know what we'll need...
from itertools import count, cycle, repeat

DEBUG = False

class LinearOscillatorModel(ModelledRepr):
    # TODO: include params for ModelledRepr

    def __init__(self, 
                 sampleRate       = 24, 
                 sampleRange      = (None, None),
                 dataIn           = None, 
                 dataInFPS        = 48,
                 parameters       = None, 
                 number_of_points = 1024,
                 hook             = 1.0,
                 data_shape       = (256,),
                 damping          = 0.9):
        '''
        sampleRate: number of samples per second to be _emmited_
        sampleRange: (min,max) of possible values
        dataIn: generator/iterator/array for input data of the form (p_1, p_2).
        dataInFPS: number of samples per second that that dataIn is emitting
        parameters: dictionary of parameters to be passed in
        number_of_points: how many points on our line?
        hook: constant in Hooks Constant
        data_shape: (number of points in data, data item size)
        damping: multiplicative factor to dampen velocities
        '''

        super(ModelledRepr, self).__init__(sampleRate  = sampleRate,
                                           sampleRange = sampleRange,
                                           dataIn      = dataIn,
                                           parameters  = parameters)

        shape = (number_of_points, 2)              # Shape of points
        self.number_of_points = number_of_points   # How many points in the line
        self.points = zeros(shape = shape, dtype = float)
        self.data_in_fps = dataInFPS  # Frames Per Second for input data
        self.fps        = sampleRate  # frames per second for OUR data
        self.hook       = hook        # hooks constant
        self.data_shape = data_shape
        self.damping    = damping     # 0 = max damping; 1.0 = no damping

        # Set up data-in
        if dataIn == None:
            
            def f():
                # Create a generator that sine stuff
                C = self.number_of_points / 2
                N = self.number_of_points / 2
                n = 0
                dshape = self.data_shape
                while n < 1000:
                    print("n = {}".format( n))
                    A = zeros(shape = dshape, dtype=float)
                    A[n % data_shape[0]] = 100.0
                    n += 1
                    yield(A)
                A = zeros(shape = dshape, dtype = float)
                while n < 2000:
                    yield(A)

            self.dataIn = iter(f())
        else:
            # XXX: This might break! See how data will be passed in...
            self.dataIn = iter(dataIn())

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
            if DEBUG:
                print("A1:\n{}".format(A1))
                print("A2:\n{}".format(A2))
            data = next(self.dataIn)

            # First, update A1
            for i, val in enumerate(data):
                freq = int(10 * (N / (dshape[0] + 1)) * i) % N
                # print ("i = {}, freq = {}, val = {}".format(i, freq, val))
                # We update our current data's velocity at the appropriate place
                A1[freq][1] += val * didt   # velocity += acceleration * delta t


            # Update velocity of points
            for i in range(N):  

                # Get y_left, y_right and y position values
                y_l = A1[i-1][0] 
                y   = A1[ i ][0]
                y_r = A1[(i+1) % N][0]

                F_l = hook * (y_l - y)  # Force Right
                F_r = hook * (y_r - y)  # Force Left
                F_v = -0.15 * hook * y     # Vertical Force
                F = (F_l + F_r + F_v)

                delta_v = F * didt
                
                # Update the velocity, storing in A2
                A2[i][1] = (A1[i][1] + delta_v)*damping
                if DEBUG:
                    print("A2[{}] = {}".format(i, A2[i]))
                # Update position
                A2[i][0] = A1[i][0] + didt * A2[i][1]
                if DEBUG:
                    print("A2[{}] = {}".format(i, A2[i]))

                if DEBUG:
                    print("i = {}".format(i), A2[i])
                    print("v = {}".format(A2[i][1]), "delta_v = {}".format(delta_v))
                    print("y: {0:7.4f}, {1:7.4f}, {2:7.4f}\n".format(y_l, y, y_r),
                          "F: {0:7.4f}, {1:7.4f}, {2:7.4f}".format(F_l, F_v, F_r))

            # Now update the points locations
            dataInTime += didt
            if dataInTime > simTime:
                simTime += dt
                # input("Yielding A2:\n{}".format( A2))
                yield A2

            # Now, update self.points to point at our new array of points
            # A1 = A2
            # A2 = zeros(shape = (self.number_of_points, 2), dtype = float)
            A1, A2 = A2, A1
            # input()
