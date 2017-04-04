import unittest as ut
from pipeline.ir import ( IntermediateRepr, AudioRepr, ParametricRepr,
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
        self.assertEquals(ir.get_sample_rate(), 24)
        self.assertEquals(ir.get_sample_range(), (0, 32))
        self.assertEquals(ir.get_sample_min(), 0)
        self.assertEquals(ir.get_sample_max(), 32)
        self.assertEquals(ir.get_data(), [])
        self.assertEquals(ir.get_param('this is'), 'a test')
