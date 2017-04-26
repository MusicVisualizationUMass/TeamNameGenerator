'''
pipeline.py
define the Pipeline class
Date:   4/4/17
Author: Benjamin Kushigian

'''

from pipeline.mp3_to_wav import mp3_to_wav
from aubio import source
from moviepy.editor import *

class Pipeline(object):
    def __init__(self, input_fields):
        self.input_fields = input_fields
        self.extract_inputs()
        self.convert_file()     # change source from mp3 to wav
        # XXX: For now, just build the video!

    def extract_inputs(self):
        '''This extracts inputs from the input_fields to member variables'''

        # First we set defaults

        self.visualization = 'linear-oscillator'
        self.verbose       = False
        self.output        = 'output.mp4'
        self.groovy        = 0.0

        params = self.input_fields

        # Now extract any data that could be useful
        if 'visualization' in params:
            self.visualization = params['visualization']
        if 'verbose' in params and params['verbose']:
            self.verbose = True
        if 'output' in params:
            self.output = params['output']
        if 'groovy' in params:
            self.groovy = params['groovy']

    def convert_file(self):
        ''' takes a filepath source and returns a new source in temp dir as a wav'''
        self.source      = self.input_fields['source']
        self.source_wav = mp3_to_wav(self.source)

    def buildVisualization(self):
        # XXX Assuming that we are doing a linear oscillator
        # Need to store a field in InputFields for type of visualization
        # later if we want multiple types of visualizations
        if self.visualization == 'linear-oscillator':
            visualizer = self.buildLinearOscillatorVisualizer()
        else:
            if self.verbose:
                print('Warning: no visualization {}'.format(self.visualization))
                print('Default visualization: linear-oscillator')
            visualizer = self.buildLinearOscillatorVisualizer()

        self.makeMovie(visualizer)



    def makeMovie(self, visualizer, output = None):
        output = self.output
        frames = visualizer.visualize()
        clip   = ImageSequenceClip(frames, fps = 24)
        if self.verbose:
            print('Pipeline.makeMovie()')
            print('    output = {}'.format(output))

        try:
            clip.write_videofile(output, fps = 24, audio=self.source)
        except:
            try:
                clip.write_videofile(output, fps = 24, audio=self.source_wav)
            except:
                print("[!] ERROR: Couldn't include audio into", output)
                clip.write_videofile(output, fps = 24)
                

    def buildLinearOscillatorVisualizer(self):
        from pipeline.ir import PhaseVocPR, AudioRepr
        from pipeline.models.linear_oscillator import LinearOscillatorModel
        from pipeline.models.linear_oscillator_visualizer import LinearOscillatorVisualizer
        
        if self.verbose:
            print("Creating AIR")
        audio = AudioRepr(self.source_wav, self.input_fields)

        if self.verbose:
            print("Creating PIR")
        phvoc = PhaseVocPR(audio, self.input_fields)
        if self.verbose:
            print("Creating MIR")
        dataInFPS = phvoc.dataInFPS # XXX: This should be automatic
        linos = LinearOscillatorModel(
                phvoc,                         # Phase Vocoder
                input_fields     = self.input_fields,
                sampleRate       = 24,         # Visual sample rate
                dataInFPS        = dataInFPS,  # Data sample rate (to generate visual)
                number_of_points = 256,        # how many points in simulation?
                hook             = 221.0,
                vertical_hook    = 0.5,
                data_shape       = (256, ),
                damping          = 0.92)
        if self.verbose:
            print("Creating VIR")
        lovis = LinearOscillatorVisualizer(linos)
        return lovis
