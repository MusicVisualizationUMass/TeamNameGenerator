'''
the breakdown is as follows: 
We first make a progenitor sandpile. It will affect the shape of the output the most.
Then a NxN array, called AN, is created. For every cell in AN we create a subScale*N sub-sandpile for each cell in the 
progenitor sandpile

the sandpiles in AN are then stitched together in a numpy array as the outputs

'''

from pipeline.ir import ModelledRepr
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from pipeline.sandpileAlt import Sandpile
import warnings


class SubSandpileModel(ModelledRepr):
    # TODO: include params for ModelledRepr

    def __init__(self,
                pir,                      # A Parametric Representation
                input_fields,             # Parameters
                sampleRate       = 24,
                sampleRange      = (None, None),
                dataInFPS        = 48,
                parameters       = None,
                subScale         = 0.5,      #0.0 < subScale < 1.0
                size             = 15,
                fill             = 10,
                data_shape       = (256,)):

        super(ModelledRepr, self).__init__(sampleRate=sampleRate,
                                           sampleRange=sampleRange,
                                           parameters=parameters)

        self.input_fields = input_fields
        self.verbose = 'verbose' in input_fields and input_fields['verbose']
        self.data_in_fps = dataInFPS  # Frames Per Second for input data
        self.fps = sampleRate  # frames per second for OUR data
        self.data_shape = data_shape
        self.size = size    #edge size of sandbox
        self.subScale = subScale
        self.subSize = int(size*subScale)   #0.0 < subScale < 1.0
        self.shape = (size*self.subSize, size*self.subSize)
        self.points = np.zeros(shape=self.shape, dtype=int)
        self.fill = fill
        self.dataIn = iter(pir)


    def __iter__(self):
        '''Create an iterator that outputs data that is calculated from data
        input. Each instance in time outputs a sandpile. These are stored in a numpy array.
        '''
        warnings.filterwarnings("ignore", ".*GUI is implemented.*")

        dt = 1.0 / self.fps  # delta t
        didt = 1.0 / self.data_in_fps  # delta t for datain
        size = self.size
        subSize = self.subSize
        output = np.zeros((size * self.subSize, size * self.subSize))
        print("didt:{}, dt:{}".format(didt, dt))

        pNxN = Sandpile(size, size, fill=self.fill) #progenitor sandpile, FILL VALUE IMPORTANT

        subCache = dict()
        maskCache = dict()
        norm = plt.Normalize(vmin=0.0, vmax= 4.0)

        AN = [[0]] * size  # instantiate NxN list to hold sandpiles
        for i in range(size):
            AN[i] = [0] * size

        while True:             
            data = next(self.dataIn)
            data_norm_max = int( norm(np.max((list(data.norm)))) )

            if data_norm_max > 0:
                print(data_norm_max)
                pNxN.check_over_flow_all()

                output = np.zeros((size * subSize, size * subSize))

                if not (max(max(list(pNxN))) > 4):
                    if data_norm_max in maskCache:
                        mask_sandpile = maskCache[data_norm_max]
                    else:
                        print("not in cache: ", data_norm_max)
                        maskCache[data_norm_max] = Sandpile(size, size, fill=data_norm_max) + Sandpile(size, size)
                        mask_sandpile = maskCache[data_norm_max]

                    pNxN = pNxN.addNoCheck(mask_sandpile)

                for i, row in enumerate(pNxN):
                    for j, col in enumerate(row):
                        cell = pNxN.table[i][j] + 3

                        # if cell value in subCache
                        if cell in subCache:
                            AN[i][j] = subCache[cell]
                        # else make it and add to subCache
                        else:
                            subCache[cell] = Sandpile(subSize, subSize, fill=cell) + Sandpile(subSize, subSize)
                            AN[i][j] = subCache[cell]

                for i, row in enumerate(AN):
                    for j, col in enumerate(row):
                        xOffset = j * subSize
                        yOffset = i * subSize
                        sandpile = list(AN[i][j])

                        for x in range(0, subSize):
                            for y in range(0, subSize):
                                output[x + xOffset][y + yOffset] = sandpile[x][y]
                yield (output)
            else:
                print("data_norm_max = 0, no audio")
                yield (output)

            #plt.imshow(output, interpolation='bicubic', aspect='auto')
            #plt.pause(0.01)  # Pause
            #plt.cla()  # Clear



    '''    
    def get_frames(self, width = 720, height = 512):
        frameList  = list(iter(self))
        #return frameList
    '''
