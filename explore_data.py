import os
import datetime
from random import seed
from random import randint

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

if __name__ == '__main__':


    print("Activities:")
    #print(Activity.objects.filter(place='Vicenza', leader="Priscilla Alboni"))
    print(Activity.objects.all())

    print("")

    print("Users:")
    print(User.objects.all())

    print("")
    print("First element in the list is:")
    print(Activity.objects.get(id=174))

    Gino = User.objects.get(username ="Gino")
    flavio = User.objects.get(username ="flavio")
    rita = User.objects.get(username ="rita")


    print("")
    print("Adding Gino e flavio to the trip:")
    a = Activity.objects.get(id=174)
    a.partecipants.add(Gino)
    a.partecipants.add(flavio)
    a.partecipants.add(rita)

    print("")
    print("The partecipants to the trip are:")
    print(a.partecipants.all())

    print("")
    print("The partecipants to the trip are:")
    print(a.partecipants.all())

    print("")
    print("The activities of flavio are:")

    print(flavio.activity_set.all())
