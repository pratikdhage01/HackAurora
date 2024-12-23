# -*- coding: utf-8 -*-
"""emotion_analyzer.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1DVTfUoWSKxymeYmIgoeZA_YSPGcXxnfv
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import joblib
from sklearn.metrics import classification_report
from twilio.rest import Client

!pip uninstall -y twilio
!pip install twilio

data = {
    'text': [
        # Happy
        "This is great!",
        "I'm so satisfied with the service.",
        "Everything is fantastic.",
        "I had a wonderful experience.",
        "I am really happy about the result.",
        "Such a delightful experience.",
        # Anger
        "I am furious about the delay.",
        "I'm so angry with the customer support.",
        "This is completely unacceptable!",
        "I cannot believe how bad this is.",
        "I'm extremely upset with this situation.",
        # Sad
        "I feel very sad about what happened.",
        "I'm really down right now.",
        "This situation makes me feel hopeless.",
        "I am not feeling great today.",
        "I'm disappointed with the way things turned out.",
        # Frustration
        "I am frustrated with the process.",
        "This is so frustrating and annoying.",
        "I can't take this anymore!",
        "I'm tired of the issues I am facing.",
        "This is not what I expected.",
    ],
    'emotion': [
        'happy', 'happy', 'happy', 'happy', 'happy', 'happy',
        'anger', 'anger', 'anger', 'anger', 'anger',
        'sad', 'sad', 'sad', 'sad', 'sad',
        'frustration', 'frustration', 'frustration', 'frustration', 'frustration'
    ]
}

from twilio.rest import Client
print("Twilio Client imported successfully.")

df = pd.DataFrame(data)

X = df['text']
y = df['emotion']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = make_pipeline(TfidfVectorizer(), MultinomialNB())
model.fit(X_train, y_train)

joblib.dump(model, 'emotion_analysis_model.pkl')

# Evaluate the model for better feedback
predictions = model.predict(X_test)
print("Classification Report:\n", classification_report(y_test, predictions))

def analyze_emotion(text):
    loaded_model = joblib.load('emotion_analysis_model.pkl')
    emotion = loaded_model.predict([text])[0]
    return emotion

def customer_service_redirect(text):
    emotion = analyze_emotion(text)
    print(f"Detected emotion: {emotion}")
    if emotion in ['anger', 'sad', 'frustration']:
        print("Redirecting to human customer service assistance...")
        # Twilio redirection to customer service representative
        account_sid = 'AC9a92fb145463e2602d4de6adc6dcf00e'  # Replace with your Twilio Account SID
        auth_token = '2dc0212445f7c223cd400f4bc493a3eb'    # Replace with your Twilio Auth Token
        client = Client(account_sid, auth_token)

        # Customer's phone number that requires assistance
        customer_phone_number = '+1123456789'  # Replace with the customer's phone number
        customer_service_number = '+0987654321'  # Replace with your customer service representative number

        # Initiating a call to the customer, and then dialing the customer service number
        call = client.calls.create(
            twiml=f'''
                <Response>
                    <Say>Your emotion has been detected as {emotion}. We are now connecting you with a customer service representative.</Say>
                    <Dial>{customer_service_number}</Dial>
                </Response>
            ''',
            from_='+12185035414',  # Replace with your Twilio phone number
            to=customer_phone_number  # Calling the customer
        )
        print(f"Call initiated to the customer: {call.sid}")
    else:
        print("No redirection needed. Emotion is neutral or positive.")

def main():
    test_inputs = [
        "I am not satisfied",
    ]
    for input_text in test_inputs:
        print(f"Input: {input_text}")
        customer_service_redirect(input_text)

if __name__ == "__main__":
    main()