import imaplib
import email
from email.header import decode_header
from src.config_manager import config_manager
from src.error_handler import error_handler
from src.logger import logger

class EmailChecker:
    def __init__(self):
        self.imap_server = config_manager.get('email')['imap_server']
        self.imap_port = config_manager.get('email')['imap_port']
        self.username = config_manager.get('email')['username']
        self.password = config_manager.decrypt(config_manager.get('email')['password'])
        self.last_checked_ids = set()

    @error_handler.handle
    def check_emails(self):
        mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
        mail.login(self.username, self.password)
        mail.select('inbox')

        _, search_data = mail.search(None, 'UNSEEN')
        new_emails = []

        for num in search_data[0].split():
            _, data = mail.fetch(num, '(RFC822)')
            _, bytes_data = data[0]

            email_message = email.message_from_bytes(bytes_data)
            subject, encoding = decode_header(email_message["subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8")
            sender = email_message["from"]

            if num.decode() not in self.last_checked_ids:
                new_emails.append({
                    'subject': subject,
                    'sender': sender,
                    'id': num.decode()
                })
                self.last_checked_ids.add(num.decode())

        mail.close()
        mail.logout()

        return new_emails

email_checker = EmailChecker()