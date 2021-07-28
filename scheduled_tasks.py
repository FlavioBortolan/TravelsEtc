import os
from datetime import *
import time
from dateutil.relativedelta import *
from dateutil.rrule import *
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

import random
from TravelsApp.models import Activity
from TravelsApp.models import Event
from TravelsApp.models import UserProfileInfo
