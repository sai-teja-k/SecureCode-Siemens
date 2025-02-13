import bcrypt
import json
import os

ADMIN_CREDENTIALS_FILE = "admin_credentials.json"
PATIENT_DATA_FILE = "patients_2.json"
MAX_LOGIN_ATTEMPTS = 3

def hash_passcode(passcode):
    return bcrypt.hashpw(passcode.encode(), bcrypt.gensalt()).decode()

def check_passcode(passcode, hashed_passcode):
    return bcrypt.checkpw(passcode.encode(), hashed_passcode.encode())

def load_credentials():
    if not os.path.exists(ADMIN_CREDENTIALS_FILE):
        return {}
    with open(ADMIN_CREDENTIALS_FILE, "r") as file:
        return json.load(file)

def save_credentials(credentials):
    with open(ADMIN_CREDENTIALS_FILE, "w") as file:
        json.dump(credentials, file)

def register_admin():
    username = input("Enter a username: ")
    credentials = load_credentials()
    if username in credentials:
        print("Username already exists. Try another one.")
        return
    passcode = input("Enter a passcode: ")
    credentials[username] = hash_passcode(passcode)
    save_credentials(credentials)
    print("Admin registered successfully!")

def login_admin():
    credentials = load_credentials()
    attempts = 0
    while attempts < MAX_LOGIN_ATTEMPTS:
        username = input("Enter username: ")
        passcode = input("Enter passcode: ")
        if username in credentials and check_passcode(passcode, credentials[username]):
            print("Login successful! Access granted.")
            return True
        else:
            print("Invalid username or passcode. Try again.")
            attempts += 1
    print("Too many failed attempts. Access locked.")
    return False

def load_patient_data():
    if not os.path.exists(PATIENT_DATA_FILE):
        return []
    with open(PATIENT_DATA_FILE, "r") as file:
        return json.load(file)

def save_patient_data(patients):
    with open(PATIENT_DATA_FILE, "w") as file:
        json.dump(patients, file)

def add_patient():
    patients = load_patient_data()
    name = input("Enter patient name: ")
    age = input("Enter patient age: ")
    condition = input("Enter medical condition: ")
    patients.append({"name": name, "age": age, "condition": condition})
    save_patient_data(patients)
    print("Patient added successfully!")

def view_patients():
    patients = load_patient_data()
    if not patients:
        print("No patient records found.")
    else:
        for i, patient in enumerate(patients, start=1):
            print(f"{i}. Name: {patient['name']}, Age: {patient['age']}, Condition: {patient['condition']}")

def main():
    while True:
        print("\n1. Register Admin")
        print("2. Login Admin")
        print("3. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            register_admin()
        elif choice == "2":
            if login_admin():
                while True:
                    print("\n1. Add Patient")
                    print("2. View Patients")
                    print("3. Logout")
                    sub_choice = input("Choose an option: ")
                    if sub_choice == "1":
                        add_patient()
                    elif sub_choice == "2":
                        view_patients()
                    elif sub_choice == "3":
                        break
                    else:
                        print("Invalid option. Try again.")
        elif choice == "3":
            print("Exiting application.")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
