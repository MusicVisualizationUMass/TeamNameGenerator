'''
circular_oscillator.py: defines a ModelledRepr extension that begins with a
unit circle on the screen parametrized by (r, theta) = (1, [0,2pi))

This will be the test case for the initial extension of ModelledRepr. We will
update/expand/tweak ModelledRepr based on this implementation to make further
extensions easier.
'''

from musicvisualizer.pipeline.ir import ModelledRepr

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
