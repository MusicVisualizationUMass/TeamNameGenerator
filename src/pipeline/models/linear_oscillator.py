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
                 hook             = 1.0,
                 damping          = 0.9):

        super(ModelledRepr, self).__init__(sampleRate  = sampleRate,
                                           sampleRange = sampleRange,
                                           dataIn      = dataIn,
                                           parameters  = parameters)

        self.number_of_points = number_of_points
        # points contain N (pos, velocity) vectors.
        # force is calculated in real time
        self.points = zeros(shape = (number_of_points,2), 
                            dtype = float) # TODO: np.float64
        self.data_in_fps = dataInFPS
        self.fps  = sampleRate
        self.hook = hook    # hooks constant
        self.damping = damping # 0 = max damping; 1.0 = no damping

        # Set up data-in
        if dataIn == None:
            print("dataIn == None")
            def f():
                # Create a generator that sine stuff
                C = self.number_of_points / 2
                t = 0.0
                while t < 300:
                    t += 0.35
                    yield (C * sin(t) + C, cos(t))
                    

            print("Assigning dataIn")
            self.dataIn = iter(f())
        else:
            self.dataIn = iter(dataIn())

    def __iter__(self):
        dt          = 1.0 / self.fps          # delta t
        didt        = 1.0 / self.data_in_fps  # delta t for datain
        myTime      = 0.0  # Current time in simulation
        dataInTime  = 0.0  # Current time in data extraction
        hook   = self.hook
        N = self.number_of_points

        while True:
            points = self.points
            freq, amp = next(self.dataIn)
            print("freq = {}; amp = {}".format(int(freq), amp))
            points[int(freq)][1] += amp * dt   # acceleration * delta t
            print (dataInTime, myTime)

            # Update velocity of points
            A = zeros(shape = (self.number_of_points, 2), dtype = float)
            for i in range(N):  
                # TODO: Note that this can be made more efficient with fewer
                # references (2/iter instead of 3/iter...)

                y_l = points[i-1][0] 
                y   = points[i][0]
                y_r = points[ (i+1) % N][0]

                # TODO: Make this more accurate? This is just looking at the y
                # delta rather than doing the trig. More efficient BUT
                # innaccurate...
                F_l = hook * (y_l - y)  # Force Right
                F_r = hook * (y_r - y)  # Force Left
                F_v = -1 * hook * y     # Vertical Force
                delta_v = (F_l + F_r + F_v) * didt
                
                # Update the velocity, storing in A
                A[i][1] = (points[i][1] + delta_v)*self.damping
                # Update position
                A[i][0] += didt * points[i][1]
            # Now update the points locations
            dataInTime += didt
            if dataInTime > myTime:
                myTime += dt
                yield A

            # Now, update self.points to point at our new array of points
            self.points = A

        

