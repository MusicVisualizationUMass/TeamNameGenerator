# -*- coding: utf-8 -*-
from aubio import pvoc, float_type
import aubio

from numpy import zeros, log10, vstack
'''
ir.py: Defines the intermediate representation API and the main components of
the pipeline. These can be extended as seen fit.

date:   4/3/17
author: Benjamin Kushigian

Overview:
    define abstract class IntermediateRepr(object) and extend it with

        * AudioRepr(IntermediateRepr)
        * ParametricRepr(IntermediateRepr)
        * ModelledRepr(IntermediateRepr)
        * VisualizableMixin(object)
    
    where Visualizable will be a trait extended by ModelledRepr. 

TODO: All of it
'''

class IntermediateRepr(object):
    def __init__(self, sampleRate = None, sampleRange = (None, None),
                 dataIn = None, parameters = None):
        '''
        sampleRate: rates per second
        sampleRange: (min, max) for possible sample values.
        dataIn: preexisting data being passed in to be processed
        parameters: a parameter dictionary passed for extra information
        '''
        self._sampleRate  = sampleRate
        self._sampleMin   = sampleRange[0]
        self._sampleMax   = sampleRange[1]
        self._dataIn      = dataIn
        self._params      = {}
        if parameters:
            self._params  = parameters
        self._data        = []

    def get_sample_rate(self):
        return self._sampleRate

    def get_sample_range(self):
        return self._sampleMin, self._sampleMax

    def get_sample_min(self):
        return self._sampleMin

    def get_sample_max(self):
        return self._sampleMax

    def get_data(self):
        return self._data

    def get_params(self):
        return self._params

    def get_param(self, key):
        if key in self._params:
            return self._params[key]
        return None

    def __iter__(self):
        return iter(self._data)

    def __getitem__(self, key):
        return self._data[key]

class VisualizableMixin(object):
    ''' Mixin describing a visualizable class '''

    def visualize(self):
        raise NotImplementedError()

class AudioRepr(IntermediateRepr):
    '''
    AudioRepr represents an audio stream/array.
    TODO: Document
    '''
    def __init__(self, audioFile, input_fields, sampleRate = 0, sampleRange = (None, None),
                 dataIn = None, parameters = None, sampleType = int, 
                 bitDepth = 16):

        self.input_fields = input_fields
        verbose = 'verbose' in input_fields and input_fields['verbose']
        if verbose:
            print('[DEBUG] Creating AudioRepr instance')
        self._audioFile  = audioFile
        self._sampleRate = sampleRate
        self._sampleMin  = sampleRange[0]
        self._sampleMax  = sampleRange[1]
        self._sampleType = sampleType
        self._bitDepth   = bitDepth

        if sampleRange[0] is None:
            self._sampleMin = 0
        if sampleRange[1] is None:
            self._sampleMax = 2**bitDepth

        self.win_s  = 512           # fft window size
        self.hop_s  = self.win_s // 2    # hop size
        
        if verbose:
            print('        audiofile = {}, win_s = {}, hop_s = {}'.format(
                  audioFile, self.win_s, self.hop_s))
        self.source = aubio.source(audioFile, sampleRate, self.hop_s)
        self.sampleRate = self.source.samplerate
        if verbose:
            print('        source = {}'.format(self.source))
            print('        sampelrate = {}'.format(self.sampleRate))


    def __iter__(self):
        raise NotImplementedError('I\'m not implemented! Oh No!')

    def __getitem__(self, key):
        '''
        TODO: Error check? Extend?
        '''
        raise NotImplementedError('I\'m not implemented! Oh No!')

class ParametricRepr(IntermediateRepr):
    '''
    ParametricRepr: represents the parametrized phase of translation.
    '''
    def __init__(self, sampleRate = 24, sampleRange = (0, 255),
                 dataIn = None, parameters = None, dims = 2, sampleType = int):
        '''
        dims: number of dimensions to extract from dataIn
        sampleType: type of sample to create from dataIn
        '''
        super(ParametricRepr, self).__init__(sampleRate  = sampleRate,
                                            sampleRange  = sampleRange,
                                            dataIn       = dataIn,
                                            parameters   = parameters)
        self._dims       = dims
        self._sampleType = sampleType

    def __iter__(self):
        return iter(self._data)

    def __getitem(self, key):
        return self._data[key]

class PhaseVocPR(ParametricRepr):
    def __init__(self, audiorepr, input_fields, windowsize = 512, sampleRate = 0, 
                 sampleRange = (0, 255), dataIn = None, parameters = None, 
                 dims = 2, sampleType = int):
        '''
        For now ignoring a large part of the ParametricRepr API as much of
        this is taken care of automatically (via aubio.source). All we need is
        an aubiosource input and an input_fields that contains data/parameters
        from the user/defaults from the system
        '''

        self.input_fields = input_fields
        self.verbose = 'verbose' in input_fields and input_fields['verbose']
        
        if self.verbose:
            print('[DEBUG] Creating PhaseVocPR')
        self.air    = audiorepr
        self.source = self.air.source
        self.input_fields = input_fields
        self.win_s  = self.air.win_s
        self.hop_s  = self.air.hop_s
        self.fft_s  = self.win_s // 2 + 1
        self.sampleRate = self.air.sampleRate
        self.dataInFPS  = int(self.sampleRate / self.hop_s)


    def getDataIn(self):
        ''' 
        Return a new dataIn function that creates a generator for cvec data
        Pretty much the same as __iter__(). Probably can take this out...
        '''
        def dataIn():
            pv = pvoc(self.win_s, self.hop_s)
            while True:
                samples, read = self.source() # Read the file
                cvec          = pv(samples)
                if read < self.source.hop_size:
                    break                     # Out of samples
                yield (cvec)

        return dataIn

    def __iter__(self):
        if self.verbose:
            print('[DEBUG] PhaseVocPR.__iter__()')
        pv = pvoc(self.win_s, self.hop_s)
        if self.verbose:
            print('        Created Phase Vocoder (pv = pvoc(self.win_s, self.hop_s)')

        while True:
            samples, read = self.source() # Read the file
            cvec = pv(samples)
            if read < self.source.hop_size:
                break                     # Out of samples
            yield (cvec)

class ModelledRepr(IntermediateRepr, VisualizableMixin):
    def __init__(self, sampleRate = 24, sampleRange = (None, None),
                 dataIn = None, parameters = None):
        super(ModelledRepr, self).__init__(sampleRate  = sampleRate,
                                           sampleRange = sampleRange,
                                           dataIn      = dataIn,
                                           parameters  = parameters)
    def visualize(self):
        raise NotImplementedError('todo')

