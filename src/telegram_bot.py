import telebot
from error_handler import error_handler
from logger import get_logger

class TelegramBot:
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.logger = get_logger()
        self.bot_token = self.config_manager.get('telegram.bot_token')
        self.chat_id = self.config_manager.get('telegram.chat_id')
        self.bot = telebot.TeleBot(self.bot_token)

    @error_handler.handle
    def send_message(self, message):
        self.bot.send_message(self.chat_id, message)
        self.logger.info(f"Message sent to Telegram: {message}")

    def start_bot(self):
        @self.bot.message_handler(commands=['start', 'help'])
        def send_welcome(message):
            self.bot.reply_to(message, "Welcome to EmailEcho Bot!")

        @self.bot.message_handler(commands=['status'])
        def send_status(message):
            # Implement status check here
            self.bot.reply_to(message, "Status: Running")

        self.bot.polling(none_stop=True)