import base64
import io
from flask import Flask, request, jsonify
from flask_cors import CORS
from google.cloud import speech

app = Flask(__name__)
CORS(app)

# Initialize the Google Cloud Speech client
client = speech.SpeechClient()

@app.route('/', methods=['POST'])
def respond():
    data = request.json
    audio_data = data.get('audio', '')  # Get Base64 audio data
    
    if not audio_data:
        return jsonify({"reply": "No audio data received."})

    try:
        # Decode the Base64 audio data
        audio_bytes = base64.b64decode(audio_data)
        print(f"Decoded audio data length: {len(audio_bytes)} bytes")  # Check if data is complete

        # Use Google Cloud Speech API to recognize speech from the audio
        audio = speech.RecognitionAudio(content=audio_bytes)
        
        # Configure recognition settings
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,  # Change if needed
            sample_rate_hertz=16000,  # Ensure this matches the sample rate of your recording
            language_code="en-US",  # Change to your preferred language code
        )
        
        # Perform speech recognition
        response = client.recognize(config=config, audio=audio)

        # Log the response for debugging
        print(f"Google Cloud Speech response: {response}")

        if response.results:
            transcription = response.results[0].alternatives[0].transcript
        else:
            transcription = "Sorry, I couldn't understand that."

        return jsonify({"reply": transcription})

    except Exception as e:
        print(f"Error processing audio: {e}")
        return jsonify({"reply": "Sorry, there was an error processing the audio."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
