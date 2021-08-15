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
from TravelsApp.models import Ticket



if __name__ == '__main__':


    ts= Ticket.objects.all()
    if ts.count()>0:
        #t[0].user='flavio.bortolan@gmail.com'
        #t[0].save()
        print(str(t[0].user))
