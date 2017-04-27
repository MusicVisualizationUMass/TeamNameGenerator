import unittest as ut
from pipeline.ir import (IntermediateRepr, AudioRepr, ParametricRepr,
                         ModelledRepr)

class TestIR(ut.TestCase):
    
    def test_constructor(self):
        try:
            ir = IntermediateRepr(sampleRate  = 24, 
                                  sampleRange = (0, 32), 
                                  dataIn      = 'sample data string', 
                                  parameters  = {'this is': 'a test'} )
        except:
            self.assertFalse(True)

    def test_getters(self):
        ir = IntermediateRepr(sampleRate  = 24, 
                              sampleRange = (0, 32), 
                              dataIn      = 'sample data string', 
                              parameters  = {'this is': 'a test'} )
        self.assertEqual(ir.get_sample_rate()   , 24)
        self.assertEqual(ir.get_sample_range()  , (0, 32))
        self.assertEqual(ir.get_sample_min()    , 0)
        self.assertEqual(ir.get_sample_max()    , 32)
        self.assertEqual(ir.get_data()          , [])
        self.assertEqual(ir.get_param('this is'), 'a test')


    def test_iter(self):
        
        ir = IntermediateRepr(sampleRate  = 24, 
                              sampleRange = (0, 32), 
                              dataIn      = 'sample data string', 
                              parameters  = {'this is': 'a test'} )
        

        total = 0   # total number of elements
        for i in iter(ir):
            total += 1
        self.assertEqual(total, 0) # Should be empty

        ir._data = range(100)
        
        for i in iter(ir):
            total += 1

        self.assertEqual(total, 100)

    def test_getitem(self):
        ir = IntermediateRepr(sampleRate  = 24, 
                              sampleRange = (0, 32), 
                              dataIn      = 'sample data string', 
                              parameters  = {'this is': 'a test'} )

        ir._data = range(100)

        for i in range(100):
            self.assertEqual(ir[i], i)
        
        

class TestAudioRepr(TestIR):
    '''This extends TestIR...'''
    def test_air_constructor_default_vals(self):
        try:
            air = AudioRepr()
            self.assertEqual(air._sampleRate, 44100)
            self.assertEqual(air._bitDepth  , 16   )
            self.assertEqual(air._sampleMin , 0    )
            self.assertEqual(air._sampleMax , 2**16)
            self.assertEqual(air._sampleType, int  )
            self.assertEqual(air._audioFile , None )

        except Exception as e:
            print("Caught Exception: {}".format(e))
            self.assertFalse(True)
        


