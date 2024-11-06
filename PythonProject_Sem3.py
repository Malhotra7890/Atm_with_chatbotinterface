import tkinter as tk
from tkinter import messagebox

class ATM:
    def __init__(self, balance=0):
        self.balance = balance

    def check_balance(self):
        return f"Your current balance is: ₹{self.balance:.2f}"

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return f"₹{amount:.2f} has been deposited successfully."
        else:
            return "Invalid deposit amount."

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            return f"₹{amount:.2f} has been withdrawn successfully."
        elif amount > self.balance:
            return "Insufficient balance."
        else:
            return "Invalid withdrawal amount."

class ChatBot:
    def __init__(self):
        # Rephrased responses with clearer question formatting
        self.responses = {
            "what is the customer care number?": "Our customer care number is 1800-123-456.",
            "how can i apply for a credit card?": "You can apply for a credit card through our website or at the nearest branch.",
            "how can i apply for a debit card?": "You can apply for a debit card by visiting the nearest branch with your ID and account details.",
            "what is the interest rate on savings accounts?": "The current interest rate on savings accounts is 3.5% per annum.",
            "how can i reset my atm pin?": "To reset your ATM PIN, visit our ATM and select 'PIN Change' or call customer care for assistance."
        }

    def get_response(self, query):
        query = query.lower()
        for key in self.responses:
            if key in query:
                return self.responses[key]
        return "Sorry, I don't understand that question."

def start_atm():
    def check_balance():
        result = atm.check_balance()
        result_label.config(text=result)

    def deposit_money():
        try:
            amount = float(deposit_entry.get())
            result = atm.deposit(amount)
            result_label.config(text=result)
        except ValueError:
            result_label.config(text="Invalid input. Please enter a valid number.")

    def withdraw_money():
        try:
            amount = float(withdraw_entry.get())
            result = atm.withdraw(amount)
            result_label.config(text=result)
        except ValueError:
            result_label.config(text="Invalid input. Please enter a valid number.")

    def chat():
        user_question = chat_entry.get()
        response = chatbot.get_response(user_question)
        chat_response_label.config(text=response)

    def verify_pin():
        if pin_entry.get() == "1234":  # For demonstration, PIN is "1234"
            pin_frame.pack_forget()  # Hide PIN frame
            atm_interface()  # Show ATM interface
        else:
            messagebox.showerror("Invalid PIN", "The PIN entered is incorrect.")

    def atm_interface():
        # ATM Interface frame
        atm_frame = tk.Frame(root, padx=20, pady=20, borderwidth=5, relief="solid")
        atm_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(atm_frame, text="NCU Bank", font=("Arial", 18)).pack()

        # Check balance button
        check_button = tk.Button(atm_frame, text="Check Balance", command=check_balance, font=("Arial", 14), width=20, height=2)
        check_button.pack(pady=10)

        # Deposit section
        global deposit_entry
        deposit_label = tk.Label(atm_frame, text="Deposit Amount:", font=("Arial", 12))
        deposit_label.pack()
        deposit_entry = tk.Entry(atm_frame, font=("Arial", 14), width=20, borderwidth=5, relief="solid")
        deposit_entry.pack()
        deposit_button = tk.Button(atm_frame, text="Deposit", command=deposit_money, font=("Arial", 14), width=20, height=2)
        deposit_button.pack(pady=10)

        # Withdraw section
        global withdraw_entry
        withdraw_label = tk.Label(atm_frame, text="Withdraw Amount:", font=("Arial", 12))
        withdraw_label.pack()
        withdraw_entry = tk.Entry(atm_frame, font=("Arial", 14), width=20, borderwidth=5, relief="solid")
        withdraw_entry.pack()
        withdraw_button = tk.Button(atm_frame, text="Withdraw", command=withdraw_money, font=("Arial", 14), width=20, height=2)
        withdraw_button.pack(pady=10)

        # Exit button
        exit_button = tk.Button(atm_frame, text="Exit", command=root.quit, font=("Arial", 14), width=20, height=2)
        exit_button.pack(pady=10)

        # Result display
        global result_label
        result_label = tk.Label(atm_frame, text="", font=("Arial", 14), fg="green")
        result_label.pack(pady=10)

        # Chatbot Frame at bottom right
        chat_frame = tk.Frame(root, padx=10, pady=10, borderwidth=5, relief="solid")
        chat_frame.place(relx=1.0, rely=1.0, anchor="se")

        tk.Label(chat_frame, text="Chat with ATM Bot", font=("Arial", 16)).pack()

        # Chat entry
        global chat_entry
        chat_entry = tk.Entry(chat_frame, font=("Arial", 12), width=30, borderwidth=3, relief="solid")
        chat_entry.pack(pady=10)

        # Chat button
        chat_button = tk.Button(chat_frame, text="Ask", command=chat, font=("Arial", 12), width=10, height=1)
        chat_button.pack()

        # Chatbot response
        global chat_response_label
        chat_response_label = tk.Label(chat_frame, text="", font=("Arial", 12), fg="red")
        chat_response_label.pack(pady=10)

    # Set up the main window
    root = tk.Tk()
    root.title("ATM with Chatbot Interface")

    atm = ATM(1000)  # Starting balance
    chatbot = ChatBot()

    # PIN entry frame
    pin_frame = tk.Frame(root, padx=20, pady=20, borderwidth=5, relief="solid")
    pin_frame.pack()

    tk.Label(pin_frame, text="Welcome to ATM System", font=("Arial", 18)).pack()
    tk.Label(pin_frame, text="Enter Account Holder Name:", font=("Arial", 12)).pack()
    name_entry = tk.Entry(pin_frame, font=("Arial", 14), borderwidth=3, relief="solid")
    name_entry.pack()

    tk.Label(pin_frame, text="Enter Account Number:", font=("Arial", 12)).pack()
    account_number_entry = tk.Entry(pin_frame, font=("Arial", 14), borderwidth=3, relief="solid")
    account_number_entry.pack()

    tk.Label(pin_frame, text="Enter PIN:", font=("Arial", 12)).pack()
    pin_entry = tk.Entry(pin_frame, show="*", font=("Arial", 14), borderwidth=3, relief="solid")
    pin_entry.pack()

    enter_button = tk.Button(pin_frame, text="Enter", command=verify_pin, font=("Arial", 14), width=15, height=2)
    enter_button.pack(pady=10)

    # Run the application
    root.mainloop()

if __name__ == "__main__":
    start_atm()
