'''
Implement the AudioSource class. This represents an audio source, such as a
music file or an audio stream, and should be extended for particular inputs.

Date:   4/4/17
Author: Benjamin Kushigian
'''

class AudioSource(object):
    def __init__(self):
        raise NotImplementedError('AudioSource is abstract')

    def __iter__(self):
        raise NotImplementedError('AudioSource is abstract')
