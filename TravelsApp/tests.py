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
from models import Activity
from models import Event
from models import UserProfileInfo
from django.db.models import F

from django.core.management.base import BaseCommand, CommandError

# Import settings
django.setup()
User = get_user_model()


# Create your tests here.
if __name__ == '__main__':

    e=Event.objects[0]
    user = User.objects.filter(email='flavio.bortolan@gmail.com')

    m = Mailer(sender='roberto.ferro1996@gmail.com', smtp_server = "smtp.gmail.com", password = 'margherita1')
    m.login()

    response = render(None, 'TravelsApp/free_ticket_message.html', {'event':e, 'user': user})
    html=str(response.content.decode('UTF-8'))

    m.send_mail(user.email, "buongiorno da mailer", html, html)
    m.quit()
