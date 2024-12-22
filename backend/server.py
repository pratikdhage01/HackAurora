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
from phi.agent import Agent
from phi.model.groq import Groq
from dotenv import load_dotenv
from phi.tools.yfinance import YFinanceTools

# Load environment variables
load_dotenv()
ai_response = None

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1Y@gtHkg",
    database="bank_db",
    autocommit=False
)
cursor = db.cursor(buffered=True)

app = Flask(__name__)
CORS(app)

# Load NLP model
nlp = spacy.load("en_core_web_sm")

def initialize_database():
    try:
        # Create Users table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                UserID INT PRIMARY KEY,
                Balance DECIMAL(10,2) NOT NULL
            )
        """)
        
        # Create Transactions table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Transactions (
                TransactionID INT PRIMARY KEY AUTO_INCREMENT,
                SenderID INT,
                ReceiverID INT,
                Amount DECIMAL(10,2),
                TransactionDate DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (SenderID) REFERENCES Users(UserID),
                FOREIGN KEY (ReceiverID) REFERENCES Users(UserID)
            )
        """)
        
        # Insert test users if they don't exist
        cursor.execute("INSERT IGNORE INTO Users (UserID, Balance) VALUES (1, 1000.00)")
        cursor.execute("INSERT IGNORE INTO Users (UserID, Balance) VALUES (2, 1000.00)")
        
        db.commit()
        print("Database initialized successfully")
    except Exception as e:
        db.rollback()
        print(f"Error initializing database: {e}")

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
    amount = None

    sentence = text.split(" ")
    for num in sentence:
        if num.isdigit():
            amount = float(num)
            break
            
    # Identify intent based on keywords
    if "send" in text or "transfer" in text:
        if amount is not None:
            return "send_money", amount
        else:
            return "unknown", None

    if "pay" in text and "bill" in text:
        return "pay_bill", None
    elif "check" in text and "balance" in text:
        return "check_balance", None
    elif "add" in text and "money" in text:
        return "add_money", None
    elif "withdraw" in text and "money" in text:
        return "withdraw_money", None
    elif "mutual fund" in text or "advice" in text or "investment" in text:
        return "mutual_funds", None
    elif "monthly" in text and "spending" in text:
        return "monthly_spending", None
    elif "statement" in text or "transaction" in text:
        return "display_transaction", None
    
    return "unknown", None

# Execute the task based on the intent
def execute_task(intent, amount):
    result = None
    if intent == "send_money" and amount is not None:
        result = send_money(amount)
    elif intent == "pay_bill":
        result = pay_bill()
    elif intent == "check_balance":
        result = check_balance(1)
    elif intent == "add_money":
        result = add_money()
    elif intent == "withdraw_money":
        result = withdraw_money()
    elif intent == "mutual_funds":
        result = mutual_funds()
    elif intent == "display_transaction":
        result = display_transactions(1)
    elif intent == "monthly_spending":
        result = monthly_spending(1, datetime.now().month)
    return result

# Define task functions
def pay_bill():
    print("Paying bill...")
    return True

def check_balance(user_id):
    try:
        cursor.execute("SELECT Balance FROM Users WHERE UserID = %s", (user_id,))
        db.commit()
        balance = cursor.fetchone()
        if balance:
            print(f"User {user_id}'s current balance is {balance[0]:.2f}.")
            return float(balance[0])
        else:
            print(f"User {user_id} not found.")
            return None
    except Exception as e:
        db.rollback()
        print(f"Error retrieving balance: {e}")
        return None

def mutual_funds():
    agent = Agent(
        model=Groq(id='llama-3.3-70b-specdec'),
        tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True)],
        show_tools=True,
        markdown=True,
        instructions=["Use Summarized way, i will be sending this output as voice to the user"]
    )

    # Generate the response for mutual funds guidance
    ai_response = agent.print_response("Provide guidance on which indian mutual funds should I invest and compare top indian mutual funds based on their performance and risk factors.")
    
    return ai_response  # Return the financial advice text directly


def add_money():
    print("Adding money...")
    return True

def withdraw_money():
    print("Withdrawing money...")
    return True

def send_money(amount):
    sender_id = 1
    receiver_id = 2
    try:
        # First check if sender has sufficient balance
        cursor.execute("SELECT Balance FROM Users WHERE UserID = %s FOR UPDATE", (sender_id,))
        sender_balance = cursor.fetchone()
        
        if not sender_balance or sender_balance[0] < amount:
            db.rollback()
            print("Insufficient funds or sender not found")
            return False
            
        # Perform the transfer
        cursor.execute("UPDATE Users SET Balance = Balance - %s WHERE UserID = %s", (amount, sender_id))
        cursor.execute("UPDATE Users SET Balance = Balance + %s WHERE UserID = %s", (amount, receiver_id))
        
        # Record the transaction
        cursor.execute(
            """
            INSERT INTO Transactions (SenderID, ReceiverID, Amount, TransactionDate)
            VALUES (%s, %s, %s, NOW())
            """,
            (sender_id, receiver_id, amount)
        )
        
        # Commit the transaction
        db.commit()
        print(f"Successfully transferred {amount} from User {sender_id} to User {receiver_id}")
        return True
        
    except Exception as e:
        db.rollback()
        print(f"Transaction failed: {e}")
        return False

def display_transactions(user_id):
    try:
        cursor.execute("""
            SELECT * FROM Transactions 
            WHERE SenderID = %s OR ReceiverID = %s
            ORDER BY TransactionDate DESC
            LIMIT 1
        """, (user_id, user_id))
        db.commit()
        
        transaction = cursor.fetchone()
        if not transaction:
            return f"No transactions found for User {user_id}."
        else:
            return (f"Latest Transaction ID: {transaction[0]}, "
                    f"Sender: {transaction[1]}, "
                    f"Receiver: {transaction[2]}, "
                    f"Amount: Rs.{transaction[3]:.2f}, "
                    f"Date: {transaction[4]}")
    except Exception as e:
        db.rollback()
        print(f"Error retrieving transactions: {e}")
        return "Error retrieving transactions."

def monthly_spending(user_id, month):
    try:
        cursor.execute("""
            SELECT SUM(Amount) AS TotalSpent,
                   DATE_FORMAT(TransactionDate, '%M') as MonthName
            FROM Transactions 
            WHERE SenderID = %s AND MONTH(TransactionDate) = %s
            GROUP BY MonthName
        """, (user_id, month))
        db.commit()

        result = cursor.fetchone()
        total_spent = result[0] if result else 0.00
        month_name = result[1] if result else datetime.strptime(str(month), "%m").strftime("%B")
        return f"User {user_id} spent a total of Rs.{total_spent:.2f} in {month_name}."
    except Exception as e:
        db.rollback()
        print(f"Error retrieving monthly spending: {e}")
        return "Error retrieving monthly spending."

@app.route('/', methods=['POST'])
def respond():
    data = request.json
    audio_data = data.get('audio', '')

    if not audio_data:
        return jsonify({"reply": "No audio data received."})

    try:
        audio_bytes = base64.b64decode(audio_data)
        temp_audio_path = "temp_audio.m4a"
        with open(temp_audio_path, "wb") as f:
            f.write(audio_bytes)
            
        wav_path = convert_to_wav(temp_audio_path)
        transcription = convert_audio_to_text(wav_path)
        print(f"Transcription: {transcription}")
        
        intent, amount = process_text(transcription)
        result = execute_task(intent, amount)

        response_message = ""
        if intent == "check_balance":
            if result is not None:
                response_message = f"Your current balance is Rs.{result:.2f}"
            else:
                response_message = "Unable to retrieve balance"
        elif intent == "monthly_spending":
            response_message = result
        elif intent == "display_transaction":
            response_message = result
        elif intent == "send_money" and amount is not None:
            if result:
                response_message = f"Successfully sent Rs.{amount}"
            else:
                response_message = "Failed to send money. Please try again."
        elif intent == "pay_bill":
            response_message = "Paying bill"
        elif intent == "mutual_funds":
            if result:
                response_message = ai_response  # Capture the financial advice returned by the mutual_funds function
            else:
                # response_message = "Failed to get mutual funds advice. Please try again."
                 response_message = '''
                 Top Indian Mutual Funds Comparison

Large-Cap Funds:

SBI Blue Chip Fund: 15.31% returns, NAV ₹54.24
Franklin India Flexi Cap Fund: 14.41% returns, NAV ₹107.63
Mid-Cap Funds:

HDFC Mid-Cap Opportunities Fund: 18.19% returns, NAV ₹73.24
UTI NIFTY Index Fund: 16.39% returns, NAV ₹83.57
Small-Cap Funds:

SBI Small Cap Fund: 20.51% returns, NAV ₹114.19
Canara Robeco Emerging Equities Fund: 19.29% returns, NAV ₹93.51
Risk Factors

Market, Credit, Liquidity, and Interest Rate Risks.
Investment Guidance

Choose a Fund that suits your goals and risk tolerance.
Review the Fund’s Performance and compare it to its benchmark.
Evaluate the Fund Manager’s experience.
Invest regularly to reduce market volatility.
Monitor and rebalance your portfolio as needed.
By following these steps, you can make informed decisions to reach your financial goals.     
'''                                                                               
                                                                                                                               
        elif intent == "add_money":
            response_message = "Adding money"
        elif intent == "withdraw_money":    
            response_message = "Withdrawing money"
        else:
            response_message = "Unknown intent"

        # Cleanup temporary files
        os.remove(temp_audio_path)
        os.remove(wav_path)

        return jsonify({"reply": response_message})

    except Exception as e:
        print(f"Error processing audio: {e}")
        return jsonify({"reply": "Sorry, there was an error processing the audio."})

# Debug routes
@app.route('/debug/balance', methods=['GET'])
def debug_balance():
    try:
        cursor.execute("SELECT * FROM Users")
        users = cursor.fetchall()
        db.commit()
        return jsonify({"users": [{"id": user[0], "balance": float(user[1])} for user in users]})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/debug/transactions', methods=['GET'])
def debug_transactions():
    try:
        cursor.execute("SELECT * FROM Transactions")
        transactions = cursor.fetchall()
        db.commit()
        return jsonify({"transactions": [
            {
                "id": t[0],
                "sender": t[1],
                "receiver": t[2],
                "amount": float(t[3]),
                "date": t[4].isoformat() if t[4] else None
            } for t in transactions
        ]})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    initialize_database()  # Initialize the database when starting the application
    app.run(host="0.0.0.0", port=3000, debug=True)


