'''
the breakdown is as follows: 
We first make a progenitor sandpile. It will affect the shape of the output the most.
Then a NxN array, called AN, is created. For every cell in AN we create a subScale*N sub-sandpile for each cell in the 
progenitor sandpile

the sandpiles in AN are then stitched together in a numpy array as the outputs

'''

from ir import ModelledRepr
import numpy as np
import matplotlib.pyplot as plt
from sandpileAlt import Sandpile
import warnings
import time


class SubSandpileModel(ModelledRepr):
    # TODO: include params for ModelledRepr

    def __init__(self,
                sampleRate       = 24,
                sampleRange      = (None, None),
                dataIn           = None,
                dataInFPS        = 48,
                parameters       = None,
                subScale         = 0.5,      #0.0 < subScale < 1.0
                size             = 15,
                fill             = 10,
                data_shape       = (256,)):

        super(ModelledRepr, self).__init__(sampleRate=sampleRate,
                                           sampleRange=sampleRange,
                                           dataIn=dataIn,
                                           parameters=parameters)
        self.data_in_fps = dataInFPS  # Frames Per Second for input data
        self.fps = sampleRate  # frames per second for OUR data
        self.data_shape = data_shape
        self.size = size    #edge size of sandbox
        self.subScale = subScale
        self.subSize = int(size*subScale)   #0.0 < subScale < 1.0
        self.shape = (size*self.subSize, size*self.subSize)
        self.points = np.zeros(shape=self.shape, dtype=int)
        self.fill = fill

        # Set up data-in
        if dataIn == None:

            def f():

                # Create a generator that sine stuff
                C = self.number_of_points / 2
                N = self.number_of_points / 2
                n = 0
                dshape = self.data_shape
                while n < 1000:
                    print("n = {}".format(n))
                    A = np.zeros(shape=dshape, dtype=float)
                    A[n % data_shape[0]] = 100.0
                    n += 1
                    yield (A)
                A = np.zeros(shape=dshape, dtype=float)
                while n < 2000:
                    yield (A)

            self.dataIn = iter(f())
        else:
            # XXX: This might break! See how data will be passed in...
            self.dataIn = iter(dataIn())


    def __iter__(self):
        '''Create an iterator that outputs data that is calculated from data
        input. Each instance in time outputs a sandpile. These are stored in a numpy array.
        '''
        warnings.filterwarnings("ignore", ".*GUI is implemented.*")

        dt = 1.0 / self.fps  # delta t
        didt = 1.0 / self.data_in_fps  # delta t for datain
        size = self.size
        subSize = self.subSize
        print("didt:{}, dt:{}".format(didt, dt))

        pNxN = Sandpile(size, size, fill=self.fill) #progenitor sandpile, FILL VALUE IMPORTANT

        cache = dict()
        for i in range(1,9):
            cache[i] = Sandpile(subSize,subSize, fill=i+3) + Sandpile(subSize, subSize)

        while True:             
            start = time.time()
            data = next(self.dataIn)

            output = np.zeros((size * subSize, size * subSize))

            pNxN.check_over_flow_all()
            
            #g = max(max(list(pNxN))) - min(min(list(pNxN)))     #largest value in the sandpile minus the smallest


            AN = [[0]] * size           #instantiate NxN list to hold sandpiles
            for i in range(size):
                AN[i] = [0] * size

            for i, row in enumerate(pNxN):
                for j, col in enumerate(row):
                    cell = pNxN.table[i][j] + 3

                    #if cell_g value not in cache
                    if cell in cache:
                        AN[i][j] = cache[cell]
                    #else make it and add to cache
                    else:
                        cache[cell] = Sandpile(subSize, subSize, fill=cell) + Sandpile(subSize, subSize)
                        AN[i][j] = cache[cell]

            for i, row in enumerate(AN):
                for j, col in enumerate(row):
                    xOffset = j * subSize 
                    yOffset = i * subSize 
                    sandpile = list(AN[i][j])

                    for x in range(0, subSize):
                        for y in range(0, subSize):
                            output[x + xOffset][y + yOffset] = sandpile[x][y]
            yield(output)

            #end = time.time()
            #print("size: {}, time: {}".format(size, end-start))


#fig = plt.imshow(output)
#plt.axis('off')
#fig.axes.get_xaxis().set_visible(False)
#fig.axes.get_yaxis().set_visible(False)
#plt.show()

#plt.matshow(output,)
#start = time.time()
#end = time.time()
#print("time: {}".format(end - start))
