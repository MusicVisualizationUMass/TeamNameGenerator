import unittest as ut
import matplotlib.pyplot as plt
from pipeline.models.grayscottmodel import GrayScottModel


class TestGrayScott(ut.TestCase):
    
    def test_constructor(self):
        try:
            model = GrayScottModel()
        except Exception as e:
            self.assertFalse(True)

