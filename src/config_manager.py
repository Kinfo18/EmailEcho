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
        if not os.path.exists(self.config_path):
            return self.create_default_config()
        with open(self.config_path, 'r') as file:
            return json.load(file)

    def create_default_config(self):
        default_config = {
            "email": {
                "imap_server": "",
                "imap_port": 993,
                "smtp_server": "",
                "smtp_port": 587,
                "username": "",
                "password": ""
            },
            "telegram": {
                "bot_token": "",
                "chat_id": ""
            },
            "check_interval": 3600,
            "log_level": "INFO",
            "max_log_size": 10485760,
            "max_log_backups": 5,
            "resource_threshold": {
                "cpu": 80,
                "memory": 80
            },
            "update_check_interval": 86400
        }
        with open(self.config_path, 'w') as file:
            json.dump(default_config, file, indent=4)
        return default_config

    def get(self, key, default=None):
        keys = key.split('.')
        value = self.config
        for k in keys:
            if k not in value:
                return default
            value = value[k]
        return value

    def set(self, key, value):
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
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

    def set_password(self, password):
        encrypted_password = self.encrypt(password)
        self.set('email.password', encrypted_password)

    def get_password(self):
        encrypted_password = self.get('email.password')
        if encrypted_password:
            return self.decrypt(encrypted_password)
        return None

def setup_config():
    config_manager = ConfigManager('config/config.json')
    
    # Configuración de correo electrónico
    if not config_manager.get('email.username'):
        username = input("Por favor, ingrese su dirección de correo electrónico: ")
        config_manager.set('email.username', username)
    
    if not config_manager.get('email.password'):
        password = input("Por favor, ingrese su contraseña de correo electrónico: ")
        config_manager.set_password(password)
    
    if not config_manager.get('email.imap_server'):
        imap_server = input("Por favor, ingrese el servidor IMAP (ej. imap.gmail.com): ")
        config_manager.set('email.imap_server', imap_server)
    
    if not config_manager.get('email.smtp_server'):
        smtp_server = input("Por favor, ingrese el servidor SMTP (ej. smtp.gmail.com): ")
        config_manager.set('email.smtp_server', smtp_server)
    
    # Configuración de Telegram
    if not config_manager.get('telegram.bot_token'):
        bot_token = input("Por favor, ingrese el token de su bot de Telegram: ")
        config_manager.set('telegram.bot_token', bot_token)
    
    if not config_manager.get('telegram.chat_id'):
        chat_id = input("Por favor, ingrese su chat_id de Telegram: ")
        config_manager.set('telegram.chat_id', chat_id)
    
    print("Configuración completa.")

if __name__ == "__main__":
    setup_config()