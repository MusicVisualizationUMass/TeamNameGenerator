# -*- coding: utf-8 -*-
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
        raise self._sampleRate

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
        raise NotImplementedError()

    def __getitem__(self, key):
        raise NotImplementedError()

class VisualizableMixin(object):
    ''' Mixin describing a visualizable class '''

    def visualize(self):
        raise NotImplementedError()

class AudioRepr(IntermediateRepr):
    '''
    AudioRepr represents an audio stream/array.
    TODO: Document
    '''
    def __init__(self, sampleRate = 44100, sampleRange = (None, None),
                 dataIn = None, parameters = None, sampleType = int, 
                 bitDepth = 16, audioFile = None):
        '''
        TODO: how to pull in audio data?
        '''

        super(AudioRepr, self).__init__(sampleRate  = sampleRate,
                                        sampleRange = (0, 2**bitDepth),
                                        dataIn      = dataIn,
                                        parameters  = parameters)
        self._bitDepth   = bitDepth
        self._sampleType = sampleType
        self._audioFile  = audioFile

    def __iter__(self):
        return iter(self._data)

    def __getitem__(self, key):
        '''
        TODO: Error check? Extend?
        '''
        return self._data[key]

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

class ModelledRepr(IntermediateRepr, VisualizableMixin):
    def __init__(self, sampleRate = 24, sampleRange = (None, None),
                 dataIn = None, parameters = None):
        super(ModelledRepr, self).__init__(sampleRate  = sampleRate,
                                           sampleRange = sampleRange,
                                           dataIn      = dataIn,
                                           parameters  = parameters)
    def visualize(self):
        # TODO
        raise NotImplementedError('todo')

