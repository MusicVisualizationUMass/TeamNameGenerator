from aubio import pvoc, source, float_type
from numpy import zeros, log10, vstack
import matplotlib.pyplot as plt
from pipeline.models.linear_oscillator import LinearOscillatorModel
from sys import argv

def plot_spectrogram(filename, samplerate = 0):
    points = 257 
    win_s  = 512                                        # fft window size
    hop_s  = win_s // 2                                 # hop size
    fft_s  = win_s // 2 + 1                             # spectrum bins

    a = source(filename, samplerate, hop_s)            # source file

    if samplerate == 0: 
        samplerate = a.samplerate
    pv = pvoc(win_s, hop_s)                            # phase vocoder
    specgram = zeros([0, fft_s], dtype=float_type)     # numpy array to store spectrogram

    while False:   # Set to true for interpreter
        s = input('>>> ').strip()
        if s.lower() in ('x', 'q', 'quit', 'exit', 'break'):
            break
        try:
            exec(s)
        except Exception as e:
            print(e)

    # Set up LinearOscillatorModel
    def dataIn():
        while True:
            samples, read = a()        # read file
            specgram = pv(samples)     # grab complex vector
            # while True:
            #     s = input('>>> ')
            #     if s.strip() == 'q':
            #         break
            #     try:
            #         exec(s)
            #     except Exception as e:
            #         print(e)
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

    I = iter(M)

    plt.ion()            # Interactive I/O

    for frame in I:
        ys = [ p[0] for p in frame]
        xs = range(len(frame))
        # Set frame info (+/- 1) to keep view realtively fixed...
        ys = ys + [1.0, -1.0]
        # Set the extra points in ys to x = 0
        xs = list(xs) + [len(xs), len(xs)]
        plt.plot(xs, ys)
        plt.show()        # Update visuals
        plt.pause(0.01)    # Pause
        plt.cla()         # Clear 

if __name__ == '__main__':
    if len(argv) == 1:
        plot_spectrogram('../media/440Hz_With_660Hz-Pulse.wav', samplerate = 0)
    else:
        plot_spectrogram(argv[1], samplerate = 0)
