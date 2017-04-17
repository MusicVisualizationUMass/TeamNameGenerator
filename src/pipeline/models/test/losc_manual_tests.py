#!/usr/bin/python3
from pipeline.models.linear_oscillator import LinearOscillatorModel
import matplotlib.pyplot as plt

if __name__ == '__main__':
    points = 1024

    def dataIn():
        print("CUSTOM DATA IN")
        for i in range(1000):
            print("time =", i)
            if i % 200 == 0:
                yield (points/2, 12)
            else:
                yield (0,0)
    def dataIn_empty():
        for i in range(1000):
            yield (0.0, 0.0)
    def dataIn_singlePulse():
        yield(points/2, 20)
        for i in range(1000):
            yield (0.0, 0.0)

    M = LinearOscillatorModel(
            sampleRate       = 24,      # Visual sample rate
            dataInFPS        = 96,      # Data sample rate (to generate visual)
            number_of_points = points,  # how many points in simulation?
            hook             = 21.0,
            dataIn           = None,
            damping          = 0.999)

    I = iter(M)
#    l = list(I) # [ [pt0_pos, pt0_vel]
#                #   [pt1_pos, pt1_vel],
#                #   [pt2_pos, pt3_vel],
#                #   [pt3_pos, pt3_vel],
#                #   [pt4_pos, pt4_vel],
#                #          . . .      ,
#                #   [ptn_pos, ptn_vel]]
#
    plt.ion()            # Interactive I/O
    

    for frame in I:
        ys = [ p[0] for p in frame]
        vs = [ p[1] for p in frame]
        xs = range(len(frame))
        # print("max(ys) = {}".format(max(ys)))
        # print("max(vs) = {}".format(max(vs)))
        ys = ys + [0.1, -0.1]
        xs = list(xs) + [0, 0]
        plt.scatter(xs, ys)
        plt.show()        # Update visuals
        plt.pause(0.02)    # Pause
        plt.cla()         # Clear 

