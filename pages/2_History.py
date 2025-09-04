import streamlit as st
import os

st.set_page_config(page_title="Transcript History", layout="wide")
st.title("🕓 Transcript History")

transcript_dir = "transcripts"

if not os.path.exists(transcript_dir):
    st.info("No transcripts found.")
else:
    files = sorted(os.listdir(transcript_dir), reverse=True)
    if not files:
        st.info("No transcripts available.")
    else:
        for i, file in enumerate(files):
            filepath = os.path.join(transcript_dir, file)
            with open(filepath, "r") as f:
                content = f.read()
            st.subheader(f"📄 {file}")
            st.text_area("Transcript", content, height=150, key=f"transcript_{i}")
