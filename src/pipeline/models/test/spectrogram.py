import sys, os.path
from aubio import pvoc, source, float_type
from numpy import zeros, log10, vstack
import matplotlib.pyplot as plt

def get_spectrogram(filename, samplerate = 0):
    win_s = 512                                        # fft window size
    hop_s = win_s // 2                                 # hop size
    fft_s = win_s // 2 + 1                             # spectrum bins

    a = source(filename, samplerate, hop_s)            # source file
    if samplerate == 0: samplerate = a.samplerate
    pv = pvoc(win_s, hop_s)                            # phase vocoder
    specgram = zeros([0, fft_s], dtype=float_type)     # numpy array to store spectrogram

    # analysis
    while True:
        samples, read = a()                              # read file
        specgram = pv(samples).norm   # store new norm vector
        if read < a.hop_size: 
            break
        print(specgram)
        input()
