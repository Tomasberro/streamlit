from pydub import AudioSegment

def get_chunk_size(audio_file):
    audio = AudioSegment.from_file(audio_file)
    audio_duration_ms = len(audio)

    if audio_duration_ms <= 5 * 60 * 1000:  
        return {"audio": audio,"duration": audio_duration_ms, "chunk_size": 15000}  
    elif audio_duration_ms <= 10 * 60 * 1000:  # 10 minutes
        return {"audio": audio,"duration": audio_duration_ms, "chunk_size": 30000}
    elif audio_duration_ms <= 15 * 60 * 1000:  # 15 minutes
        return {"audio": audio,"duration": audio_duration_ms, "chunk_size": 45000} 
    elif audio_duration_ms <= 20 * 60 * 1000:  # 20 minutes
        return {"audio": audio,"duration": audio_duration_ms, "chunk_size": 60000}
    elif audio_duration_ms <= 25 * 60 * 1000:  # 25 minutes
        return {"audio": audio,"duration": audio_duration_ms, "chunk_size": 75000}
    elif audio_duration_ms <= 30 * 60 * 1000:  # 30 minutes
        return {"audio": audio,"duration": audio_duration_ms, "chunk_size": 90000}
    elif audio_duration_ms <= 35 * 60 * 1000:  # 35 minutes
        return {"audio": audio,"duration": audio_duration_ms, "chunk_size": 105000}
    elif audio_duration_ms <= 40 * 60 * 1000:  # 40 minutes
        return {"audio": audio,"duration": audio_duration_ms, "chunk_size": 120000}
    elif audio_duration_ms <= 45 * 60 * 1000:  # 45 minutes
        return {"audio": audio,"duration": audio_duration_ms, "chunk_size": 135000}
    elif audio_duration_ms <= 50 * 60 * 1000:  # 50 minutes
        return {"audio": audio,"duration": audio_duration_ms, "chunk_size": 150000}
    elif audio_duration_ms <= 55 * 60 * 1000:  # 55 minutes
        return {"audio": audio,"duration": audio_duration_ms, "chunk_size": 165000}
    else :
        return {"audio": audio,"duration": audio_duration_ms, "chunk_size": 180000}