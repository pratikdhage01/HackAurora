import base64
import io
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from pydub import AudioSegment
import speech_recognition as sr
import spacy
import mysql.connector
from datetime import datetime
db = mysql.connector.connect(host="localhost", user="root", password="1Y@gtHkg", database="bank_db")
cursor = db.cursor()

app = Flask(__name__)
CORS(app)

# Load NLP model
nlp = spacy.load("en_core_web_sm")

intent = ""

# Convert any audio file to WAV format
def convert_to_wav(input_audio_path):
    audio = AudioSegment.from_file(input_audio_path)
    wav_path = "temp.wav"
    audio.export(wav_path, format="wav")
    return wav_path

# Convert audio file to text using the SpeechRecognition library
def convert_audio_to_text(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand the audio."
    except sr.RequestError as e:
        return f"Error with the recognition service: {e}"

# Process the text to determine the intent
def process_text(text):
    doc = nlp(text)
    if "pay" in text and "bill" in text:
        return "pay_bill"
    elif "check" in text and "balance" in text:
        return "check_balance"
    elif "transfer" in text or "send" in text:
        return "transfer_money"

    elif "mutual fund" in text or "advice" in text or "investment" in text:
        return "mutual_funds"

    elif "add" in text and "money" in text:
        return "add_money"
    elif "withdraw" in text and "money" in text:
        return "withdraw_money"
    return "unknown"

# Execute the task based on the intent
def execute_task(intent):
    if intent == "pay_bill":
        print(f"Detected intent: {intent}")
        pay_bill()
    elif intent == "check_balance":
        print(f"Detected intent: {intent}")
        check_balance()
    elif intent == "transfer_money":
        print(f"Detected intent: {intent}")
        transfer_money()
    elif intent == "mutual_funds":
        print(f"Detected intent: {intent}")
        mutual_funds()
    elif intent == "add_money":
        print(f"Detected intent: {intent}")
        add_money()
    elif intent == "withdraw_money":
        print(f"Detected intent: {intent}")
        withdraw_money()
    else:
        print("Intent not recognized.")

def pay_bill():
    intent = "Paying bill"
    print("Paying bill...")

def check_balance():
    intent = "Checking balance"
    print("Checking balance...")

def transfer_money(sender_id=1, receiver_id=2, amount=20):
        
    try:
        # Start transaction
        db.start_transaction()

        # Check if sender has enough balance
        cursor.execute("SELECT Balance FROM Users WHERE UserID = %s", (sender_id,))
        sender_balance = cursor.fetchone()[0]
        if sender_balance < amount:
            raise ValueError("Insufficient funds")

        # Deduct from sender
        cursor.execute("UPDATE Users SET Balance = Balance - %s WHERE UserID = %s", (amount, sender_id))

        # Add to receiver
        cursor.execute("UPDATE Users SET Balance = Balance + %s WHERE UserID = %s", (amount, receiver_id))

        # Log the transaction in the Transactions table
        cursor.execute("""
            INSERT INTO Transactions (SenderID, ReceiverID, Amount)
            VALUES (%s, %s, %s)
        """, (sender_id, receiver_id, amount))

        # Commit transaction
        db.commit()
        print(f"Transferred {amount} from User {sender_id} to User {receiver_id}")

    except Exception as e:
        db.rollback()
        print(f"Transaction failed: {e}")

def mutual_funds():
    intent = "Mutual funds"
    print("Mutual funds...")

def add_money():
    intent = "Adding money"
    print("Adding money...")

def withdraw_money():
    intent = "Withdrawing money"
    print("Withdrawing money...")

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
        
        # Save the audio data as a temporary file
        temp_audio_path = "temp_audio.m4a"
        with open(temp_audio_path, "wb") as f:
            f.write(audio_bytes)

        # Convert to WAV format
        wav_path = convert_to_wav(temp_audio_path)
        
        # Perform speech recognition
        transcription = convert_audio_to_text(wav_path)
        print(f"Transcription: {transcription}")

        # Process text and determine the intent
        intent = process_text(transcription)
        
        # Execute the task based on the intent
        execute_task(intent)

        if intent == "pay_bill":
            transcription = "Paying bill"   
        elif intent == "check_balance":
            transcription = "Checking balance"
        elif intent == "transfer_money":
            transcription = "Transferring money"
        elif intent == "mutual_funds":
            transcription = "Mutual funds"
        elif intent == "add_money":
            transcription = "Adding money"
        elif intent == "withdraw_money":
            transcription = "Withdrawing money"
        else:
            transcription = "Unknown intent"
        # Clean up temporary audio and wav files
        os.remove(temp_audio_path)
        os.remove(wav_path)

        return jsonify({"reply": transcription})

    except Exception as e:
        print(f"Error processing audio: {e}")
        return jsonify({"reply": "Sorry, there was an error processing the audio."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)