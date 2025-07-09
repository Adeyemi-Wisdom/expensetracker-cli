import os
import json
DATA_FILE = "File.txt"
numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

def operation_logic(user_data):
    print(f'You are welcome back {user_data["name"]}')
    if not user_data.get("user_expenses"):
        print("You have no expenses recorded yet.")
    else:
        print("Here are your current expenses:")
        for i, expense in enumerate(user_data["user_expenses"], 1):
            print(f"{i}. {expense['goods']} - ${expense['price']}")
    while True:
        opt = input("New Expenses? (Yes/No): ").lower()
        if opt == "yes":
            goods = input("Product bought / What money is spent on: ")
            price = int(input("How much is it: $"))
            expense_record = {
                "goods": goods,
                "price": price
            }
            if "user_expenses" not in user_data or not isinstance(user_data["user_expenses"], list):
                user_data["user_expenses"] = []
            user_data["user_expenses"].append(expense_record)
            print("Expense recorded successfully!")
            update_user_data(user_data)
        else:
            print(f"Goodbye {user_data['name']}")
            break
def update_user_data(user_data):
    if not os.path.exists(DATA_FILE):
        print("Data file does not exist.")
        return
    updated_lines = []
    user_updated = False
    with open(DATA_FILE, 'r') as file:
        for line in file:
            try:
                data = json.loads(line.strip())
                if data.get("name") == user_data["name"] and data.get("password") == user_data["password"]:
                    updated_lines.append(json.dumps(user_data) + "\n")
                    user_updated = True
                else:
                    updated_lines.append(line)
            except json.JSONDecodeError:
                updated_lines.append(line)
    with open(DATA_FILE, 'w') as file:
        file.writelines(updated_lines)

    if user_updated:
        print(f"Data for {user_data['name']} updated successfully!")
    else:
        print("User data not found. No updates made.")

def save_user_data(user_data):
    if not isinstance(user_data, dict):
        raise ValueError("user_data must be a dictionary.")
    with open(DATA_FILE, "a") as file:
        file.write(json.dumps(user_data) + "\n")

def login_check(password, username):
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            for line in file:
                try:
                    data = json.loads(line.strip())
                    if data.get('password') == password and data.get('name') == username:
                        return data
                except json.JSONDecodeError:
                    print("Error decoding data file.")
    return None

def Create_account():
    print("You Are Welcome To Wisdom's Expense Tracking System")
    print('Kindly fill in your details')
    while True:
        person_name = input('Your name in full: ')
        if any(i in numbers for i in person_name):
            print("Kindly input the correct name!")
        else:
            break
    while True:
        try:
            person_password = input('Input a four-digit number to be saved as your password: ')
            if len(person_password) == 4 and person_password.isdigit():
                break
            else:
                print("Password must be a four-digit number.")
        except ValueError:
            continue
    person_email = input('Please enter your email address: ')
    person_1 = {
        "name": person_name,
        "password": person_password,
        "email": person_email,
    }
    save_user_data(person_1)
    print("Account created successfully!")

def verification():
    total_wrong = 0
    while total_wrong < 3:
        user_name = input("Enter your username: ")
        user_password = input("Enter your password: ")
        user_data = login_check(user_password, user_name)
        if user_data:
            return user_data
        else:
            total_wrong += 1
            print("Wrong password or username.")
    print("Too many failed attempts. Access denied.")
    return None

def Login():
    print("You are welcome")
    while True:
        login_choice = input("If you already have an account, enter 1 to login\n"
                             "If no account yet, enter 2 to create an account: ")
        if login_choice == "1":
            user_data = verification()
            if user_data:
                operation_logic(user_data)
            break
        elif login_choice == "2":
            Create_account()
            break
        else:
            print("Wrong input.")

# Main program
operation = input("Enter 1 to Create an account\n"
                  "Enter 2 to Login to your account\n")
if operation == "1":
    Create_account()
    while True:
        account_choice = input("Enter 'again' to create another account\n"
                               "'off' to shutdown\n"
                               "'login' to login into your account: ").lower()
        if account_choice == 'again':
            Create_account()
        elif account_choice == 'off':
            print("Goodbye!")
            break
        elif account_choice == 'login':
            Login()
            break
        else:
            print("Wrong input.")
elif operation == "2":
    Login()