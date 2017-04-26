from ir import ModelledRepr
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

		#minVal = min(min(frame))
		#maxVal = max(max(frame))

		#image = Image.fromarray(frame.astype('uint8'), 'RGB')
		#frame = [x-minVal for x in frame]	#remove 
		#frame_n = frame/frame.max(axis=0)	#normalize frame
		im = Image.fromarray(np.uint8(cm.gist_earth(frame_n)*255))
		return im

	def visualize(self):
		result = []

		#I = list(iter(self.model))
		I = iter(self.model)
		for frame in I:
			result.append(make_frame(frame))

		#isc = ImageSequenceClip(result, fps = 24)
		#isc.write_videofile('movie.mp4', fps=24)

		return result


