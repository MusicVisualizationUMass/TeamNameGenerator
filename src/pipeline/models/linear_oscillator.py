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

class LinearOscillatorModel(ModelledRepr):
    # TODO: include params for ModelledRepr

    def __init__(self, 
                 sampleRate       = 24, 
                 sampleRange      = (None, None),
                 dataIn           = None, 
                 dataInFPS        = 48,
                 parameters       = None, 
                 number_of_points = 1024,
                 hook             = 1.0):

        super(ModelledRepr, self).__init__(sampleRate  = sampleRate,
                                           sampleRange = sampleRange,
                                           dataIn      = dataIn,
                                           parameters  = parameters)

        self.number_of_points = number_of_points
        # points contain N (pos, velocity) vectors.
        # force is calculated in real time
        self.points = zeros(shape = (number_of_points,2), 
                            dtype = np.float64)
        self.data_in_fps = dataInFPS
        self.hook = hook    # hooks constant

        # Set up data-in
        if dataIn == None:
            print("dataIn == None")
            def f():
                # Create a generator that sine stuff
                C = self.number_of_points / 2
                t = 0.0
                while True:
                    t += 0.11
                    yield (C * sin(t) + C, cos(t))
                    

            print("Assigning dataIn")
            self.dataIn = iter(f())

    def __iter__(self):
        while True:
            ind, amp = next(self.dataIn)
            self.points[int(ind)] += amp
            A = ndarray(shape = self.number_of_points, buffer = self.points)
