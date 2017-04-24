'''
the breakdown is as follows: 
We first make a progenitor sandpile. It will affect the shape of the output the most.
Then a NxN array, called AN, is created. For every cell in AN we create a subScale*N sub-sandpile for each cell in the 
progenitor sandpile

the sandpiles in AN are then stitched together in a numpy array as the output

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
                subScale          = 0.5,      #0.0 < subScale < 1.0
                size             = 15,
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
        print("didt:{}, dt:{}".format(didt, dt))

        
        sizeList = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
        n=0
        while True:
            start = time.time()

            data = next(self.dataIn)

            size = sizeList[n]
            subSize = int(size * self.subScale)
            n+=1

            output = np.zeros((size * subSize, size * subSize))

            pNxN = Sandpile(size, size, fill=4)
            pNxN = pNxN + Sandpile(size, size)

            g = max(max(list(pNxN))) - min(min(list(pNxN)))     #largest value in the sandpile minus the smallest
            AN = [[0]] * size     #instantiate NxN list
            for i in range(size):
                AN[i] = [0] * size

            for i, row in enumerate(pNxN):
                for j, col in enumerate(row):
                    AN[i][j] = (Sandpile(subSize, subSize, fill=pNxN.table[i][j] + g) + Sandpile(subSize, subSize))

            for i, row in enumerate(AN):
                for j, col in enumerate(row):
                    xOffset = j * subSize 
                    yOffset = i * subSize 
                    sandpile = list(AN[i][j])

                    for x in range(0, subSize):
                        for y in range(0, subSize):
                            output[x + xOffset][y + yOffset] = sandpile[x][y]

            end = time.time()
            print("size: {}, time: {}".format(size, end-start))
            if n==14: n=0
            yield(output)


#fig = plt.imshow(output)
#plt.axis('off')
#fig.axes.get_xaxis().set_visible(False)
#fig.axes.get_yaxis().set_visible(False)
#plt.show()

#plt.matshow(output,)
#start = time.time()
#end = time.time()
#print("time: {}".format(end - start))
