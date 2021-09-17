import os
from datetime import *
import time
from dateutil.relativedelta import *
from dateutil.rrule import *
from datetime import datetime

import sys
import smtplib, ssl

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Mailer:

    def __init__(self, sender_email, smtp_server, password):

        self.sender_email = sender_email
        self.smtp_server = smtp_server
        self.password = password

        port = 465  # For SSL
        context = ssl.create_default_context()

        self.server =  smtplib.SMTP_SSL(smtp_server, port, context=context)

    def login(self):
        return self.server.login(self.sender_email, self.password)

    def quit(self):
        return self.server.quit()

    def send_mail(self, receiver_email, subject, txt, html):

        self.receiver_email = receiver_email
        self.subject = subject
        self.txt = txt
        self.html = html

        msg = self.build_message()

        return self.server.sendmail(self.sender_email, self.receiver_email, msg)

    def build_message(self):

        message = MIMEMultipart("alternative")
        message["Subject"] = self.subject
        message["From"] = self.sender_email
        message["To"] = self.receiver_email

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(self.txt, "plain")
        part2 = MIMEText(self.html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)

        return message.as_string()
