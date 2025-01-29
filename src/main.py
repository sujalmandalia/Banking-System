import os
from decimal import Decimal
from uuid import UUID
from application.service import BankAccountApplication
from dotenv import load_dotenv  # type: ignore

load_dotenv()

os.environ["PERSISTENCE_MODULE"] = os.getenv("PERSISTENCE_MODULE")
os.environ["POSTGRES_DBNAME"] = os.getenv("POSTGRES_DBNAME")
os.environ["POSTGRES_HOST"] = os.getenv("POSTGRES_HOST")
os.environ["POSTGRES_PORT"] = os.getenv("POSTGRES_PORT")
os.environ["POSTGRES_USER"] = os.getenv("POSTGRES_USER")
os.environ["POSTGRES_PASSWORD"] = os.getenv("POSTGRES_PASSWORD")


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
        print(f"Error: {e}")


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
        balance = app.get_balance(UUID(account_id))
        print(f"Account Balance is {balance}")
    except Exception as e:
        print(f"Error: {e}")


def get_all_accounts(app):
    app.get_all_accounts()


def main():

    app = BankAccountApplication()

    while True:
        print("\nChoose an option:")
        print("1. Open Account")
        print("2. Withdraw Cash")
        print("3. Credit Account")
        print("4. Check Balance")
        print("5. Get All Accounts")
        print("6. Close Account")
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
            get_all_accounts(app)
        elif choice == "6":
            close_account(app)
        elif choice == "6":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


main()
