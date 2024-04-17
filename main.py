
import mysql.connector

# Connect to MySQL database
try:
    connection = mysql.connector.connect(user="root", database="bank", password="M1ssionTX@123")
    cursor = connection.cursor()

except mysql.connector.Error as error:
    print("Error while connecting to MySQL:", error)

# SQL command to create the 'accounts' table
create_table_query = """
CREATE TABLE IF NOT EXISTS accounts (
    account_number INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    pin VARCHAR(4) NOT NULL,
    balance DECIMAL(10, 2) NOT NULL DEFAULT 0.0
)
"""

# Execute the SQL command to create the table
try:
    cursor.execute(create_table_query)
    connection.commit()
    print("Table 'accounts' created successfully.")
except mysql.connector.Error as error:
    print("Error creating 'accounts' table:", error)

# Function to create a new account
def create_account():
    print("\nWelcome to the Online Banking System - Account Creation")
    name = input("Enter your full name: ")
    pin = input("Choose a 4-digit PIN for your account: ")

    try:
        cursor.execute("INSERT INTO accounts (name, pin) VALUES (%s, %s)", (name, pin))
        connection.commit()
        new_account_number = cursor.lastrowid
        print("Account created successfully! Your account number is:", new_account_number)
    except mysql.connector.Error as error:
        print("Error creating account:", error)

# Function to log in
def log_in():
    print("\nWelcome to the Online Banking System - Log In")
    account_number = input("Enter your account number: ")
    pin = input("Enter your PIN: ")

    cursor.execute("SELECT * FROM accounts WHERE account_number=%s AND pin=%s", (account_number, pin))
    account = cursor.fetchone()

    if account:
        print("Welcome back, {}!".format(account[1]))
        return account
    else:
        print("Invalid account number or PIN.")
        return None

# Function to check balance
def check_balance(account):
    cursor.execute("SELECT balance FROM accounts WHERE account_number=%s", (account[0],))
    balance = cursor.fetchone()[0]
    updated_account = (account[0], account[1], account[2], balance)
    print("\nAccount Balance:")
    print("Name:", updated_account[1])
    print("Account Number:", updated_account[0])
    print("Balance:", updated_account[3])
# Function to deposit
from decimal import Decimal

# Function to deposit
def deposit(account):
    print("\nDeposit Funds")
    amount = Decimal(input("Enter deposit amount: "))
    new_balance = account[3] + amount
    try:
        cursor.execute("UPDATE accounts SET balance=%s WHERE account_number=%s", (new_balance, account[0]))
        connection.commit()
        print("Deposit successful. New balance is:", new_balance)
        # Update the account variable with the new balance
        account = (account[0], account[1], account[2], new_balance)
    except mysql.connector.Error as error:
        print("Error depositing funds:", error)
# Function to withdraw
def withdraw(account):
    print("\nWithdraw Funds")
    amount = float(input("Enter withdrawal amount: "))
    if account[3] >= amount:
        new_balance = account[3] - amount
        try:
            cursor.execute("UPDATE accounts SET balance=%s WHERE account_number=%s", (new_balance, account[0]))
            connection.commit()
            print("Withdrawal successful. New balance is:", new_balance)
        except mysql.connector.Error as error:
            print("Error withdrawing funds:", error)
    else:
        print("Insufficient funds.")

# Function to close account
def close_account(account):
    print("\nClose Account")
    confirm = input("Are you sure you want to close your account? (yes/no): ")
    if confirm.lower() == 'yes':
        try:
            cursor.execute("DELETE FROM accounts WHERE account_number=%s", (account[0],))
            connection.commit()
            print("Account closed successfully.")
        except mysql.connector.Error as error:
            print("Error closing account:", error)
    else:
        print("Account closure canceled.")

# Function to modify account details
def modify_account(account):
    print("\nModify Account Details")
    print("1. Modify Name")
    print("2. Modify PIN")
    choice = input("Enter your choice: ")

    if choice == '1':
        new_name = input("Enter new name: ")
        try:
            cursor.execute("UPDATE accounts SET name=%s WHERE account_number=%s", (new_name, account[0]))
            connection.commit()
            print("Name updated successfully.")
        except mysql.connector.Error as error:
            print("Error updating name:", error)
    elif choice == '2':
        new_pin = input("Enter new 4-digit PIN: ")
        try:
            cursor.execute("UPDATE accounts SET pin=%s WHERE account_number=%s", (new_pin, account[0]))
            connection.commit()
            print("PIN updated successfully.")
        except mysql.connector.Error as error:
            print("Error updating PIN:", error)
    else:
        print("Invalid choice.")

# Main menu
while True:
    print("\nWelcome to the Online Banking System")
    print("1. Log In")
    print("2. Create Account")
    print("3. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        account = log_in()
        if account:
            while True:
                print("\nWhat would you like to do?")
                print("1. Check Balance")
                print("2. Deposit")
                print("3. Withdraw")
                print("4. Close Account")
                print("5. Modify Account Details")
                print("6. Log Out")

                option = input("Enter your option: ")

                if option == '1':
                    # Re-fetch the account data to ensure we have the latest balance
                    cursor.execute("SELECT * FROM accounts WHERE account_number=%s", (account[0],))
                    updated_account = cursor.fetchone()
                    check_balance(updated_account)
                elif option == '2':
                    deposit(account)
                elif option == '3':
                    withdraw(account)
                elif option == '4':
                    close_account(account)
                    break
                elif option == '5':
                    modify_account(account)
                elif option == '6':
                    print("Logged out.")
                    break
                else:
                    print("Invalid option.")
    elif choice == '2':
        create_account()
    elif choice == '3':
        print("Thank you for using our Online Banking System.")
        break
    else:
        print("Invalid choice. Please try again.")

# Close MySQL connection
if 'connection' in locals():
    if cursor:
        cursor.close()
    connection.close()
    print("MySQL connection closed.")
