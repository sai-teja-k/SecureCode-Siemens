import rsa
import json
import os

PRIVATE_KEY_FILE = "doctor_private.pem"
PATIENT_DATA_FILE = "encrypted_patient_data.json"

def load_private_key():
    with open(PRIVATE_KEY_FILE, "rb") as priv_file:
        private_key = rsa.PrivateKey.load_pkcs1(priv_file.read())
    return private_key

def load_encrypted_data():
    if os.path.exists(PATIENT_DATA_FILE):
        with open(PATIENT_DATA_FILE, "rb") as file:
            return file.read()
    else:
        print("No patient data found.")
        return None

def decrypt_patient_data(encrypted_data, private_key):
    try:
        decrypted_data = rsa.decrypt(encrypted_data, private_key).decode()
        return json.loads(decrypted_data)
    except Exception as e:
        print(f"Decryption failed: {e}")
        return None

def view_patient_data():
    private_key = load_private_key()
    encrypted_data = load_encrypted_data()
    if encrypted_data:
        patient_data = decrypt_patient_data(encrypted_data, private_key)
        if patient_data:
            print("\nDecrypted Patient Data:")
            for key, value in patient_data.items():
                print(f"{key}: {value}")

def main():
    print("Doctor's Patient Data Viewer")
    view_patient_data()

if __name__ == "__main__":
    main()
