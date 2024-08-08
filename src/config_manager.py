import json
import os
from cryptography.fernet import Fernet

class ConfigManager:
    def __init__(self, config_path):
        self.config_path = config_path
        self.config = self.load_config()
        self.key = self.load_or_create_key()
        self.fernet = Fernet(self.key)

    def load_config(self):
        with open(self.config_path, 'r') as file:
            return json.load(file)

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        self.save_config()

    def save_config(self):
        with open(self.config_path, 'w') as file:
            json.dump(self.config, file, indent=4)

    def load_or_create_key(self):
        key_path = os.path.join(os.path.dirname(self.config_path), 'secret.key')
        if os.path.exists(key_path):
            with open(key_path, 'rb') as key_file:
                return key_file.read()
        else:
            key = Fernet.generate_key()
            with open(key_path, 'wb') as key_file:
                key_file.write(key)
            return key

    def encrypt(self, data):
        return self.fernet.encrypt(data.encode()).decode()

    def decrypt(self, data):
        return self.fernet.decrypt(data.encode()).decode()

config_manager = ConfigManager('config/config.json')