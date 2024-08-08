import time
import schedule
from src.email_checker import email_checker
from src.telegram_bot import telegram_bot
from src.resource_monitor import resource_monitor
from src.config_manager import config_manager
from src.logger import logger
from src.error_handler import error_handler
from src.updater import updater
from src.metrics_collector import metrics_collector

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

def main():
    logger.info("Starting Email Notifier")
    
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