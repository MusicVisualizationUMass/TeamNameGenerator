import unittest as ut
import os
from musicvisualizer.pipeline.ir import (IntermediateRepr, AudioRepr, ParametricRepr,
                                         ModelledRepr, PhaseVocPR)
from musicvisualizer.pipeline.models.linear_oscillator import LinearOscillatorModel
from musicvisualizer.pipeline.mp3_to_wav import mp3_to_wav

class TestLinearOscillator(ut.TestCase):
    
    def setUp(self):
        from os.path import join
        source = join('..','media', 'sampler.mp3')
        source_wav = mp3_to_wav(source)  # Create a temp file
        self.source_wav = source_wav     # Store for later deletion!
        self.input_fields = {'groovyness' : 0}
        self.air   = AudioRepr (source_wav, self.input_fields)
        self.phvoc = PhaseVocPR(self.air  , self.input_fields)

        
    def tearDown(self):
        try:
            os.remove(self.source_wav)   # Get rid of temp file
        except Exception as e:
            print ("Error deleting temp file!", e)

    def test_constructor_type(self):
        linosc = LinearOscillatorModel(self.phvoc, self.input_fields)
        self.assertIsInstance(linosc, LinearOscillatorModel)

    def test_constructor_type2(self):
        linosc = LinearOscillatorModel(self.phvoc, self.input_fields)
        self.assertIsInstance(linosc, ModelledRepr)

    def test_construtor_bad_PIR(self):
        pir = ParametricRepr()
        def this_should_raise():
            try:
                linosc = LinearOscillatorModel(pir, self.input_fields)
            except Exception as e:
                print(e)
                raise e
        self.assertRaises(Exception, this_should_raise)
