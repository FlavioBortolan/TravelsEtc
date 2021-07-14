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

import random
from TravelsApp.models import Activity
from TravelsApp.models import Event
from TravelsApp.models import UserProfileInfo
from faker import Faker

fakegen = Faker('it_IT')

def populate_users(users_count = 5):

    for entry in range(users_count):
        fake_name= fakegen.name().split()
        fake_first_name = fake_name[0]
        fake_last_name = fake_name[1]
        fake_email= fakegen.email()
        fake_number = fakegen.phone_number()

        #new entry
        u    = User           .objects.get_or_create(username = fake_email, first_name = fake_last_name,last_name= fake_last_name,email = fake_email)[0]
        print('Created User:' + str(u) )

        pi   = UserProfileInfo.objects.get_or_create(user=u, phone_number = fake_number, credits = randint(15, 40))[0]
        print('Created UserProfileInfo:' + str(pi) )

        u.save()
        print('user saved')

        pi.user = u
        print('UserProfileInfo assigned to user')

        pi.save()
        print('UserProfileInfo saved')


def populate_activities(activities_count = 5):

    for entry in range(activities_count):

        t = Activity.objects.get_or_create(
            type = random.choice(['Aperitivo', 'Trekking', 'Bicicletta']),
            place = random.choice(['Vicenza','Verona','Padova','Venezia','Brescia', 'Milano']),
            name = random.choice(['Monte gioia', 'Valle serena','gita al mare', 'Arte in città']),
            description = fakegen.text(max_nb_chars=300),
            leader = fakegen.name(),
            price = randint(15, 40),
            duration = randint(2, 5),
            meetPlaceLink = fakegen.uri(),
            meetPlaceDirections = fakegen.text(),
            activityDetail = fakegen.text(max_nb_chars=900),
            difficultyLevel = random.choice(['E','EE', 'ES']),
            length = randint(15, 40),
            gradient = randint(10, 90)*10,
            streetType = random.choice(['Sterrato','Asfalto', 'Ghiaino']),
            whatToBring = "Scarpe da trekking, cappello, crema solare, pranzo al sacco.",
            dogsAllowed = random.choice([0,1]),
            kidsAllowed = random.choice([0,1]),
            minNumPartecipants = randint(7, 12),
            maxNumPartecipants = randint(20, 25),
            )[0]

        t.save()

def populate_events(events_count = 5 ):

    for entry in range(events_count):
        e = Event.objects.get_or_create(
        activity = Activity.objects.all()[randint(0, Activity.objects.count()-1)],
        dateTime = fakegen.date_between_dates(date_start=datetime(2021,3,1), date_end=datetime(2021,12,31)),

        confirmed = random.choice([0,1]),
        )[0]

        #add random partecipants to this event
        for num in range(randint(0, User.objects.count()-1)):
            randUser = User.objects.all()[randint(0, User.objects.count()-1)]
            e.partecipants.add(randUser)

        e.save()

if __name__=="__main__" :

    print("Populating the databases with: ")
    print(sys.argv[1] + " users, ")
    print(sys.argv[2] + " activities and")
    print(sys.argv[3] + " events.")
    print("Please wait....")

    populate_users      (int(sys.argv[1]))
    populate_activities (int(sys.argv[2]))
    populate_events     (int(sys.argv[3]))

    print('Populating Complete!')
