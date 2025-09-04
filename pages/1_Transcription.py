#app.py
import streamlit as st
from datetime import datetime
import os
import pandas as pd
from pydub import AudioSegment
import speech_recognition as sr
from utils import extract_tags, save_transcript
from audio_recorder_streamlit import audio_recorder

# --- Setup ---
st.set_page_config(page_title="Speech Recognition System", layout="wide")
os.makedirs("uploads", exist_ok=True)
os.makedirs("transcripts", exist_ok=True)

# --- Custom CSS Styling ---
st.markdown("""
    <style>
        body { background-color: #f7f9fc; }
        .stButton>button {
            background-color: #2c7be5;
            color: white;
            border-radius: 10px;
            padding: 0.5rem 1rem;
        }
        .stDownloadButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 10px;
            padding: 0.5rem 1rem;
        }
        .chat-bubble {
            background-color: #ffffff;
            border-radius: 1rem;
            padding: 1rem;
            margin-bottom: 0.5rem;
            box-shadow: 0 1px 5px rgba(0,0,0,0.1);
        }
        .operator {
            border-left: 5px solid #2c7be5;
        }
        .client {
            border-left: 5px solid #00c9a7;
        }
        .tag {
            display: inline-block;
            background-color: #e0f0ff;
            color: #2c7be5;
            padding: 0.2rem 0.5rem;
            margin-right: 0.3rem;
            border-radius: 0.5rem;
            font-size: 0.75rem;
        }
    </style>
""", unsafe_allow_html=True)

# --- Title and Sidebar ---
st.title("🎙 Speech Recognition System")
st.sidebar.header("Options")
record_mode = st.sidebar.radio("Choose Input Mode", ["Upload File", "Record Audio"])

# --- Initialize session ---
if 'transcript' not in st.session_state:
    st.session_state.transcript = ""
if 'filename' not in st.session_state:
    st.session_state.filename = ""

# --- Upload Mode ---
if record_mode == "Upload File":
    uploaded_file = st.file_uploader("Upload an audio file", type=["wav", "mp3", "m4a", "ogg", "flac"])
    if uploaded_file:
        file_ext = os.path.splitext(uploaded_file.name)[1]
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        saved_path = os.path.join("uploads", f"{timestamp}{file_ext}")
        with open(saved_path, "wb") as f:
            f.write(uploaded_file.read())

        # Convert to WAV if needed
        if not saved_path.endswith(".wav"):
            audio = AudioSegment.from_file(saved_path)
            saved_path_wav = saved_path.rsplit(".", 1)[0] + ".wav"
            audio.export(saved_path_wav, format="wav")
        else:
            saved_path_wav = saved_path

        recognizer = sr.Recognizer()
        with sr.AudioFile(saved_path_wav) as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data)
                st.session_state.transcript = text
                st.session_state.filename = uploaded_file.name
                save_transcript(text, uploaded_file.name)
                st.success("✅ Transcription completed successfully!")
            except sr.UnknownValueError:
                st.error("Could not understand the audio.")
            except sr.RequestError:
                st.error("Recognition service error.")

# --- Record Mode (using audio_recorder_streamlit) ---
elif record_mode == "Record Audio":
    st.info("Click the microphone below to start/stop recording.")
    audio_bytes = audio_recorder()

    if audio_bytes:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"recording_{timestamp}.wav"
        filepath = os.path.join("uploads", filename)

        # Save the recorded audio
        with open(filepath, "wb") as f:
            f.write(audio_bytes)

        # Transcribe
        recognizer = sr.Recognizer()
        with sr.AudioFile(filepath) as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data)
                st.session_state.transcript = text
                st.session_state.filename = filename
                save_transcript(text, filename)
                st.success("✅ Transcription completed successfully!")
            except sr.UnknownValueError:
                st.error("Could not understand the audio.")
            except sr.RequestError:
                st.error("Recognition service error.")

# --- Display Transcript ---
if st.session_state.transcript:
    st.subheader("📝 Transcription")
    segments = st.session_state.transcript.split(". ")
    for i, line in enumerate(segments):
        role = "Operator" if i % 2 == 0 else "Client"
        tags = extract_tags(line)
        st.markdown(f"""
            <div class="chat-bubble {'operator' if role=='Operator' else 'client'}">
                <b>{role}:</b> {line.strip()}<br/>
                {"".join([f'<span class="tag">{t}</span>' for t in tags])}
            </div>
        """, unsafe_allow_html=True)

    transcript_text = st.session_state.transcript
    transcript_filename = st.session_state.filename.replace(" ", "_")

    st.download_button("📄 Download as TXT", transcript_text, file_name=transcript_filename.replace(".wav", ".txt"))
    st.download_button("📄 Download as CSV", pd.DataFrame({"Transcript": [transcript_text]}).to_csv(index=False), file_name=transcript_filename.replace(".wav", ".csv"))