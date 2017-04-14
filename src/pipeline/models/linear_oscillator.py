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

class CircularOscillatorModel(ModelledRepr):
    # TODO: include params for ModelledRepr

    def __init__(self, 
                 sampleRate       = 24, 
                 sampleRange      = (None, None),
                 dataIn           = None, 
                 parameters       = None, 
                 number_of_points = 1024):

        super(ModelledRepr, self).__init__(sampleRate  = sampleRate,
                                           sampleRange = sampleRange,
                                           dataIn      = dataIn,
                                           parameters  = parameters)

        self.number_of_points = number_of_points
        self.points = [0.0 for i in range(self.number_of_points)]

    def increment_time(self):
        pass
