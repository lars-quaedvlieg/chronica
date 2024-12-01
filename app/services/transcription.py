#from shh import update_recording
from backup_shh import transcribe


def process_audio(audio_data):
    #return update_recording(audio_data)
    return transcribe(audio_data)
