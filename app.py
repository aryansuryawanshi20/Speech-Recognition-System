import streamlit as st
from pathlib import Path
import base64

# Hide default sidebar completely
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
hide_st_style = """
    <style>
    [data-testid="stSidebar"] {display: none;}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# Inject custom CSS
def load_custom_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load CSS
load_custom_css("styles/home.css")

# Bubbles
# Add decorative layers
st.markdown("""
<div class="bubbles">
    <span></span><span></span><span></span>
    <span></span><span></span><span></span>
</div>
<div class="curved-section"></div>
<div class="circle-deco"></div>
""", unsafe_allow_html=True)


# Load and encode image
def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

image_base64 = get_base64_image("static/image.jpg")
image_html = f"data:image/jpeg;base64,{image_base64}"

# Custom Top Navbar (with button-style links)
st.markdown("""
<div class="navbar">
    <div class="nav-right">
        <a href="/?page=Home" class="nav-item">Home</a>
        <a href="/Transcription" class="nav-item">Transcription</a>
        <a href="/History" class="nav-item">History</a>
        <a href="/Analysis" class="nav-item">Analysis</a>
        <a href="/Info" class="nav-item">Info</a> <!-- Link to Info page -->
    </div>
</div>
""", unsafe_allow_html=True)

# Hero Section with "Learn more" button
st.markdown(f"""
<div class="hero">
    <div class="hero-left">
        <h1>Voice Recognition</h1>
        <p>Transform your voice into powerful actions. Explore the future of seamless voice recognition with cutting-edge accuracy and speed.</p>
        <a href="/Info" class="learn-btn">Learn more</a>
    </div>
    <div class="hero-right">
        <img src="{image_html}" alt="Voice Illustration" class="hero-img">
    </div>
</div>
""", unsafe_allow_html=True)
