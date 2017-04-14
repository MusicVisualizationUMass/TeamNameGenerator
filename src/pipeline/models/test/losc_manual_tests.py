#!/usr/bin/python3
from pipeline.models.linear_oscillator import LinearOscillatorModel as LOM
import matplotlib.pyplot as plt

if __name__ == '__main__':
    points = 200

    def dataIn():
        print("CUSTOM DATA IN")
        for i in range(10000):
            print("time =", i)
            if i % 200 == 0:
                yield (100, 0.1)
            else:
                yield (0,0)

    M = LOM(sampleRate = 1,   # Visual sample rate
            dataInFPS  = 1,   # Data sample rate (to generate visual)
            number_of_points = points, # Points to view
            hook             = 1.0,
            dataIn           = dataIn)

    I = iter(M)
    l = list(I) # [ [pt0_pos, pt0_vel]
                #   [pt1_pos, pt1_vel],
                #   [pt2_pos, pt3_vel],
                #   [pt3_pos, pt3_vel],
                #   [pt4_pos, pt4_vel],
                #          . . .      ,
                #   [ptn_pos, ptn_vel]]

    plt.ion()
    plt.ylim(-2., 2.)
    for frame in l:
        ys = [ p[0] for p in frame]
        xs = range(len(frame))
        plt.scatter(xs, ys)
        plt.show()
        plt.pause(0.10)
        plt.cla()

