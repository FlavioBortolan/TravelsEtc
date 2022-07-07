import os
from os.path import basename
from datetime import *
import time
from dateutil.relativedelta import *
from dateutil.rrule import *
from datetime import datetime

import sys
import smtplib, ssl

from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

class Mailer:

    def __init__(self, sender_email, smtp_server, password):

        self.sender_email = sender_email
        self.smtp_server = smtp_server
        self.password = password
        self.logged_in = False

        port = 465  # For SSL
        context = ssl.create_default_context()

        self.server =  smtplib.SMTP_SSL(smtp_server, port, context=context)

    def login(self):

        self.logged_in=True
        r = self.server.login(self.sender_email, self.password)
        print('login:' + str(r))
        return r

    def quit(self):

        self.logged_in=False
        return self.server.quit()

    def send_mail(self, receiver_email, subject, txt, html, attachements=[]):

        self.receiver_email = receiver_email
        self.subject = subject
        self.txt = txt
        self.html = html
        self.attachements = attachements

        msg = self.build_message()

        r = self.server.sendmail(self.sender_email, self.receiver_email, msg)
        print('mail send:' + str(r))
        return r

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

        #add the attachements
        for f in self.attachements or []:
            with open(f, "rb") as fil:
                attachment_part = MIMEApplication(fil.read(), Name=basename(f))

            # After the file is closed
            attachment_part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
            message.attach(attachment_part)

        return message.as_string()

    def flush_outmail(self, om, attachements=[]):

        print('Mailer: flush_outmail: ' + om.recipient.email + ', ' + om.subject)

        self.login()

        print('sending mail to ' + om.recipient.email + ':' + om.subject)
        r = self.send_mail(om.recipient.email, om.subject, om.html, om.html, attachements)


        om.status = 'notified'
        om.save()

        self.quit()

        if r == True:
            print('Success!!')

        return r
