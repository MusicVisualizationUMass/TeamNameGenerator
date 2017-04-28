#!/usr/bin/python3
from musicvisualizer.pipeline.models.linear_oscillator import LinearOscillatorModel
import matplotlib.pyplot as plt
#plt.style.use('ggplot')

if __name__ == '__main__':
    points = 1024

    def dataIn():
        print("CUSTOM DATA IN")
        t = 0.0
        MAXT = 30
        while t < MAXT:
            t += 0.1

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
            hook             = 11.0,
            dataIn           = None,
            damping          = 0.9999)

    I = iter(M)

    plt.ion()            # Interactive I/O
    

    for frame in I:
        ys = [ p[0] for p in frame]
        vs = [ p[1] for p in frame]
        xs = range(len(frame))
        # print("max(ys) = {}".format(max(ys)))
        # print("max(vs) = {}".format(max(vs)))
        ys = ys + [1.0, -1.0]
        xs = list(xs) + [0, 0]
        plt.scatter(xs, ys)
        plt.show()        # Update visuals
        plt.pause(0.02)    # Pause
        plt.cla()         # Clear 

