import getpass

class Bank:
    banks = {}  # Class variable all bank 

    def __init__(self, bank_name, ifsc_code, branch):
        self.bank_name = bank_name
        self.ifsc_code = ifsc_code
        self.branch = branch

    @classmethod
    def add_bank(cls, bank_name, ifsc_code, branch):
        if bank_name in cls.banks:
            print(f"Bank '{bank_name}' already exists.")
            return cls.banks[bank_name]
        new_bank = cls(bank_name, ifsc_code, branch)
        cls.banks[bank_name] = new_bank
        return new_bank

    @classmethod
    def get_bank(cls, bank_name):
        return cls.banks.get(bank_name)

class User:
    def __init__(self, name, account_number, balance, user_id, password, bank):
        self.name = name
        self.account_number = account_number
        self.balance = balance
        self.user_id = user_id
        self.password = password
        self.bank = bank  

    def deposit(self, amount):
        self.balance += amount
        print(f"Deposited {amount}. New Balance: {self.balance}")

    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient funds.")
            return False
        self.balance -= amount
        print(f"Withdrew {amount}. New Balance: {self.balance}")
        return True 

    def transfer(self, amount, recipient):
        if self.bank != recipient.bank:
            print("Error: Cannot transfer funds between different banks.")
            return
        if self.withdraw(amount):
            recipient.deposit(amount)
            print(f"Transferred {amount} to {recipient.name}")

    def authenticate(self, password):
        return self.password == password

def display_menu():
    print("\nChoose Below Option:")
    print("1. Deposit Money")
    print("2. Withdraw Money")
    print("3. Transfer Money")
    print("4. Check Balance")
    print("5. Exit")

def create_user(users):
    print("\nAvailable Banks:")
    for bank_name in Bank.banks:
        print(f"- {bank_name}")

    bank_name = input("Enter the Bank Name where you want to create a user: ")
    bank = Bank.get_bank(bank_name)
    
    if not bank:
        print("Bank not found. You need to create the bank first.")
        return

    user_name = input("Enter the Name for the new User: ")
    account_number = input("Enter the Account Number for the new User: ")
    balance = get_float_input("Enter the Initial Amount for the new User: ")
    user_id = input("Enter Username for the new User: ")
    
    while True:
        password = getpass.getpass("Enter Password for the new User: ")
        confirm_password = getpass.getpass("Confirm Password: ")
        if password == confirm_password:
            break
        else:
            print("Passwords do not match. Please try again.")

    new_user = User(user_name, account_number, balance, user_id, password, bank)
    users[user_id] = new_user
    print(f"User {user_name} created successfully in {bank_name}.")

def create_bank():
    bank_name = input("Enter the Bank Name: ")
    if Bank.get_bank(bank_name):
        print(f"Bank '{bank_name}' already exists.")
        return
    ifsc_code = input("Enter the IFSC Code: ")
    branch_name = input("Enter the Branch Name: ")
    Bank.add_bank(bank_name, ifsc_code, branch_name)
    print(f"Bank '{bank_name}' created successfully.")

def get_float_input(prompt):
    while True:
        try:
            value = float(input(prompt))
            return value
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

def perform_operation(users, operation):
    bank_name = input("Enter the Bank Name: ")
    bank = Bank.get_bank(bank_name)
    if not bank:
        print("Bank not found.")
        return

    user_id = input("Enter your User ID: ")
    user = users.get(user_id)
    
    if not user:
        print("Invalid user ID.")
        return

    if user.bank.bank_name != bank_name:
        print("Error: User does not belong to this bank.")
        return

    if operation == '1':  # Deposit Money
        amount = get_float_input("Enter the amount to deposit: ")
        user.deposit(amount)

    elif operation == '2':  # Withdraw Money
        password = getpass.getpass("Enter Password: ")
        if user.authenticate(password):
            amount = get_float_input("Enter the amount to withdraw: ")
            user.withdraw(amount)
        else:
            print("Incorrect password.")

    elif operation == '3':  # Transfer Money
        receiver_id = input("Enter the Receiver's User ID: ")
        receiver = users.get(receiver_id)
        if not receiver:
            print("Invalid receiver ID.")
            return
        if receiver.bank.bank_name != bank_name:
            print("Error: Receiver does not belong to this bank.")
            return
        password = getpass.getpass("Enter your Password: ")
        if user.authenticate(password):
            amount = get_float_input("Enter the amount to transfer: ")
            user.transfer(amount, receiver)
        else:
            print("Incorrect password.")

    elif operation == '4':  # Check Balance
        password = getpass.getpass("Enter Password: ")
        if user.authenticate(password):
            print(f"Current Balance: {user.balance}")
        else:
            print("Incorrect password.")

def main():
    users = {}

    while True:
        choice = input("Do you want to create a bank or a user? (bank/user/exit): ").strip().lower()
        if choice == 'bank':
            create_bank()
        elif choice == 'user':
            create_user(users)
        elif choice == 'exit':
            break
        else:
            print("Invalid choice. Please enter 'bank', 'user', or 'exit'.")

    while True:
        display_menu()
        choice = input("Enter Your Choice: ")

        if choice in ['1', '2', '3', '4']:  # Deposit, Withdraw, Transfer, Check Balance
            perform_operation(users, choice)

        elif choice == '5':  # Exit
            print("Thanks for using the banking system!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
