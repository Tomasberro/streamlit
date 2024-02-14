
from io import BytesIO


def stream_audio_file(audio_file, chunk_size):
    while True:
        chunk = audio_file.read(chunk_size)
        if not chunk:
            break
        yield BytesIO(chunk)