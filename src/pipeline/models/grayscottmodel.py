'''
grayscottmodel.py: simulate Gray Scott model of reaction diffusion
'''

from pipeline.ir import ModelledRepr
from scipy.ndimage.filters import laplace
from math import sin, cos, pi
import numpy as np

''' 
grayscott.py:
A sample simulation of the grayscott diffusion equations. This doesn't run
fast and it isn't a great set of params (and it may not run correctly either :D)
but it _runs_, and that's the important bit!

The equations are written about here:
    https://groups.csail.mit.edu/mac/projects/amorphous/GrayScott/

You will need the modules:
    scipy/numpy (via pip3)
    matplotlib  (via pip3)
    tkinter     (I had to install with sudo apt-get... no pip from what I could
                 tell...)

author: ben kushigian
date:   4/10/2017

'''

class GrayScottModel(ModelledRepr):
    def __init__(self, width = 80, height = 80, k = 1.0, ru = 0.1, rv = 0.1, 
                                                f = 0.2, dt = 0.01):
        self.dt     = dt
        self.t      = 0.0
        self.height = height
        self.width  = width
        self.shape  = (self.height, self.width)
        self.k      = k
        self.ru     = ru
        self.rv     = rv
        self.f      = f

        # Start with some periodic initial configuration -- this should be
        # modified and possibly controlled through some interface
        self.us = [ [(1 + cos(2*pi*x / width ) * sin(2*pi*y/height))/2 for x in range(width)] for y in range(height)]
        self.vs = [ [(1 + cos(2*pi*y / height) * sin(2*pi*x/width ))/2 for x in range(width)] for y in range(height)]

        self.lapl_u = np.zeros(self.shape)  # Laplacian of us; init to zeros
        self.lapl_v = np.zeros(self.shape)  # Laplacian of vs; init to zeros

    def increment_time(self):
        self.lapl_u = laplace(self.us)     # Laplace of us
        self.lapl_v = laplace(self.vs)     # Laplace of vs
        delta_us, delta_vs = self.calculate_deltas()
        dt = self.dt
        self.t += dt
        for i in range(self.height):
            for j in range(self.width):
                self.us[i][j] += dt * delta_us[i][j]
                self.vs[i][j] += dt * delta_vs[i][j]



    def calculate_deltas(self):
        '''Calculate full array of the du/dt'''
        result_u = np.zeros(self.shape)
        result_v = np.zeros(self.shape)
        ru, rv, f, k = self.ru, self.rv, self.f, self.k
        lapl_u, lapl_v = self.lapl_u, self.lapl_v
        us, vs = self.us, self.vs
        for i in range(self.height):
            for j in range(self.width):
                u, v = us[i][j], vs[i][j]
                result_u[i][j] = ru * lapl_u[i][j] - u * v * v + f * (1 - u)
                result_v[i][j] = rv * lapl_v[i][j] + u * v * v - (f + k) * v
        return result_u, result_v



