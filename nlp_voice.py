from pydub import AudioSegment
from speech_recognition import Recognizer, AudioFile
import spacy
import os

# Load NLP model
nlp = spacy.load("en_core_web_sm")

def convert_to_wav(input_audio_path):
    # Convert any audio file to WAV format
    audio = AudioSegment.from_file(input_audio_path)
    wav_path = "temp.wav"
    audio.export(wav_path, format="wav")
    return wav_path

def convert_audio_to_text(audio_path):
    recognizer = Recognizer()
    with AudioFile(audio_path) as source:
        audio = recognizer.record(source)
    return recognizer.recognize_google(audio)

def process_text(text):
    doc = nlp(text)
    # Example: Check for specific intents
    if "pay" in text and "bill" in text:
        return "pay_bill"
    elif "check" in text and "balance" in text:
        return "check_balance"
    elif "transfer" in text or "send" in text:
        return "transfer_money"
    elif "investment" in text and "advice" in text:
        return "investment_advice"
    # Add more intents as needed
    return "unknown"

def execute_task(intent):
    if intent == "pay_bill":
        pay_bill()
    elif intent == "check_balance":
        check_balance()
    elif intent == "transfer_money":
        transfer_money()
    # elif intent == "investment_advice":
    #     provide_investment_advice()
    else:
        print("Intent not recognized.")

def pay_bill():
    # Placeholder for bill payment logic
    print("Paying bill...")

def check_balance():
    # Placeholder for balance checking logic
    print("Checking balance...")

def transfer_money():
    # Placeholder for money transfer logic
    print("Transferring money...")

# Example usage
audio_path = r"D:\Volume E VIIT\Projects and Hackathons Project\HackAurora1 VJTI\balance_check.m4a"
wav_path = convert_to_wav(audio_path)
text = convert_audio_to_text(wav_path)
intent = process_text(text)
execute_task(intent)

# Clean up temporary WAV file
os.remove(wav_path)
