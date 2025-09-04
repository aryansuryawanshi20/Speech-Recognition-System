import streamlit as st

# Inject custom CSS for Info Page
def load_custom_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load custom CSS
load_custom_css("styles/info.css")

# Info Page Content
st.markdown("""
    <div class="info-header">
        <h1>About Voice Recognition App</h1>
        <p>Our app uses cutting-edge voice recognition technology to provide real-time transcription.</p>
    </div>
    <div class="info-content">
        <h2>How It Works</h2>
        <p>This application allows users to upload audio files or record using their microphone. The voice input is transcribed into text using advanced machine learning models.</p>
        <h2>Features</h2>
        <ul>
            <li>Real-time transcription</li>
            <li>Support for multiple audio formats</li>
            <li>Text history and analysis</li>
        </ul>
        <h2>Technologies Used</h2>
        <p>Python, Streamlit, Speech Recognition API, Natural Language Processing (NLP)</p>
    </div>
""", unsafe_allow_html=True)
