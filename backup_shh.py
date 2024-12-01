from faster_whisper import WhisperModel

print('Also called')
model = WhisperModel("large-v3", compute_type="int8")

def transcribe(wav_path: str) -> str:
    print("Loading whisper")
    print("Segmentation baby!")
    segments, info = model.transcribe(wav_path, beam_size=5)
    segments = list(segments)
    print("Detected language '%s' with probability %f" % (info.language, info.language_probability))
    for segment in segments:
        print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
    ret = "".join(segment.text for segment in segments)
    print("RETTTTTT", ret)
    return ret
