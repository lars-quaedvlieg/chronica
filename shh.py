import os
import time
import shutil
import threading
from pathlib import Path

import wave
from newwhisper.client import Client, TranscriptionTeeClient


class ActualWhisperClient(TranscriptionTeeClient):
    def __init__(
        self,
        host,
        port,
        lang=None,
        translate=False,
        model="small",
        use_vad=True,
        save_output_recording=False,
        output_recording_filename="./output_recording.wav",
        output_transcription_path="./output.srt",
        log_transcription=True,
    ):
        self.client = Client(host, port, lang, translate, model, srt_file_path=output_transcription_path, use_vad=use_vad, log_transcription=log_transcription)
        if save_output_recording and not output_recording_filename.endswith(".wav"):
            raise ValueError(f"Please provide a valid `output_recording_filename`: {output_recording_filename}")
        if not output_transcription_path.endswith(".srt"):
            raise ValueError(f"Please provide a valid `output_transcription_path`: {output_transcription_path}. The file extension should be `.srt`.")
        TranscriptionTeeClient.__init__(
            self,
            [self.client],
            save_output_recording=save_output_recording,
            output_recording_filename=output_recording_filename
        )

        print("[INFO]: Waiting for server ready ...")
        for client in self.clients:
            while not client.recording:
                if client.waiting or client.server_error:
                    self.close_all_clients()
                    return
        print("[INFO]: Server ready")

        self.cv = threading.Condition()
        if self.save_output_recording:
            if os.path.exists("chunks"):
                shutil.rmtree("chunks")
            os.makedirs("chunks")
        self.n_audio_files = 0

    def process_segments(self, segments: list[str]):
        super().process_segments(segments)
        #with self.cv:
        #    self.cv.notify()

    def update(self, data: bytes):
        self.frames += data
        audio_array = self.bytes_to_float_array(data)

        self.multicast_packet(audio_array.tobytes())

        # save frames if more than a minute
        if len(self.frames) > 60 * self.rate:
            if self.save_output_recording:
                self.save_chunk(self.n_audio_files)
                self.n_audio_files += 1
            self.frames = b""
        self.write_all_clients_srt()

        # Wait until we receive a response from the server (we get notified in the process_segments).
        #with self.cv:
        #    print("[INFO] Waiting for server response")
        #    self.cv.wait()
        #print("[INFO] Got server response :D")


data_root = Path("data/entry_new")
CLIENT: ActualWhisperClient = ActualWhisperClient(
    "localhost",
    9090,
    lang="en",
    translate=False,
    model="small",
    use_vad=False,
    save_output_recording=True,
    output_recording_filename=str(data_root/"recording.wav"),
    output_transcription_path=str(data_root/"transcript.srt"),
)
assert len(CLIENT.clients) == 1
CLIENT.stream = CLIENT.p.open(
    format=CLIENT.p.get_format_from_width(2),  # TODO maybe not 2?
    channels=CLIENT.channels,
    rate=48000, #16000, # TODO maybe different?
    input=True,
    output=True,
    frames_per_buffer=CLIENT.chunk,
)


def update_recording(new_entry_path: str) -> str:
    print(f"[INFO] Whispering path {new_entry_path}")
    with wave.open(new_entry_path, "rb") as wavfile:
        assert wavfile.getframerate() == 48000, wavfile.getframerate()
        assert wavfile.getsampwidth() == 2, wavfile.getsampwidth()
        print("[INFO] This wav should be", wavfile.getnframes()/wavfile.getframerate(), "seconds")
        while (data := wavfile.readframes(CLIENT.chunk)) != b"":
            print("[INFO] Sending data with length", len(data))
            assert len(CLIENT.clients) == 1
            audio_array = CLIENT.bytes_to_float_array(data)
            print("[INFO] Len array:", audio_array.size)
            CLIENT.multicast_packet(audio_array.tobytes())
            CLIENT.stream.write(data)

    while CLIENT.clients[0].done_with_this_crap < 2:
        time.sleep(0.05)
    CLIENT.clients[0].done_with_this_crap = 0
    return "".join(segment["text"] for segment in CLIENT.clients[0].transcript) + CLIENT.clients[0].last_segment["text"]

    # Wait until transcription is done.
    # We do this in (a not very nice way).
    # We wait until we receive two consecutive responses where the text didn't change.
    #prev_text = None
    #current_text = None
    #last_response_received = CLIENT.clients[0].last_response_received
    #current_last_response_received = CLIENT.clients[0].last_response_received
    #converged = False
    #while not converged:
    #    time.sleep(1.0)
    #    prev_text = current_text
    #    last_response_received = current_last_response_received

    #    current_text = "".join(segment["text"] for segment in CLIENT.clients[0].transcript)
    #    current_last_response_received = CLIENT.clients[0].last_response_received
    #    if CLIENT.clients[0].last_segment is not None:
    #        current_text += CLIENT.clients[0].last_segment["text"]
    #    print(last_response_received, current_last_response_received, prev_text, current_text)
    #    if last_response_received < current_last_response_received and prev_text == current_text:
    #        assert CLIENT.clients[0].last_segment is not None
    #        converged = True
    #return current_text


if __name__ == "__main__":
    txt1 = update_recording("recordings/rec1.wav")
    print("Output1:")
    print(txt1)
    txt2 = update_recording("recordings/rec2.wav")
    print("Output2:")
    print(txt2)
    txt3 = update_recording("recordings/rec3.wav")
    print("Output3:")
    print(txt3)
