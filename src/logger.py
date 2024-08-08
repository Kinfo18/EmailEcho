import logging
from logging.handlers import RotatingFileHandler
import os

class Logger:
    def __init__(self, log_file, max_size, backup_count, log_level):
        self.logger = logging.getLogger('EmailNotifier')
        self.logger.setLevel(log_level)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        file_handler = RotatingFileHandler(log_file, maxBytes=max_size, backupCount=backup_count)
        file_handler.setFormatter(formatter)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)

logger = Logger(
    'logs/email_notifier.log',
    config_manager.get('max_log_size'),
    config_manager.get('max_log_backups'),
    config_manager.get('log_level')
)