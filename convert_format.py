from pydub import AudioSegment
import io
import os

def convert_to_mp3(audio_data,  output_dir, chunk_index):
    """
    Converts audio data to MP3 format.

    Parameters:
        audio_data (ndarray): The audio data recorded by sounddevice.

    Returns:
        BytesIO: The audio file in MP3 format.
    """
    # Convert to audio file format (MP3).
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    audio_segment = AudioSegment(audio_data.tobytes(), frame_rate=44100, sample_width=2, channels=2)
    audio_file_path = os.path.join(output_dir, f"chunk_{chunk_index}.mp3")
    audio_segment.export(audio_file_path, format='mp3')

    return audio_file_path
