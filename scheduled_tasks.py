import os
from datetime import *
import time
from dateutil.relativedelta import *
from dateutil.rrule import *
from datetime import datetime

from random import seed
from random import randint
import sys
import smtplib, ssl


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
            print('Event ' + e.activity.name + ' has free tickets!.')
            print('Event ' + e.activity.name + ' has ' + str(e.queued_partecipants.count()) + ' queued partecipants')
            for p in e.queued_partecipants.all():
                if hasattr(p, 'userprofileinfo'):
                    msg = ' A ticket has become available for event  ' + e.activity.name + ' on date ' + str(e.date)
                    print('Sending a mail to ' + p.email + msg)
                    msg=message = """\
                    Subject: Hi there

                    This message is sent from Python."""
                    err = server.sendmail(sender_email, p.email, msg)
                    print (list(err))
    server.quit()

if __name__=="__main__" :
    check_free_events()
