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

    s = Setting.objects.get_or_create( name="subscription_duration_months", value = '12', description='duration of a renewed subscription in months')[0]
    s.save()
