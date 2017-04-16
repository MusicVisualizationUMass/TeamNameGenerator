from pydub import AudioSegment
from sys import argv
import uuid

def mp3_to_wav(filepathIn):
    sound = AudioSegment.from_mp3(filepathIn)
    unique_filename = '/tmp/' + uuid.uuid4()
    sound.export(unique_filename, format="wav")
    return unique_filename
