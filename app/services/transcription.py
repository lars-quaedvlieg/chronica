import os
import subprocess
import tempfile

import werkzeug.datastructures.file_storage

from shh import update_recording

def process_audio(audio_data: werkzeug.datastructures.file_storage.FileStorage) -> str:
    #with tempfile.NamedTemporaryFile(suffix=".webm") as webmfile:
    if os.path.exists("temp.webm"):
        os.unlink("temp.webm")
    if os.path.exists("temp.wav"):
        os.unlink("temp.wav")

    with open("temp.webm", "wb+") as webmfile:
        webmfile.write(audio_data.read())
        webmfile.flush()
        #with tempfile.NamedTemporaryFile(suffix=".wav") as wavfile:
        with open("temp.wav", "wb+") as wavfile:
            print(webmfile.name, wavfile.name)
            #subprocess.run(["ffmpeg", "-i", webmfile.name, wavfile.name])
            subprocess.run(["ffmpeg", "-y", "-i", "temp.webm", "temp.wav"])
            wavfile.flush()
            #return update_recording(wavfile.name)
            return update_recording("temp.wav")


def old_process_audio(audio_data: werkzeug.datastructures.file_storage.FileStorage):
    print(type(audio_data))
    assert not os.path.exists("temp.webm")
    with open("temp.webm", "wb+") as f:
        f.write(audio_data.read())
        print("Wrote!")
    subprocess.run(["ffmpeg", "-i", "temp.webm", "temp.wav"])
    # This is a placeholder function that returns sample text.
    # In a real implementation, this would interact with a speech-to-text service.
    return "sample transcription"
