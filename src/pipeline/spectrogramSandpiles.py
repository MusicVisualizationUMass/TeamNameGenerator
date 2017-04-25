from aubio import pvoc, source, float_type
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from pipeline.models.SandPlot import SubSandpileModel

from tkinter import *
from PIL import Image, ImageTk
import moviepy

from sys import argv

def plot_spectrogram(filename, samplerate = 0):
    foo = []
    points = 512 
    win_s  = 512                                        # fft window size
    hop_s  = win_s // 2                                 # hop size
    fft_s  = win_s // 2 + 1                             # spectrum bins

    a = source(filename, samplerate, hop_s)            # source file

    if samplerate == 0: 
        samplerate = a.samplerate
    pv = pvoc(win_s, hop_s)                            # phase vocoder
    specgram = np.zeros([0, fft_s], dtype=float_type)     # numpy array to store spectrogram

    while False:   # Set to true for interpreter
        s = input('>>> ').strip()
        if s.lower() in ('x', 'q', 'quit', 'exit', 'break'):
            break
        try:
            exec(s)
        except Exception as e:
            print(e)

    # Set up Sandpiles
    def dataIn():
        while True:
            samples, read = a()                              # read file
            specgram = pv(samples).norm   # store new norm vector
            if read < a.hop_size: 
                break
            yield(specgram)
        
    M = SubSandpileModel(
            sampleRate       = 24,      # Visual sample rate
            dataInFPS        = 24,      # Data sample rate (to generate visual)
            dataIn           = dataIn,
            data_shape       = (256, ),
            size             = 5,
            subScale         = 0.5,
            fill             = 10)

    I = iter(M)

    plt.ion()            # Interactive I/O

    for frame in I:
        plt.imshow(frame, interpolation='bilinear', aspect='auto')
        plt.axis('off')

        # save the image
        plt.savefig('buffer.png')

        plt.show()
        plt.pause(0.1)    # Pause
        plt.cla()         # Clear 

if __name__ == '__main__':
    if len(argv) == 1:
        plot_spectrogram('../media/440Hz_With_660Hz-Pulse.wav', samplerate = 0)
    else:
        plot_spectrogram(argv[1], samplerate = 0)
