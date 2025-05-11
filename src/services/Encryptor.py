class Encryptor:
    def __init__(self, key_store_path="config/encryption_keys.json"):
        self.key_store_path = key_store_path
        
    def load_key_store(self):
        pass

    def save_key_store(self):
        pass

    def generate_key(self):
        pass

    def encrypt(self, text, file_name):
        # encrypt text and store the key
        pass

    def decrypt(self, text, key):
        pass