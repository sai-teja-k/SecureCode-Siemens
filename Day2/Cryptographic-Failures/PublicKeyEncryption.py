import bcrypt
import json
import os
import rsa

ADMIN_CREDENTIALS_FILE = "admin_credentials.json"
PATIENT_DATA_FILE = "encrypted_patient_data.json"
#PATIENT_DATA_FILE = "patients.json"
PUBLIC_KEY_FILE = "doctor_public.pem"
PRIVATE_KEY_FILE = "doctor_private.pem"
MAX_LOGIN_ATTEMPTS = 3

# RSA Key Generation (Run once to create keys)
if not os.path.exists(PUBLIC_KEY_FILE) or not os.path.exists(PRIVATE_KEY_FILE):
    public_key, private_key = rsa.newkeys(2048)
    with open(PUBLIC_KEY_FILE, "wb") as pub_file:
        pub_file.write(public_key.save_pkcs1("PEM"))
    with open(PRIVATE_KEY_FILE, "wb") as priv_file:
        priv_file.write(private_key.save_pkcs1("PEM"))

def load_public_key():
    with open(PUBLIC_KEY_FILE, "rb") as pub_file:
        return rsa.PublicKey.load_pkcs1(pub_file.read())

def load_private_key():
    with open(PRIVATE_KEY_FILE, "rb") as priv_file:
        return rsa.PrivateKey.load_pkcs1(priv_file.read())

def encrypt_rsa(data, public_key):
    return rsa.encrypt(data.encode(), public_key)

def decrypt_rsa(encrypted_data, private_key):
    return rsa.decrypt(encrypted_data, private_key).decode()

def save_encrypted_data(encrypted_data):
    with open(PATIENT_DATA_FILE, "wb") as file:
        file.write(encrypted_data)

def load_encrypted_data():
    if os.path.exists(PATIENT_DATA_FILE):
        with open(PATIENT_DATA_FILE, "rb") as file:
            return file.read()
    else:
        print("No patient records found.")
        return None

def register_admin():
    """Allows a new admin to register securely."""
    username = input("Enter new admin username: ")
    password = input("Enter new admin password: ")
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    # Store credentials securely
    credentials = {}
    if os.path.exists(ADMIN_CREDENTIALS_FILE):
        with open(ADMIN_CREDENTIALS_FILE, "r") as file:
            credentials = json.load(file)
    
    if username in credentials:
        print("Username already exists. Choose a different one.")
        return
    
    credentials[username] = hashed_password.decode()
    
    with open(ADMIN_CREDENTIALS_FILE, "w") as file:
        json.dump(credentials, file)
    
    print("Admin registered successfully!")

def login_admin():
    """Allows an admin to log in securely."""
    if not os.path.exists(ADMIN_CREDENTIALS_FILE):
        print("No registered admins found. Please register first.")
        return False

    with open(ADMIN_CREDENTIALS_FILE, "r") as file:
        credentials = json.load(file)

    attempts = 0
    while attempts < MAX_LOGIN_ATTEMPTS:
        username = input("Enter admin username: ")
        password = input("Enter admin password: ")

        if username in credentials and bcrypt.checkpw(password.encode(), credentials[username].encode()):
            print("Login successful!")
            return True
        else:
            print("Invalid credentials. Try again.")
            attempts += 1
    
    print("Too many failed login attempts. Access denied.")
    return False

def add_patient():
    """Encrypt and store patient data securely."""
    public_key = load_public_key()
    name = input("Enter patient name: ")
    age = input("Enter patient age: ")
    email = input("Enter patient email: ")
    ssn = input("Enter patient SSN: ")
    history = input("Enter history of illness: ")
    
    patient_data = json.dumps({
        "name": name, "age": age, "email": email, "ssn": ssn, "history": history
    })
    
    encrypted_data = encrypt_rsa(patient_data, public_key)
    save_encrypted_data(encrypted_data)

    print("Patient data encrypted and stored securely!")

def view_patient():
    """Decrypt and display patient data securely."""
    private_key = load_private_key()
    encrypted_data = load_encrypted_data()
    
    if encrypted_data:
        try:
            decrypted_data = decrypt_rsa(encrypted_data, private_key)
            patient_info = json.loads(decrypted_data)

            print("\n🔹 Decrypted Patient Data:")
            for key, value in patient_info.items():
                print(f"{key}: {value}")
        except Exception as e:
            print(f"Error decrypting data: {e}")

def main():
    while True:
        print("\n1. Register Admin")
        print("2. Login as Admin")
        print("3. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            register_admin()
        elif choice == "2":
            if login_admin():
                while True:
                    print("\n1. Add Patient Data")
                    print("2. View Patient Data")
                    print("3. Logout")
                    sub_choice = input("Choose an option: ")
                    if sub_choice == "1":
                        add_patient()
                    elif sub_choice == "2":
                        view_patient()
                    elif sub_choice == "3":
                        print("Logged out successfully.")
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
