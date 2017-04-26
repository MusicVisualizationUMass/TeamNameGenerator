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
    groovyness = 0
    source = ''
    def __init__(self, input_fields):
        self.input_fields = input_fields
        self.visual_type = 'linear-oscillator'
        self.convert_file()     # change source from mp3 to wav
        # XXX: For now, just build the video!

    def convert_file(self):
        # takes a filepath source and returns a new source in temp dir as a wav
        source = self.input_fields['source']
        self.source     = source   # original source
        self.source_wav = mp3_to_wav(source) # WAV file

    def buildVisualization(self):
        # XXX Assuming that we are doing a linear oscillator
        # Need to store a field in InputFields for type of visualization
        # later if we want multiple types of visualizations
        if self.visual_type == 'linear-oscillator':
            visualizer = self.buildLinearOscillatorVisualizer()
            self.makeMovie(visualizer)


    def makeMovie(self, visualizer, output = None):
        if output == None:
            if 'output' in self.input_fields:
                output = self.input_fields['output']
            else:
                output = 'output.mp4'
        frames = visualizer.visualize()
        clip = ImageSequenceClip(frames, fps = 24)

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
        
        print("Creating AIR")
        audio = AudioRepr(self.source_wav)
        print("Creating PIR")
        phvoc = PhaseVocPR(audio, self.input_fields)
        print("Creating MIR")
        dataInFPS = phvoc.dataInFPS # XXX: This should be automatic
        linos = LinearOscillatorModel(
                phvoc,                         # Phase Vocoder
                sampleRate       = 24,         # Visual sample rate
                dataInFPS        = dataInFPS,  # Data sample rate (to generate visual)
                number_of_points = 256,        # how many points in simulation?
                hook             = 181.0,
                data_shape       = (256, ),
                damping          = 0.95)
        print("Creating VIR")
        lovis = LinearOscillatorVisualizer(linos)
        return lovis
