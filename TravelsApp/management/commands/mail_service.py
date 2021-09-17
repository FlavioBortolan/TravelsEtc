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
from TravelsApp.models import Setting
from TravelsApp.models import OutMail

from TravelsApp.mailer import Mailer


from TravelsApp.models import UserProfileInfo
from django.db.models import F



from django.core.management.base import BaseCommand, CommandError

# Import settings
django.setup()
User = get_user_model()

class Command(BaseCommand):

    help = 'Background mailer service. Sends all mails contained in OutMail object'

    def handle(self, *args, **options):

        company_mail = Setting.get_setting('company_email')
        smtp_server  = Setting.get_setting('company_email_smtp_server')
        company_pw   = Setting.get_setting('company_email_password')

        #setup mailer component
        m = Mailer(sender_email=company_mail, smtp_server = smtp_server, password = company_pw)
        m.login()

        #scan all elements in OutMail
        for om in OutMail.objects.filter(status = 'created'):

            self.stdout.write('sending mail to ' + om.recipient.email + ':' + om.subject)
            r = m.send_mail(om.recipient.email, om.subject, om.html, om.html)
            self.stdout.write(str(r))

            om.status = 'notified'
            om.save()

        m.quit()

        self.stdout.write(self.style.SUCCESS('Success!!'))
