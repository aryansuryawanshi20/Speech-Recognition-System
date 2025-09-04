#utils.py
import os

def extract_tags(text):
    """
    Extracts simple tags based on keywords.
    You can expand this with NLP or regex for more accuracy.
    """
    keywords = {
        "error": "Error",
        "issue": "Issue",
        "payment": "Payment",
        "login": "Login",
        "disconnect": "Disconnect",
        "support": "Support"
    }
    tags = [tag for key, tag in keywords.items() if key in text.lower()]
    return tags


def save_transcript(text, filename):
    """
    Saves the transcript to the 'transcripts' directory as a text file.
    """
    os.makedirs("transcripts", exist_ok=True)
    base = os.path.splitext(os.path.basename(filename))[0]
    file_path = os.path.join("transcripts", f"{base}.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text)