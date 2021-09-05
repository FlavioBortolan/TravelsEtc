import os
from datetime import datetime
from random import seed
from random import randint
import sys


# Configure settings for project
# Need to run this before calling models from application!
os.environ.setdefault('DJANGO_SETTINGS_MODULE','TravelsEtc.settings')

import django
from django.contrib.auth import get_user_model
# Import settings
django.setup()
User = get_user_model()


from TravelsApp.models import Setting


if __name__=="__main__" :

    print("Genrating settings table: ")

    s = Setting.objects.get_or_create( name="subscription_duration_months", value = '12', description='Duration of a renewed subscription in months.')[0]
    s.save()

    s = Setting.objects.get_or_create( name="year_subscription_price", value = '20', description='Price for the yearly subscription.')[0]
    s.save()

    s = Setting.objects.get_or_create( name="card_refund_cost", value = '1', description='Cost of the refund by card')[0]
    s.save()

    s = Setting.objects.get_or_create( name="smallest_currency_ratio", value = '100', description='Ratio between one currency unit and its smallest value. Exp 1 euro = 100 euro cents.')[0]
    s.save()

    #company email
    s = Setting.objects.get_or_create( name="company_email", value = 'roberto.ferro1996@gmail.com', description='Company email. Used to send official communication to users')[0]
    s.save()

    s = Setting.objects.get_or_create( name="company_email_smtp_server", value = 'smtp.gmail.com', description='Company email. smtp server address')[0]
    s.save()

    s = Setting.objects.get_or_create( name="company_email_password", value = 'margherita1', description='Company email. password')[0]
    s.save()
