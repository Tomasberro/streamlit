from pydub import AudioSegment

def split_audio(chunk_size):
    duration = chunk_size["duration"]
    segment_length = chunk_size["chunk_size"]
    num_segments = duration // segment_length
    remainder = duration % segment_length
    
    results = []
   
    
    # Split audio into segments
    for i in range(num_segments):
        start_time = i * segment_length
        end_time = (i + 1) * segment_length
        segment = chunk_size["audio"][start_time:end_time]
        segment.export(f"temp/segment_{i + 1}.mp3", format="mp3")
        results.append(segment)
        
    if remainder > 0:
        start_time = num_segments * segment_length
        segment = chunk_size["audio"][start_time:]
        if len(segment) >= 0.1 * 1000:
            segment.export(f"temp/segment_{num_segments + 1}.mp3", format="mp3")
            results.append(segment)
  
    return results
