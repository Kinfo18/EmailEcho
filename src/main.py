from src.config_manager import setup_config, ConfigManager
from src.email_checker import EmailChecker
from src.telegram_bot import TelegramBot
from src.resource_monitor import ResourceMonitor
from src.logger import setup_logger
from src.error_handler import error_handler
from src.updater import Updater
from src.metrics_collector import MetricsCollector
import schedule
import time

def main():
    setup_config()
    config_manager = ConfigManager('config/config.json')
    logger = setup_logger(config_manager)
    
    email_checker = EmailChecker(config_manager)
    telegram_bot = TelegramBot(config_manager)
    resource_monitor = ResourceMonitor(config_manager)
    updater = Updater(config_manager)
    metrics_collector = MetricsCollector()

    @error_handler.handle
    def check_and_notify():
        new_emails = email_checker.check_emails()
        if new_emails:
            for email in new_emails:
                message = f"New email from: {email['sender']}\nSubject: {email['subject']}"
                telegram_bot.send_message(message)
                metrics_collector.increment_email_count()
        else:
            resources = resource_monitor.check_resources()
            message = "No new emails.\nSystem status:\n"
            message += f"CPU: {resources['cpu']}%\n"
            message += f"Memory: {resources['memory']}%\n"
            message += f"Disk: {resources['disk']}%"
            telegram_bot.send_message(message)

        metrics_collector.log_metrics()

    logger.info("Starting EmailEcho")
    
    # Initial check
    check_and_notify()
    
    # Schedule regular checks
    schedule.every(config_manager.get('check_interval')).seconds.do(check_and_notify)
    
    # Schedule update checks
    schedule.every(config_manager.get('update_check_interval')).seconds.do(updater.check_for_updates)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()