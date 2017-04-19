'''
pipeline.py
define the Pipeline class
Date:   4/4/17
Author: Benjamin Kushigian

TODOs:
    * Just about everything
'''

from spectrogram import get_spectrogram
from mp3_to_wav import mp3_to_wav

class Pipeline(object):
    groovyness = 0
    source = ''
    def __init__(self, inputFields):
        groovyness = inputFields.groovyness
        source = inputFields.source
        convert_file() # change source from mp3 to wav

    def convert_file():
        # takes a filepath source and returns a new source in temp dir as a wav
        source = mp3_to_wav(source)

    # this is what will be called to build the visualization
    def buildVisualization():
        # returns a numpy array
        specgram = get_spectrogram(source) # no sample rate for now
        # TODO: do something with that numpy array
