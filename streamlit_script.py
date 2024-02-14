import os
import time
import streamlit as st
import requests
from stream_audio import stream_audio_file
from split_audio import split_audio
from chunk_size import get_chunk_size
import sounddevice as sd
import numpy as np

from convert_format import convert_to_mp3
from file_downloader import get_binary_file_downloader, get_binary_file_downloader_html

# fastapi_url = "http://127.0.0.1:8000" 
fastapi_url = "http://18.219.65.176:8000"

endpoint_path = "/"  
endpoint_whisper = "/whisper_model/"
moderation_endpoint = "/moderation/"
fine_completion_endpoint = "/fine_tuning_completions/"
endpoint_whisper_incremental = "/whisper_model_incremental/"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    
USERNAME = "arijit"
PASSWORD = "ramen"

username_input = st.sidebar.text_input("User", "")
password_input = st.sidebar.text_input("Password", "", type="password")

if st.sidebar.button("Login"):
    if username_input == USERNAME and password_input == PASSWORD:
        st.session_state.logged_in = True
        st.success("Login successful. Welcome, {}".format(USERNAME))
        # Here goes the rest of your application code
    else:
        st.error("Incorrect credentials. Please try again.")
        st.session_state.logged_in = False
if st.session_state.logged_in:
    
    st.title("Transcription of all audio at once")

    audio_file = st.file_uploader("Select an audio file", type=["mp3", "m4a", "wav"])

    # Button to make the call to the audio translation endpoint
    if audio_file and st.button("Translate Audio to Text"):
        # Make HTTP request to the audio translation endpoint
        translation_response = requests.post(f"{fastapi_url}{endpoint_whisper}", files={"file": audio_file})

        # Check if the request was successful (status code 200)
        if translation_response.status_code == 200:
            st.success("Translation successful.")
            translated_text = translation_response.json()["result"]
            st.text(translation_response.json()["result"])  # Display the translated text in Streamlit
     
            moderation_response = requests.post(f"{fastapi_url}{moderation_endpoint}", json={"transcription": translated_text['text']})
       
            if moderation_response.status_code == 200:
                moderation_result = moderation_response.json()["result"]
                if moderation_result == "approved":
                    st.text("Moderation: Text is approved.")
                    fine_completion_response = requests.post(f"{fastapi_url}{fine_completion_endpoint}", json={"transcription": translated_text['text']})
                    st.text(fine_completion_response.json()["result"]["message"]["content"])
                else:
                    st.warning("{moderation_result}: Text is not approved.")
            else:
                st.error(f"Moderation failed. Status code: {moderation_response.status_code}")
        else:
            st.error(f"Translation failed. Status code: {translation_response.status_code}")

    st.title("Real-time Audio Transcription (from to segments)")

    audio_file = st.file_uploader("Select an audio file to real-time", type=["mp3", "m4a", "wav"])

    # Button to call the audio translation endpoint
    if audio_file and st.button("Translate Audio Real time to Text"):
        chunk_size = get_chunk_size(audio_file)
        translation_result = ""
    
        with st.spinner("Translating..."):
            start_time = time.time()
            audio_segments = split_audio(chunk_size)
            for i , segment in enumerate(audio_segments):
                #  Make HTTP request to the incremental audio translation endpoint
                segment_file_path = f"temp/segment_{i + 1}.mp3"
                if os.path.exists(segment_file_path):
                    with open(segment_file_path, "rb") as audio_segment:
                   
                        translation_response = requests.post(
                        f"{fastapi_url}{endpoint_whisper}",
                        files={"file": audio_segment},
                        )
                    if translation_response.status_code == 200:
                        translation_result += translation_response.json()["result"]["text"]
                        st.text("Translation:")
                        st.text(translation_response.json()["result"]["text"])
                        moderation_response = requests.post(f"{fastapi_url}{moderation_endpoint}", json={"transcription": translation_response.json()["result"]["text"]})
                        if moderation_response.status_code == 200:
                            moderation_result = moderation_response.json()["result"]
                            if moderation_result == "approved":
                                st.text("Moderation: Text is approved.")
                                fine_completion_response = requests.post(f"{fastapi_url}{fine_completion_endpoint}", json={"transcription": translation_response.json()["result"]["text"]})
                                st.text("Summary:")
                                st.text(fine_completion_response.json()["result"]["message"]["content"])
                                end_time = time.time()
                                st.text(f"Total time: {end_time - start_time}")
                            else:
                                st.warning("{moderation_result}: Text is not approved.")
                        else:
                            st.error(f"Moderation failed. Status code: {moderation_response.status_code}")
                    else:
                     st.error(f"Translation failed. Status code: {translation_response.status_code}")
                     # Delete the temporary file after transcription
                     os.remove(segment_file_path)
                     # time.sleep(chunk_size["chunk_size"] / 1000)
                     time.sleep(5)
                else:
                    st.error(f"Temporary file for segment {i + 1} not found")

        st.success("Translation successful.")
        st.text(translation_result)


    # Main Streamlit app
    st.title("Real-time Microphone Transcription")

    recording = False
    # Button to start real-time transcription
    if not recording and st.button("Start Real-time Microphone (30 seconds)"):
        st.write("Recording started...")
        translation_result = ""
        recording = True
        # Define the duration of each audio chunk (in seconds)
        chunk_duration = 10  # You can adjust this value as needed
        total_duration = 30
    
        output_dir = "temp"
        os.makedirs(output_dir, exist_ok=True)
        # Start recording audio in real-time
        with st.spinner("Transcribing..."):
            start_time = time.time()
            chunk_index = 0
            while recording:
                # Capture audio from the microphone
                audio_data = sd.rec(int(chunk_duration * 44100), samplerate=44100, channels=2, dtype=np.int16)
                sd.wait()
                # print(audio_data, "audio_data")
                audio_file_path = convert_to_mp3(audio_data, output_dir, chunk_index)
           
                chunk_index += 1
          
                # Translate the audio chunk
                with open(audio_file_path, "rb") as audio_file:
                    translation_response = requests.post(
                        f"{fastapi_url}{endpoint_whisper}",
                        files={"file": audio_file}
                    )
                    if translation_response.status_code == 200:
                        translation_result = translation_response.json()["result"]["text"]
                        st.text("Translation:")
                        st.text(translation_result)
                        # Other processing logic
                        moderation_response = requests.post(f"{fastapi_url}{moderation_endpoint}", json={"transcription": translation_response.json()["result"]["text"]})
                        if moderation_response.status_code == 200:
                            moderation_result = moderation_response.json()["result"]
                            if moderation_result == "approved":
                                st.text("Moderation: Text is approved.")
                                fine_completion_response = requests.post(f"{fastapi_url}{fine_completion_endpoint}", json={"transcription": translation_response.json()["result"]["text"]})
                                st.text("Summary:")
                                st.text(fine_completion_response.json()["result"]["message"]["content"])
                                end_time = time.time()
                                st.text(f"Total time: {end_time - start_time}")
                            else:
                                st.warning("{moderation_result}: Text is not approved.")
                        else:
                            st.error(f"Moderation failed. Status code: {moderation_response.status_code}")
                    else:
                     st.error(f"Translation failed. Status code: {translation_response.status_code}")

                if time.time() - start_time >= total_duration:  # Stop after 60 seconds (you can adjust this)
                 break
            
        st.success("Transcription complete.")
    
    # if recording and st.button("Stop Recording"):
    #     recording = False

    st.title("Audio Upload and CSV Download")

    audio_file = st.file_uploader("Select an audio file to csv", type=["mp3", "m4a","wav"])

    if audio_file is not None and st.button("Submit"):
        response = requests.post(f"{fastapi_url}/whisper_fine_tune_csv/", files={"file": audio_file})
        if response.status_code == 200:
            st.markdown(get_binary_file_downloader(response.content, "CSV File"), unsafe_allow_html=True)
        else:
            st.error("There was an error processing the request. Please try again.")

