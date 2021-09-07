import os
from datetime import *
import time
from dateutil.relativedelta import *
from dateutil.rrule import *
from datetime import datetime
from django.shortcuts import render

from random import seed
from random import randint
import sys
import smtplib, ssl

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Configure settings for project
# Need to run this before calling models from application!
os.environ.setdefault('DJANGO_SETTINGS_MODULE','TravelsEtc.settings')

import django
from django.contrib.auth import get_user_model

import random
from TravelsApp.models import Activity
from TravelsApp.models import Event
from TravelsApp.models import UserProfileInfo
from django.db.models import F

from django.core.management.base import BaseCommand, CommandError

# Import settings
django.setup()
User = get_user_model()

class Command(BaseCommand):

    help = 'Sends a mail to peple queued to an event where a ticket has become free'

    def build_ticket_available_msg( self, sender, user, event ):

        message = MIMEMultipart("alternative")
        message["Subject"] = 'Ticket available for event ' + event.activity.name + ' on ' + str(event.date)
        message["From"] = sender
        message["To"] = user.email

        response = render(None, 'TravelsApp/free_ticket_message.html', {'event':event, 'user': user})
        html=str(response.content.decode('UTF-8'))

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(html, "plain")
        part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)

        return message

    def handle(self, *args, **options):
        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        sender_email = "roberto.ferro1996@gmail.com"  # Enter your address
        password = 'margherita1'
        context = ssl.create_default_context()

        print('Advising queued people that there are free tickets.....')
        server =  smtplib.SMTP_SSL(smtp_server, port, context=context)
        server.login(sender_email, password)

        for e in Event.objects.filter(date__gte = datetime.now()) :
            if e.partecipants.count() < e.activity.maxNumPartecipants and e.queued_partecipants.count()>0:
                self.stdout.write('Event ' + e.activity.name + ' has free tickets!.')

                for p in e.queued_partecipants.all():
                    if hasattr(p, 'userprofileinfo'):
                        #msg = ' A ticket has become available for event  ' + e.activity.name + ' on date ' + str(e.date)
                        msg = self.build_ticket_available_msg(sender_email, p, e )
                        self.stdout.write('Sending a mail to: ' + p.email)

                        err = server.sendmail(sender_email, p.email, msg.as_string())
                        self.stdout.write('Message sent to: ' + p.email)

        server.quit()

        self.stdout.write(self.style.SUCCESS('Success!!'))
