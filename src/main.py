from decimal import Decimal
from uuid import UUID

from application.service import BankAccountApplication

def open_account(app):
    full_name = input("Enter full name: ")
    email = input("Enter email address: ")
    account_id = app.open_account(full_name, email)
    print(f"Account opened successfully. Account ID: {account_id}")

def withdraw_cash(app):
    account_id = input("Enter account ID: ")
    try:
        app.get_account(UUID(account_id))
        amount = Decimal(input("Enter amount to withdraw: "))
        app.withdraw_funds(UUID(account_id), amount)
        print("Withdrawal successful.")
    except Exception as e:
        print("Error:")
        print(e)

def credit_account(app):
    account_id = input("Enter account ID: ")
    amount = Decimal(input("Enter amount to credit: "))
    try:
        app.deposit_funds(UUID(account_id), amount)
        print("Account credited successfully.")
    except Exception as e:
        print(f"Error: {e}")

def close_account(app):
    account_id = input("Enter account ID: ")
    try:
        app.close_account(UUID(account_id))
        print("Account closed successfully.")
    except Exception as e:
        print(f"Error: {e}")
        
def check_balance(app):
    account_id = input("Enter account ID: ")
    try:
        balance =  app.get_balance(UUID(account_id))
        print(f"Account Blance is {balance}")
    except Exception as e:
        print(f"Error: {e}")

def main():
  
    app = BankAccountApplication()

    while True:
        print("\nChoose an option:")
        print("1. Open Account")
        print("2. Withdraw Cash")
        print("3. Credit Account")
        print("4. Check Balance")
        print("5. Close Account")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            open_account(app)
        elif choice == "2":
            withdraw_cash(app)
        elif choice == "3":
            credit_account(app)
        elif choice == "4":
            check_balance(app)
        elif choice == "5":
            close_account(app)
        elif choice == "6":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


main()