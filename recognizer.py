#recognizer.py
import speech_recognition as sr

def recognize_audio_from_file(filepath):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(filepath) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
            return text
    except sr.UnknownValueError:
        return "Could not understand the audio."
    except sr.RequestError:
        return "Recognition service error."
    except Exception as e:
        return f"Error: {str(e)}"