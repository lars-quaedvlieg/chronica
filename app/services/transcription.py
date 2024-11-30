from shh import update_recording


def process_audio(audio_data):
    return update_recording(audio_data.read())
