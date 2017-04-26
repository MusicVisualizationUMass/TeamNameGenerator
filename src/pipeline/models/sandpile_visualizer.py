from pipeline.ir import ModelledRepr, VisualizableMixin
import numpy as np
import matplotlib.pyplot as plt
#from moviepy.editor import *
from PIL import Image

class SubSandpileVisualizer(VisualizableMixin):
	def __init__(self, sandpile_model):
		self.model = sandpile_model

	def make_frame(self, frame):
		size = self.model.size
		A = np.zeros(shape=())

		return im

	def visualize(self, width = 100, height = 100):
		result = []

		#I = list(iter(self.model))
		I = iter(self.model)
		for frame in I:
			result.append(self.make_frame(frame))

		#isc = ImageSequenceClip(result, fps = 24)
		#isc.write_videofile('movie.mp4', fps=24)

		return result


