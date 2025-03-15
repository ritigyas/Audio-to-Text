import speech_recognition as sr         # for converting speech to text
import os                               # to interact with the operating system (CREATING NEW DIR -- saves audio files)
import tempfile                         # Creates temporary files for audio processing
from flask import Flask, request, jsonify, render_template      # web framework to create the backend server
from flask_cors import CORS             # Allows frontend applications (like JS) to make API calls to this Flask server
from pydub import AudioSegment          # library for processing and converting audio files
from pydub.utils import which

app = Flask(__name__)
CORS(app)

# Ensure Pydub finds ffmpeg
AudioSegment.converter = which("ffmpeg")

r = sr.Recognizer()  # Initialize Speech Recognizer

# Set custom temp directory path
TEMP_AUDIO_DIR = "temp_audio_files"
os.makedirs(TEMP_AUDIO_DIR, exist_ok=True)

def convert_to_pcm_wav(audio_path):
    """Convert uploaded audio file to PCM WAV format using pydub."""
    try:
        audio = AudioSegment.from_file(audio_path)  # Load audio
        pcm_wav_path = os.path.splitext(audio_path)[0] + '_pcm.wav'  # New file path
        audio.export(pcm_wav_path, format="wav", parameters=["-acodec", "pcm_s16le"])
        return pcm_wav_path
    except Exception as e:
        print(f"Error during conversion: {str(e)}")
        return None

def record_text_from_file(audio_path):
    """Convert speech to text from an uploaded audio file."""
    try:
        if not audio_path.lower().endswith(".wav"):
            audio_path = convert_to_pcm_wav(audio_path)
            if not audio_path:
                return "Error during audio conversion."

        with sr.AudioFile(audio_path) as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio_data = r.record(source)
        return r.recognize_google(audio_data)
    except sr.RequestError as e:
        return f"API request error: {e}"
    except sr.UnknownValueError:
        return "Could not recognize speech from file."

@app.route('/')
def index():
    """Serve the frontend HTML page"""
    return render_template('index.html')

@app.route('/speech-to-text', methods=['POST'])
def speech_to_text():
    """API endpoint for file upload"""
    if 'audio' in request.files:
        audio_file = request.files['audio']

        if not audio_file.filename.lower().endswith(('.wav', '.mp3', '.m4a')):
            return jsonify({"error": "Invalid file type. Please upload a WAV, MP3, or M4A file."}), 400

        with tempfile.NamedTemporaryFile(delete=False, dir=TEMP_AUDIO_DIR, suffix=".wav") as temp_audio:
            try:
                audio_file.save(temp_audio.name)
                print(f"Saved file to {temp_audio.name}")

                converted_audio_path = convert_to_pcm_wav(temp_audio.name)
                if not converted_audio_path:
                    return jsonify({"error": "Audio conversion failed."}), 500

                print(f"Converted audio path: {converted_audio_path}")

                text = record_text_from_file(converted_audio_path)
                print(f"Recognized Text: {text}")

                return jsonify({"text": text})
            except Exception as e:
                print(f"Error: {str(e)}")
                return jsonify({"error": f"Error processing file: {str(e)}"}), 500

    return jsonify({"error": "No audio file provided"}), 400

if __name__ == '__main__':
    app.run(debug=True)
