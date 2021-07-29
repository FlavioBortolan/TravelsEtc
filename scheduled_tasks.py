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
# Import settings
django.setup()
User = get_user_model()

import random
from TravelsApp.models import Activity
from TravelsApp.models import Event
from TravelsApp.models import UserProfileInfo
from django.db.models import F


#Scan all events to find if some event has queued people but has less partecipants than its Maximum
def check_free_events():

    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "roberto.ferro1996@gmail.com"  # Enter your address
    password = 'margherita1'
    context = ssl.create_default_context()

    print('Advising queued people that there are free tickets.....')
    server =  smtplib.SMTP_SSL(smtp_server, port, context=context)
    server.login(sender_email, password)

    for e in Event.objects.filter(date__gte = datetime.now()) :
        if e.partecipants.count() < e.activity.maxNumPartecipants:
            #print('Event ' + e.activity.name + ' has free tickets!.')
            #print('Event ' + e.activity.name + ' has ' + str(e.queued_partecipants.count()) + ' queued partecipants')
            for p in e.queued_partecipants.all():
                if hasattr(p, 'userprofileinfo'):
                    #msg = ' A ticket has become available for event  ' + e.activity.name + ' on date ' + str(e.date)
                    msg = build_ticket_available_msg(sender_email, p.email, p.first_name, e.activity.name, str(e.date) )
                    print('Sending a mail to ' + p.email + msg.as_string())

                    err = server.sendmail(sender_email, p.email, msg.as_string())
                    #print (list(err))
    server.quit()


def build_ticket_available_msg( sender, receiver, name, activity, date ):

    message = MIMEMultipart("alternative")
    message["Subject"] = 'Ticket available for event ' + activity + ' on ' + date
    message["From"] = sender
    message["To"] = receiver

    # Create the plain-text and HTML version of your message
    text = """\
    Hi,
    How are you?
    Real Python has many great tutorials:
    www.realpython.com"""

    #html = html.format(activity, date)
    response = render(None, 'TravelsApp/free_ticket_message.html', {'name': name, 'event': activity, 'date': date})
    html=str(response.content.decode('UTF-8'))

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    return message

if __name__=="__main__" :
    check_free_events()
