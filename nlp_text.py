import spacy

# Load NLP model
nlp = spacy.load("en_core_web_sm")


def process_text(text):
    text = text.lower()  # Convert text to lowercase
    doc = nlp(text)
    # Example: Check for specific intents
    if "pay" in text and "bill" in text:
        print("Detected intent: pay_bill")
        return "pay_bill"
    elif "check" in text and "balance" in text:
        print("Detected intent: check_balance")
        return "check_balance"
    elif "transfer" in text or "send" in text:
        print("Detected intent: transfer_money")
        return "transfer_money"
    elif "investment advice" in text:  # Check for exact phrase
        print("Detected intent: investment_advice")
        return "investment_advice"
    # Add more intents as needed
    print("Detected intent: unknown")
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
text_input = "Send Rs. 100 to dev."
intent = process_text(text_input)
execute_task(intent)


