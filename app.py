# app.py
import speech_recognition as sr
from flask import Flask, request, jsonify
from gtts import gTTS
import os

app = Flask(__name__)

# Speech-to-Text function
def recognize_speech(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Sorry, I didn't catch that."
        except sr.RequestError:
            return "Could not request results from Google Speech Recognition service."

@app.route('/process_audio', methods=['POST'])
def process_audio():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file found"}), 400
    
    audio_file = request.files['audio']
    command_text = recognize_speech(audio_file)
    
    response_text = process_command(command_text)
    
    tts = gTTS(response_text)
    tts.save("response.mp3")
    
    return jsonify({"command": command_text, "response": response_text})

def process_command(command):
    if "weather" in command:
        return "The weather today is sunny with a high of 25°C."
    elif "news" in command:
        return "Here are today's top headlines..."
    else:
        return "I didn't understand that command."

if __name__ == '__main__':
    app.run(debug=True)
