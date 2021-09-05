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

    def __init__(self, sender, smtp_server, password):

        self.sender = sender
        self.smtp_server = smtp_server
        self.password = password

        port = 465  # For SSL
        context = ssl.create_default_context()

        self.server =  smtplib.SMTP_SSL(smtp_server, port, context=context)

    def login(self):
        return self.server.login(self.sender, self.password)

    def quit(self):
        return self.server.quit()

    def send_mail(self, receiver, subject, txt, html):

        self.receiver = receiver
        self.subject = subject
        self.txt = txt
        self.html = html

        msg = self.build_message()

        err = self.server.sendmail(self.sender, self.receiver, msg)

    def build_message(self):

        message = MIMEMultipart("alternative")
        message["Subject"] = self.subject
        message["From"] = self.sender
        message["To"] = self.receiver

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(self.txt, "plain")
        part2 = MIMEText(self.html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)

        return str(message)
