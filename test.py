import time
import os
from datetime import datetime
from random import seed
from random import randint
import sys
from TravelsApp.mailer import *

from django.shortcuts import render

# Configure settings for project
# Need to run this before calling models from application!
os.environ.setdefault('DJANGO_SETTINGS_MODULE','TravelsEtc.settings')

import django
from django.contrib.auth import get_user_model
# Import settings
django.setup()
User = get_user_model()


from TravelsApp.models import Setting
from TravelsApp.models import Event
from TravelsApp.models import Order
from TravelsApp.models import OutMail
from TravelsApp.models import UserProfileInfo

from TravelsApp.views import flush


#views.save_setting(name='subscription_duration_months', description = 'Duration of subscription', value=13)

#subscription_duration_months = int(views.get_setting('subscription_duration_months'))
#print(int(subscription_duration_months))
#views.save_setting(name='cancel_interval_hours', description = 'How many hours before the event can be refund', value=48)

'''
def test_open_order():
    #create an order
    print('#create an order')
    user = User.objects.get(email ="flavio.bortolan@gmail.com")
    pk=330


    res, context, order = views.open_order(pk, user)
    #close the order
    print('#close the order')
    views.close_order(order)

    print(context)
'''



def test_Order_open_close():

    pk = Event.objects.all()[0].id
    payer       = User.objects.get(email='flavio.bortolan@gmail.com')
    partecipant = User.objects.get(email='roberto.ferro1996@gmail.com')

    year_subscription_price = int(Setting.get_setting('year_subscription_price'))
    subscription_duration_months = int(Setting.get_setting('subscription_duration_months'))

    (ret, context, o) = Order.open_order(pk, payer, partecipant, year_subscription_price)
    o.close(subscription_duration_months)

def test_OutMail_Create():

    user      = User.objects.get(email='flavio.bortolan@gmail.com')
    recipient = User.objects.get(email='roberto.ferro1996@gmail.com')

    params_dict={}
    params_dict['template'] = 'your_friend_subscibed_you.html'
    params_dict['user'] = user
    params_dict['recipient'] = recipient
    params_dict['password'] = 'drtrot'

    om = OutMail.create( params_dict )
    print(om.subject)
    print(om.html)

    #test event subscription mail
    event = Event.objects.all()[0]

    params_dict={}
    params_dict['template'] = 'event_subcription_successful.html'
    params_dict['user'] = user
    params_dict['recipient'] = recipient
    params_dict['event'] = event

    om = OutMail.create( params_dict )
    print(om.subject)
    print(om.html)

def test_OutMail_create_from_order():

    pk = Event.objects.all()[0].id
    payer       = User.objects.get(email='flavio.bortolan@gmail.com')
    partecipant = User.objects.get(email='roberto.ferro1996@gmail.com')

    year_subscription_price = int(Setting.get_setting('year_subscription_price'))
    subscription_duration_months = int(Setting.get_setting('subscription_duration_months'))

    (ret, context, o) = \
    Order.open_order(pk, payer, partecipant, year_subscription_price)
    o.close(subscription_duration_months)

    om = OutMail.create_from_order( o )

    print(om.subject)
    print(om.html)

def test_OutMail_create_from_site_subscription_completed():

    pk = Event.objects.all()[0].id
    payer       = User.objects.get(email='flavio.bortolan@gmail.com')
    partecipant = User.objects.get(email='roberto.ferro1996@gmail.com')
    password = '£$%DFGS%$'

    om = OutMail.create_from_site_subscription_completed( payer, partecipant, password )

    print(om.subject)
    print(om.html)

def print_outmail_name_surname(event_id):

    evt = Event.objects.get(id=event_id)
    oms = OutMail.objects.filter(subject__contains="Risorgive", status__iexact="notified", template__iexact="event_subcription_successful.html" )

    print("Evento:" + evt.activity.name)
    print("Data:" + str(evt.date))
    print()
    print("Partecipanti:" + str(evt.partecipants.all().count()))
    print()
    print("Mail di conferma spedite:" + str(oms.count()))
    print()
    print()

    for m in oms:
        print ( "ID:" + str(m.id) + ", Acquistato da: " + m.user.first_name + " " + m.user.last_name + ", Mail:" + m.user.username + ", Per: "  + m.recipient.first_name + " " + m.recipient.last_name + ", Mail: " + m.recipient.username   )
        print()

def print_event_partecipants_name_surname(event_id):

    evt = Event.objects.get(id=event_id)

    print("Evento:" + evt.activity.name)
    print("Data:" + str(evt.date))
    print()
    print("Partecipanti:" + str(evt.partecipants.all().count()))
    print()

    for usr in evt.partecipants.all():
        print ( usr.first_name + " " + usr.last_name)

def print_event_partecipants_mail_name_surname(event_id):

    evt = Event.objects.get(id=event_id)

    print("Evento:" + evt.activity.name)
    print("Data:" + str(evt.date))
    print()
    print("Partecipanti:" + str(evt.partecipants.all().count()))
    print()
    usrs = evt.partecipants.all()
    for usr in usrs:
        print ( "Mail: " + usr.username + " Nome: " + usr.first_name + " Cognome: " + usr.last_name)

    import pandas as pd
    df = pd.DataFrame(list(evt.partecipants.all().values( 'last_name', 'first_name', 'email'))).sort_values('last_name')
    df.to_excel('C:\\tmp\\' + evt.activity.name + '.xls')

def print_users():

    print("Soci:" + str(User.objects.all().count()))
    print()

    for usr in User.objects.all():
        print ( "Mail: " + usr.username + " Nome: " + usr.first_name + " Cognome: " + usr.last_name)

from django.test.client import Client

def test_request(url):

    client = Client(SERVER_NAME='127.0.0.1')
    response = client.get(url)
    request = response.wsgi_request

    print('request.build_absolute_uri(): ' + request.build_absolute_uri())

    import re
    m = re.search(r"(http\w*:\/\/[\w\.\d\:]*\/)", request.build_absolute_uri())

    #parameters extraction
    site_address = m.group(0)

    print(site_address)

def test_mail_validation(email):
    from django.forms import EmailField
    from django.core.exceptions import ValidationError

    try:
        EmailField().clean(email)
        print('mail is OK')
        return True

    except ValidationError:
        print('mail is NOT OK')
        return False

def test_logging(msg):
    import logging
    logger = logging.getLogger('logger')
    logger.info('this is an information')
    logger.error('this is an error')


def populate_dummy_users(users_count = 10):

    id=1
    for entry in range(users_count):

        fake_first_name = 'folletto'
        fake_last_name = 'dei_boschi' + '_' + str(id)
        fake_email =  fake_first_name + '.' + fake_last_name + '@foresta.magica.com'
        fake_number = "3401461555"

        #new entry
        u    = User           .objects.get_or_create(username = fake_email, first_name = fake_first_name,last_name= fake_last_name,email = fake_email)[0]
        print('Created User:' + str(u) )

        pi   = UserProfileInfo.objects.get_or_create(user=u, phone_number = fake_number, credits = randint(15, 40))[0]
        print('Created UserProfileInfo:' + str(pi) )

        u.save()
        print('user saved')

        pi.user = u
        print('UserProfileInfo assigned to user')

        pi.save()
        print('UserProfileInfo saved')
        id=id+1

def test_mail():

    e=Event.objects.all()[0]
    user = User.objects.filter(email='flavio.bortolan@gmail.com')[0]

    company_mail = Setting.get_setting('company_email')
    smtp_server = Setting.get_setting('company_email_smtp_server')
    pw          = Setting.get_setting('company_email_password')

    #m = Mailer(sender='roberto.ferro1996@gmail.com', smtp_server = "smtp.gmail.com", password = 'margherita1')
    m = mailer.Mailer(sender_email=company_mail, smtp_server = smtp_server, password = pw)
    m.login()

    response = render(None, 'TravelsApp/free_ticket_message.html', {'event':e, 'user': user})
    html=str(response.content.decode('UTF-8'))

    m.send_mail(user.email, "buongiorno da mailer", html, html)
    m.quit()

def add_to_sent_file(sent_list_file, email):
    with open(sent_list_file, 'a') as the_file:
        the_file.write(email + '\n')

def test_OutMail_create_from_event_change(**kwargs):

    id = kwargs['id']
    change_type = kwargs['change_type']
    target_type =  kwargs['target_type']
    simulate =  kwargs['simulate']
    extra_text = kwargs['extra_text']

    event = Event.objects.get(id=id)

    from os import listdir
    from os.path import isfile, join
    mypath = 'C:\\tmp\\attachements'
    attachements = [mypath + '\\'+ f for f in listdir(mypath) if isfile(join(mypath, f))]
    #attachements = ['C:\\tmp\\a.jpeg']
    print(attachements)

    if target_type == "event_partecipants":

        tgt = event.partecipants.filter(userprofileinfo__is_minor = False)

    elif target_type=="all":

        tgt = User.objects.filter(userprofileinfo__is_minor = False)
        #tgt = User.objects.filter(email ="flavio.bortolan@gmail.com")
    else:
        return

    sent_list = []
    try:

        sent_list_file = "C:\\tmp\\sent.txt"
        with open(sent_list_file) as file:
            lines = [line.rstrip() for line in file]
        sent_list = "-".join(lines)

    except:
        print('no sent list available')

    delay = 60

    for user in tgt:

        skip = False
        simulate_ = simulate

        if ( "folletto" in user.email ):
            skip = True
        elif  'flavio.bortolan' in  user.email:
            skip = False
            simulate_ = False

        elif user.email in sent_list:
            print(user.email + "already received mail, not sending")
            skip = True
        else:
            skip = False

        if change_type == "event_incoming":

            om = OutMail.create_from_event_change(user=user, event=event, server_address= "https://www.justwalks.it", change_type='event_incoming', delta_meet_start=30, recipient=user, extra_text = extra_text)

        elif change_type == "event_change":

            om = OutMail.create_from_event_change(  user = user,\
                                                    event = event,\
                                                    delta_meet_start = 30,\
                                                    recipient = user,\
                                                    server_address = 'https://www.justwalks.it',\
                                                    change_type = 'event_cancelled',\
                                                    new_date_or_time = '',\
                                                    change_reason = ' a causa delle condizioni meteo')

        #om = OutMail.create_from_event_change(user, event, "https://www.justwalks.it", 'event_confirmed', '', '', "")

        if skip == False:

            if simulate_ == False:
                try:
                    print('sendig mail to:' + user.email)
                    m = Mailer(sender_email=Setting.get_setting('company_email'), smtp_server = Setting.get_setting('company_email_smtp_server'), password = Setting.get_setting('company_email_password'))
                    #send mail
                    r = m.flush_outmail(om, attachements)

                    if str(r)=="{}":
                        add_to_sent_file(sent_list_file, user.email)

                    time.sleep(delay)

                except Exception as e:
                    print('Could not send mail: ' + str(e))

            else:
                print("simulating mail to :" + user.email)
        else:
            print('SKIPPING sendig mail to:' + user.email)



    #print(om.subject)
    #print(om.html)

# Create your tests here.
if __name__ == '__main__':

    #print_users()
    #populate_dummy_users(users_count = 10)
    #test_mail()
    #test_Order_open_close()
    #test_OutMail_create_from_site_subscription_completed()
    #print_event_partecipants_mail_name_surname(36)
    #print_event_partecipants_name_surname(27)
    #print_users()
    #print_outmail_name_surname(19)
    #test_request('http://127.0.0.1:8000/TravelsApp/events/all/')
    #test_mail_validation('Roberto_son_of_flavio.bortolan@gmail.com')
    #test_logging("ciao ciao")

    test_OutMail_create_from_event_change( id = 44,\
                                           change_type='event_incoming',\
                                           target_type='all',\
                                           simulate=False,\
                                           extra_text='ATTENZIONE: La precedente mail riportava una data errata per cui vi preghiamo di ignorarla.')
