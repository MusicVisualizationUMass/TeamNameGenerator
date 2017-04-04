'''audiofile.py
define the AudioFile class. 

TODO: 
    * Incorporate aubio library
'''
from pipeline.audiosource import AudioSource

class AudioFile(AudioSource):
    def __init__(self, filepath):
        self.filepath  = filepath
        try:
            with open (filepath) as f:
                self.contents = f.read()
        except Exception as e:
            # TODO: Aside from print? We should return exception...
            print("Error opening audio file '{}'".format(filepath))

