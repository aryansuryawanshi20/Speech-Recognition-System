# analysis_page.py
import streamlit as st
from langdetect import detect
from collections import Counter
import re

# --------------------------
# Helper Functions
# --------------------------
def auto_detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"

def extract_keywords(text, top_n=5):
    words = re.findall(r'\w+', text.lower())
    common_words = [w for w in words if len(w) > 3]  # filter out very short words
    freq = Counter(common_words)
    return [word for word, _ in freq.most_common(top_n)]

def speaker_sentiment(transcript):
    # NOTE: Here it's just a placeholder (no AI model)
    speakers = {}
    for line in transcript.split("\n"):
        if ":" in line:
            speaker, speech = line.split(":", 1)
            speakers.setdefault(speaker.strip(), []).append("Neutral")  # default tag
    return speakers

# --------------------------
# Streamlit UI
# --------------------------
st.set_page_config(page_title="AI Text Analyzer", layout="wide")

st.title("🤖 AI Text Analyzer")

st.markdown("""
This page currently supports **fast features** (no heavy AI downloads):

- 🌍 Multi-language auto-detection
- 🔑 Keyword tagging
- 🎙️ Basic speaker sentiment (placeholder)

⚡ Advanced features like Summarization & Emotion Detection will be added soon!
""")

# Input box
text_input = st.text_area("Paste Transcript Here", height=250, placeholder="Enter text...")

if st.button("🔍 Analyze") and text_input.strip():
    # Language detection
    lang = auto_detect_language(text_input)
    st.success(f"🌍 Detected Language: **{lang.upper()}**")

    # Keyword tagging
    st.subheader("🔑 Keywords")
    keywords = extract_keywords(text_input, top_n=8)
    st.write(", ".join(keywords) if keywords else "No keywords found.")

    # Speaker sentiment
    st.subheader("🎙️ Speaker-wise Sentiment (Basic)")
    speakers = speaker_sentiment(text_input)
    if speakers:
        for spk, sents in speakers.items():
            st.write(f"**{spk}** → Neutral (placeholder)")
    else:
        st.write("No speakers detected (format should be like: `Speaker1: Hello`).")
