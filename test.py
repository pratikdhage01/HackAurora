import mysql.connector
from datetime import datetime

# Connect to MySQL
db = mysql.connector.connect(host="localhost", user="root", password="1234", database="bank_db")
cursor = db.cursor()

# Function to transfer money
def transfer_money(sender_id, receiver_id, amount):
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

# Function to check current balance for a user
def check_balance(user_id):
    try:
        # Query to retrieve the user's current balance
        cursor.execute("SELECT Balance FROM Users WHERE UserID = %s", (user_id,))
        balance = cursor.fetchone()
        if balance:
            print(f"User {user_id}'s current balance is {balance[0]:.2f}.")
        else:
            print(f"User {user_id} not found.")
    except Exception as e:
        print(f"Error retrieving balance: {e}")

# Function to display total spending for a user in a specific month
def display_monthly_spending(user_id, month):
    try:
        # Query to calculate total spending in the given month
        cursor.execute("""
            SELECT SUM(Amount) AS TotalSpent,
                   DATE_FORMAT(TransactionDate, '%M') as MonthName
            FROM Transactions 
            WHERE SenderID = %s AND MONTH(TransactionDate) = %s
            GROUP BY MonthName
        """, (user_id, month))

        result = cursor.fetchone()
        total_spent = result[0] if result else 0.00  # Handle case where no transactions exist
        month_name = result[1] if result else datetime.strptime(str(month), "%m").strftime("%B")
        print(f"User {user_id} spent a total of {total_spent:.2f} in {month_name}.")
    except Exception as e:
        print(f"Error retrieving monthly spending: {e}")

# Function to display transaction history for a user
def display_transactions(user_id):
    cursor.execute("""
        SELECT * FROM Transactions 
        WHERE SenderID = %s OR ReceiverID = %s
        ORDER BY TransactionDate DESC
    """, (user_id, user_id))
    
    transactions = cursor.fetchall()
    if not transactions:
        print(f"No transactions found for User {user_id}.")
    else:
        for transaction in transactions:
            print(f"Transaction ID: {transaction[0]}, Sender: {transaction[1]}, Receiver: {transaction[2]}, Amount: {transaction[3]}, Date: {transaction[4]}")

# Test the functions
transfer_money(2, 1, 50.00)  # Example transaction
check_balance(1)  # Check balance for User 1
print("\nMonthly Spending for User 1:")
display_monthly_spending(1, datetime.now().month)  # Display spending for the current month

print("\nTransactions for User 1:")
display_transactions(1)  # Display transactions for User 1

# Close the connection
cursor.close()
db.close()
