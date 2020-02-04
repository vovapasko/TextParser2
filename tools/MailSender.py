import logging
import smtplib
import traceback
from email.message import EmailMessage

from tools.tools import get_data_from_cred


class MailSender:
    def __init__(self):
        self.login = self.get_data_from_cred("login")
        self.password = self.get_data_from_cred("password")
        self.mail_to = self.get_data_from_cred("mailTo")
        self.port = 465
        self.message = EmailMessage()
        self.message['From'] = self.login

    def set_subject(self, subject):
        self.message['Subject'] = subject

    def set_content(self, content):
        self.message.set_content(content)

    def set_attachment(self, files):
        try:
            for file in files:
                with open(file, 'rb') as f:
                    file_data = f.read()
                    file_name = file.stem + file.suffix

                self.message.add_attachment(file_data, maintype='application', subtype='octet-stream',
                                            filename=file_name)
        except Exception:
            logging.error("Error happened while adding attachment to Email template")
            logging.error(traceback.format_exc())
            print(traceback.format_exc())

    def send_message(self):
        try:
            self.message['To'] = self.mail_to
            with smtplib.SMTP_SSL("smtp.gmail.com", self.port) as smtp:
                smtp.login(self.login, self.password)
                smtp.send_message(self.message)
        except Exception:
            logging.error("Error happened while sending Email")
            logging.error(traceback.format_exc())
            print(traceback.format_exc())

    def get_data_from_cred(self, key, subroot="MailData"):
        return get_data_from_cred(key, subroot)
