from aubio import pvoc, source, float_type
from numpy import zeros, log10, vstack
import matplotlib.pyplot as plt
from musicvisualizer.pipeline.models.linear_oscillator import LinearOscillatorModel
from sys import argv
from moviepy.editor import *

def plot_spectrogram(filename, samplerate = 0):
    points = 128 
    win_s  = 512                                        # fft window size
    hop_s  = win_s // 2                                 # hop size
    fft_s  = win_s // 2 + 1                             # spectrum bins

    a = source(filename, samplerate, hop_s)            # source file

    if samplerate == 0: 
        samplerate = a.samplerate
    pv = pvoc(win_s, hop_s)                            # phase vocoder
    specgram = zeros([0, fft_s], dtype=float_type)     # numpy array to store spectrogram

    # Set up LinearOscillatorModel
    def dataIn():
        while True:
            samples, read = a()        # read file
            specgram = pv(samples)     # grab complex vector
            if read < a.hop_size: 
                break
            yield(specgram)

    dataInFPS = int(samplerate / hop_s)
        
    M = LinearOscillatorModel(
            sampleRate       = 24,         # Visual sample rate
            dataInFPS        = dataInFPS,  # Data sample rate (to generate visual)
            number_of_points = points,     # how many points in simulation?
            hook             = 121.0,
            dataIn           = dataIn,
            data_shape       = (256, ),
            damping          = 0.95)

    frames = M.get_frames()
    clip = ImageSequenceClip(frames, fps = 24)
    try:
        clip.write_videofile("output.mp4", fps = 24, audio=filename)
    except:
        print("[!] ERROR: Couldn't Write Audio!")
        clip.write_videofile("output.mp4", fps = 24)

if __name__ == '__main__':
    if len(argv) == 1:
        plot_spectrogram('../media/440Hz_With_660Hz-Pulse.wav', samplerate = 0)
    else:
        plot_spectrogram(argv[1], samplerate = 0)
