'''
the breakdown is as follows: 
First a NxN array, called AN, is created, then for every cell in AN we create a subScale*N sub-sandpile. 


When making A10, it will have an initial value equal to its progenitor cell in all cells of A10. The value g is then added to every cell of A10
g = (highest value in A20) - (lowest value in A20)

A 20x20 numpy array will hold every instance of A10 in its corresponding cell. The output will then be a visualization of every A10 sandpile stitched together.
'''

from pipeline.ir import ModelledRepr
import numpy as np
import matplotlib.pyplot as plt
from pipeline.sandpileAlt import Sandpile
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
        input. Each instance in time outputs a line with (position, velocity)
        data. These are stored in a numpy array.
        '''
        warnings.filterwarnings("ignore", ".*GUI is implemented.*")

        dt = 1.0 / self.fps  # delta t
        didt = 1.0 / self.data_in_fps  # delta t for datain
        size = self.size
        subSize = self.subSize
        print("size: {}, subSize: {}, didt:{}, dt:{}".format(size, subSize, didt, dt))

        while True:
            data = next(self.dataIn)

            size = int(np.random.randint(8,20))
            subSize = int(size * self.subScale)
            print("size: {}, mean: {}".format(size, np.mean(data)))

            output = np.zeros((size * subSize, size * subSize))

            p20x20 = Sandpile(size, size, fill=4)
            p20x20 = p20x20 + Sandpile(size, size)

            g = max(max(list(p20x20))) - min(min(list(p20x20)))     #largest value in the sandpile minus the smallest
            AN = [[0]] * size     #instantiate NxN list
            for i in range(size):
                AN[i] = [0] * size

            for i, row in enumerate(p20x20):
                for j, col in enumerate(row):
                    AN[i][j] = (Sandpile(subSize, subSize, fill=p20x20.table[i][j] + g) + Sandpile(subSize, subSize))

            for i, row in enumerate(AN):
                for j, col in enumerate(row):
                    xOffset = j * subSize - 1
                    yOffset = i * subSize - 1
                    sandpile = list(AN[i][j])

                    for x in range(0, subSize):
                        for y in range(0, subSize):
                            output[x + xOffset][y + yOffset] = sandpile[x][y]
            yield (output)


#fig = plt.imshow(output)
#plt.axis('off')
#fig.axes.get_xaxis().set_visible(False)
#fig.axes.get_yaxis().set_visible(False)
#plt.show()

#plt.matshow(output,)
#start = time.time()
#end = time.time()
#print("time: {}".format(end - start))
