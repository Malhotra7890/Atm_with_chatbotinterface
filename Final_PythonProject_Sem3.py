import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import json


# Initialize the main window
root = tk.Tk()
root.title("ATM Interface")
root.geometry("500x600")  # Adjusting the window size

# Database (simulating with a dictionary)
account_database = {
    'Viraj Yadav': {'account_number': '57963', 'pin': '4567', 'balance': 10000},
    'Vedant Malhotra': {'account_number': '89347', 'pin': '1234', 'balance': 15000},
    'Dhyanesh Sharma': {'account_number': '69834', 'pin': '8974', 'balance': 20000},
}

# Save account database to a file
def save_account_database():
    with open("account_database.json", "w") as file:
        json.dump(account_database, file)

# Load account database from a file
def load_account_database():
    global account_database
    try:
        with open("account_database.json", "r") as file:
            account_database = json.load(file)
    except FileNotFoundError:
        # If file doesn't exist, use the default database
        pass

# Load the database at the start of the program
load_account_database()

# Transaction history to store deposits and withdrawals
transaction_history = []

# Chatbot responses
chatbot_responses = {
    "hi": "Hello! How can I assist you today?",
    "hello": "Hi there! How can I help?",
    "what is the customer care number?": "Our customer care number is 1800-123-456.",
    "how can i apply for a credit card?": "You can apply for a credit card through our website or at the nearest branch.",
    "how can i apply for a debit card?": "You can apply for a debit card by visiting the nearest branch with your ID and account details.",
    "what is the interest rate on savings accounts?": "The current interest rate on savings accounts is 3.5% per annum.",
    "how can i reset my atm pin?": "To reset your ATM PIN, visit our ATM and select 'PIN Change' or call customer care for assistance.",
    "how to apply for a checkbook?": "You can apply for a checkbook by visiting the nearest branch or by logging into your online banking account.",
    "how to apply for a loan?": "To apply for a loan, you can visit the nearest branch or apply online by filling out the loan application form."
}

# Define a global variable to store account information (initialized to None initially)
account_info = None

# Function to validate login credentials using the account database
def validate_login():
    global account_info
    name = entry_name.get()
    account_number = entry_account.get()
    pin = entry_pin.get()

    # Check if the account holder exists in the "database"
    if name in account_database:
        account_data = account_database[name]
        if account_data['account_number'] == account_number and account_data['pin'] == pin:
            account_info = account_data
            account_info['name'] = name  # Store the name for later reference
            show_atm_interface()
        else:
            messagebox.showerror("Error", "Invalid account number or PIN. Please try again.")
    else:
        messagebox.showerror("Error", "Account holder not found. Please try again.")

# Function to display ATM options
def show_atm_interface():
    if account_info is None:
        messagebox.showerror("Error", "Please login first!")
        return

    login_frame.pack_forget()
    atm_frame.pack(fill='both', expand=True, padx=10, pady=10)
    label_welcome.config(text=f"Welcome {account_info['name']}!")

# Function to get the transaction file for the current user
def get_transaction_file():
    file_name = f"{account_info['account_number']}_history.txt"
    print(f"Transaction file: {file_name}")  # Debug: Check file path
    return file_name



# Function to handle withdrawals
def withdraw_amount():
    global account_database
    amount = withdraw_entry.get().strip()
    if not amount.isdigit() and not is_float(amount):
        messagebox.showerror("Error", "Please enter a valid numeric amount.")
        return
    amount = float(amount)
    if amount <= 0:
        messagebox.showerror("Error", "Amount must be greater than zero.")
        return
    if amount > account_info['balance']:
        messagebox.showerror("Error", "Insufficient balance.")
    else:
        account_info['balance'] -= amount
        transaction = f"Withdrew: ₹{amount} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        transaction_history.append(transaction)
        account_database[account_info['name']]['balance'] = account_info['balance']  # Update in database
        save_account_database()  # Save database to file
        with open(get_transaction_file(), "a", encoding="utf-8") as file:
            file.write(transaction)
        messagebox.showinfo("Success", f"₹{amount} withdrawn successfully.")
        withdraw_frame.pack_forget()
        show_atm_interface()


# Function to handle deposits
def deposit_amount():
    global account_database
    amount = deposit_entry.get().strip()
    if not amount.isdigit() and not is_float(amount):
        messagebox.showerror("Error", "Please enter a valid numeric amount.")
        return
    amount = float(amount)
    if amount <= 0:
        messagebox.showerror("Error", "Amount must be greater than zero.")
        return
    account_info['balance'] += amount
    transaction = f"Deposited: ₹{amount} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    transaction_history.append(transaction)
    account_database[account_info['name']]['balance'] = account_info['balance']  # Update in database
    save_account_database()  # Save database to file
    with open(get_transaction_file(), "a", encoding="utf-8") as file:
        file.write(transaction)
    messagebox.showinfo("Success", f"₹{amount} deposited successfully.")
    deposit_frame.pack_forget()
    show_atm_interface()


# Helper function to check if a string can be converted to a float
def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False



# Function to show transaction history
def show_transaction_history():
    try:
        with open(get_transaction_file(), "r",encoding="utf-8") as file:
            history_text = file.read()
    except FileNotFoundError:
        history_text = "No transactions yet for this account."
    messagebox.showinfo("Transaction History", history_text)

def sign_out():
    global account_info
    account_info = None  # Reset account information
    messagebox.showinfo("Logged Out", "You have successfully logged out.")
    login_frame.pack(fill='both', expand=True, padx=10, pady=10)  # Show login frame again
    atm_frame.pack_forget()  # Hide ATM interface
    chatbot_frame.pack_forget()  # Hide Chatbot interface

# Create login screen
login_frame = tk.Frame(root, bg="#333333")    

# Function to handle chatbot response
def process_chat_input():
    user_input = entry_chat.get().lower()
    response = chatbot_responses.get(user_input, "Hello! 😊 How can I assist you today? Feel free to ask me anything.")
    label_chatbot_response.config(text=response)
    entry_chat.delete(0, tk.END)

# Function to start chatbot interface
def start_chat():
    atm_frame.pack_forget()
    chatbot_frame.pack(fill='both', expand=True, padx=10, pady=10)

# Function to go back to ATM interface
def back_to_atm():
    chatbot_frame.pack_forget()
    withdraw_frame.pack_forget()
    deposit_frame.pack_forget()
    show_atm_interface()


# Create login screen
login_frame = tk.Frame(root, bg="#333333")

label_name = tk.Label(login_frame, text="Account Holder Name:", bg="#333333", fg="white", font=("Arial", 14, "bold"))
label_name.pack(pady=10)
entry_name = tk.Entry(login_frame, font=("Arial", 14), width=35)
entry_name.pack(pady=10)

label_account = tk.Label(login_frame, text="Account Number:", bg="#333333", fg="white", font=("Arial", 14, "bold"))
label_account.pack(pady=10)
entry_account = tk.Entry(login_frame, font=("Arial", 14), width=35)
entry_account.pack(pady=10)

label_pin = tk.Label(login_frame, text="PIN:", bg="#333333", fg="white", font=("Arial", 14, "bold"))
label_pin.pack(pady=10)
entry_pin = tk.Entry(login_frame, show="*", font=("Arial", 14), width=35)
entry_pin.pack(pady=10)

login_button = tk.Button(login_frame, text="Login", command=validate_login, font=("Arial", 16, "bold"), bg="#32CD32", fg="white", width=25, height=2)
login_button.pack(pady=20)
login_frame.pack(padx=10, pady=10)

# Create ATM interface
atm_frame = tk.Frame(root, bg="#333333")
label_welcome = tk.Label(atm_frame, text="Welcome!", font=("Arial", 20, "bold"), fg="white", bg="#333333")
label_welcome.pack(pady=30)

sign_out_button = tk.Button(atm_frame, text="Sign Out", command=sign_out, font=("Arial", 14, "bold"), bg="#FF6347", fg="white", width=10, height=1)
sign_out_button.place(x=1350, y=12)

balance_button = tk.Button(atm_frame, text="Check Balance", command=lambda: messagebox.showinfo("Balance", f"₹{account_info['balance']}"),
                            font=("Arial", 16, "bold"), bg="#FFCC00", fg="white", width=25, height=2)
balance_button.pack(pady=15)

withdraw_button = tk.Button(atm_frame, text="Withdraw Money", command=lambda: withdraw_frame.pack(fill='both', expand=True, padx=10, pady=10),
                             font=("Arial", 16, "bold"), bg="#FF6347", fg="white", width=25, height=2)
withdraw_button.pack(pady=15)

deposit_button = tk.Button(atm_frame, text="Deposit Money", command=lambda: deposit_frame.pack(fill='both', expand=True, padx=10, pady=10),
                            font=("Arial", 16, "bold"), bg="#32CD32", fg="white", width=25, height=2)
deposit_button.pack(pady=15)

history_button = tk.Button(atm_frame, text="Transaction History", command=show_transaction_history, font=("Arial", 16, "bold"), bg="#8A2BE2", fg="white", width=25, height=2)
history_button.pack(pady=15)

chat_button = tk.Button(atm_frame, text="Chat with ATM Assistant", command=start_chat, font=("Arial", 16, "bold"), bg="#4169E1", fg="white", width=25, height=2)
chat_button.pack(pady=15)

# Create Withdraw Frame using pack
withdraw_frame = tk.Frame(root)
withdraw_frame.pack_forget()  # Initially, don't show this frame

# Entry field for withdrawal amount
withdraw_entry = tk.Entry(withdraw_frame, font=("Arial", 14), width=35)
withdraw_entry.pack(pady=10)

# Confirm button for withdrawal
withdraw_button_confirm = tk.Button(withdraw_frame, text="Confirm Withdrawal", command=withdraw_amount, font=("Arial", 16, "bold"), bg="#FF6347", fg="white", width=25, height=2)
withdraw_button_confirm.pack(pady=5)

# Back button for withdrawal
back_button_withdraw = tk.Button(withdraw_frame, text="Back", command=back_to_atm, font=("Arial", 16, "bold"), bg="#8A2BE2", fg="white", width=25, height=2)
back_button_withdraw.pack(pady=5)

# Create Deposit Frame using pack
deposit_frame = tk.Frame(root)
deposit_frame.pack_forget()  # Initially, don't show this frame

# Entry field for deposit amount
deposit_entry = tk.Entry(deposit_frame, font=("Arial", 14), width=35)
deposit_entry.pack(pady=10)

# Confirm button for deposit
deposit_button_confirm = tk.Button(deposit_frame, text="Confirm Deposit", command=deposit_amount, font=("Arial", 16, "bold"), bg="#32CD32", fg="white", width=25, height=2)
deposit_button_confirm.pack(pady=5)

# Back button for deposit
back_button_deposit = tk.Button(deposit_frame, text="Back", command=back_to_atm, font=("Arial", 16, "bold"), bg="#8A2BE2", fg="white", width=25, height=2)
back_button_deposit.pack(pady=5)



# Create Chatbot Interface
chatbot_frame = tk.Frame(root, bg="#333333")

label_chatbot_title = tk.Label(chatbot_frame, text="ATM Assistant", font=("Arial", 20, "bold"), fg="white", bg="#333333")
label_chatbot_title.pack(pady=10)

label_chatbot_response = tk.Label(chatbot_frame, text="Hello! 😊 How can I assist you today?", font=("Arial", 14), fg="white", bg="#333333", wraplength=400)
label_chatbot_response.pack(pady=10)

entry_chat = tk.Entry(chatbot_frame, font=("Arial", 14), width=35)
entry_chat.pack(pady=10)

send_button = tk.Button(chatbot_frame, text="Send", command=process_chat_input, font=("Arial", 16, "bold"), bg="#32CD32", fg="white", width=25, height=2)
send_button.pack(pady=10)

back_button_chat = tk.Button(chatbot_frame, text="Back to ATM Interface", command=back_to_atm, font=("Arial", 16, "bold"), bg="#8A2BE2", fg="white", width=25, height=2)
back_button_chat.pack(pady=10)


# Start the Tkinter event loop
root.mainloop()