# Speech-to-Text API

## Overview  
This project is a **Flask-based speech recognition API** that converts spoken audio into text. Users can upload audio files, which are processed and transcribed using Google’s Speech Recognition API. The system supports **WAV, MP3, and M4A** formats and ensures compatibility by converting non-WAV files into PCM WAV format.  

## Features  
- Accepts **WAV, MP3, and M4A** audio files.  
- Converts non-WAV files into **PCM WAV** for better recognition.  
- Uses **Google Speech Recognition API** for transcription.  
- Handles ambient noise adjustments for improved accuracy.  
- Provides a **RESTful API** for speech-to-text conversion.  
- Supports **CORS**, allowing integration with frontend applications.  

## Technologies Used  
- **Python** (Flask Framework)  
- **SpeechRecognition** (Google Speech API)  
- **Pydub** (Audio processing & format conversion)  
- **Flask-CORS** (Cross-Origin Resource Sharing)  
- **Tempfile & OS** (File handling & temporary storage)  

## Project Workflow  

### 1. Upload Audio  
- User sends an audio file via **POST request**.  
- The server validates the file type (**WAV, MP3, or M4A**).  

### 2. Audio Processing  
- If needed, the audio is **converted to PCM WAV** format using **Pydub**.  
- Background noise adjustments are applied before recognition.  

### 3. Speech Recognition  
- The audio is transcribed using **Google Speech Recognition API**.  
- The recognized text is returned as a JSON response.  

## API Endpoints  

### 1. Home Route  
**`GET /`**  
- Serves the frontend HTML page.  

### 2. Speech-to-Text Conversion  
**`POST /speech-to-text`**  
- Accepts an audio file as input.  
- Returns transcribed text in JSON format.  
- Example Response:  
  ```json
  {
    "text": "Hello, how are you?"
  }
  ```  

## How to Use  

1. **Run the Flask App**  
   ```bash
   python app.py
   ```
2. **Send an Audio File via API**  
   - Use Postman, cURL, or a frontend app to send a **POST request** with an audio file.  
3. **Receive Transcribed Text**  
   - The API processes the audio and returns the recognized text.  

---

