import os
import json
from cryptography.fernet import Fernet

class Encryptor:
    def __init__(self, key_store_path="config/encryption_keys.json"):
        self.key_store_path = key_store_path
        self.key_store = self.load_key_store()

    def load_key_store(self):
        if os.path.exists(self.key_store_path):
            with open(self.key_store_path, 'r') as f:
                return json.load(f)
        else:
            return {}

    def save_key_store(self):
        os.makedirs(os.path.dirname(self.key_store_path), exist_ok=True)
        with open(self.key_store_path, 'w') as f:
            json.dump(self.key_store, f)

    def generate_key(self):
        return Fernet.generate_key().decode()

    def encrypt(self, text, file_name):
        if file_name not in self.key_store:
            key = self.generate_key()
            self.key_store[file_name] = key
            self.save_key_store()
        else:
            key = self.key_store[file_name]

        fernet = Fernet(key.encode())
        encrypted = fernet.encrypt(text.encode())
        return encrypted.decode()

    def decrypt(self, text, file_name):
        if file_name not in self.key_store:
            raise ValueError(f"No key found for file: {file_name}")
        key = self.key_store[file_name]
        fernet = Fernet(key.encode())
        decrypted = fernet.decrypt(text.encode())
        return decrypted.decode()


# def main():
#     file_name = "customer_profiles.csv"
#     original_text = "Sensitive customer data like SSN or password"

#     encryptor = Encryptor()

#     print("Original text:", original_text)

#     encrypted_text = encryptor.encrypt(original_text, file_name)
#     print("Encrypted text:", encrypted_text)

#     decrypted_text = encryptor.decrypt(encrypted_text, file_name)
#     print("Decrypted text:", decrypted_text)

# if __name__ == "__main__":
#     main()
