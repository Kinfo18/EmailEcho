import imaplib
import email
from email.header import decode_header
from error_handler import error_handler
from logger import get_logger

class EmailChecker:
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.logger = get_logger()
        self.last_checked_ids = set()

    @error_handler.handle
    def check_emails(self):
        imap_server = self.config_manager.get('email.imap_server')
        imap_port = self.config_manager.get('email.imap_port')
        username = self.config_manager.get('email.username')
        password = self.config_manager.get_password()

        mail = imaplib.IMAP4_SSL(imap_server, imap_port)
        mail.login(username, password)
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