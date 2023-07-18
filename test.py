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
import subprocess

notepad_path = r"C:\Program Files\Notepad++\notepad++.exe"

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
    mypath = 'C:\\Users\\bortolanf\\Downloads\\attachements'
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

        elif change_type == "event_date_changed":

            om = OutMail.create_from_event_change(  user = user,\
                                                    event = event,\
                                                    delta_meet_start = 30,\
                                                    recipient = user,\
                                                    server_address = 'https://www.justwalks.it',\
                                                    change_type = change_type,\
                                                    new_date_or_time = 'Domenica 2 Aprile',\
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
def add_newline(string):
    # Replace any occurrence of ". " with "." to remove the space after the period
    string = string.replace(". ", ".")
    string = string.replace(". ", ".")

    # Add a newline character after each period
    string = string.replace(".", ".\n")

    return string


from datetime import datetime

def formatted_date(date):

    # define the Italian month names
    month_names = {
        1: "Gennaio",
        2: "Febbraio",
        3: "Marzo",
        4: "Aprile",
        5: "Maggio",
        6: "Giugno",
        7: "Luglio",
        8: "Agosto",
        9: "Settembre",
        10: "Ottobre",
        11: "Novembre",
        12: "Dicembre"
    }

    # format the date as "DD Month YYYY"
    formatted_date = date.strftime("%d %B %Y")

    # replace the English month name with the Italian equivalent
    formatted_date = formatted_date.replace('May', 'Maggio')
    formatted_date = formatted_date.replace('June', 'Giugno')
    formatted_date = formatted_date.replace('July', 'Luglio')
    formatted_date = formatted_date.replace('August', 'Agosto')
    formatted_date = formatted_date.replace('September', 'Settembre')
    formatted_date = formatted_date.replace('October', 'Ottobre')
    formatted_date = formatted_date.replace('November', 'Novembre')
    formatted_date = formatted_date.replace('December', 'Dicembre')
    formatted_date = formatted_date.replace('January', 'Gennaio')
    formatted_date = formatted_date.replace('February', 'Febbraio')
    formatted_date = formatted_date.replace('March', 'Marzo')
    formatted_date = formatted_date.replace('April', 'Aprile')

    # print the formatted date
    return formatted_date


def create_FB_Page_event_post(**kwargs):

    id = kwargs['id']
    path = kwargs['path']
    event = Event.objects.get(id=id)

    str_ = add_newline(event.activity.activityDetail)
    str_ = str_ + "\n\n"
    str_ = str_+\
    "\
Evento gratuito aperto al pubblico.\n\
Per iscriversi è necessario:\n\
  1)Registrarsi al sito www.justwalks.it tramite il menu Accesso->Register (o Accesso->Login per chi ha già un account)\n\
  2)Prenotare il biglietto per l'evento(gratuito) all'evento tramite il menu Eventi->Eventi accedere all'evento indicato e seguire la procedura per l'acquisto del biglietto\
\n\
\n\
Per info: 3401461537\n\
Chat whatsapp del gruppo: https://chat.whatsapp.com/CINf8I3ereiBEXqsiePWuP\n\
\n\
A presto!"

    #save FB JustWalks Page event post
    filepath = path + "FB_Page_event_post for " + event.activity.name + ".txt"
    save_and_open(filepath, str_)

def create_FB_groups_share_event_post(**kwargs):

    id = kwargs['id']
    path = kwargs['path']
    delta_meet_start = kwargs['delta_meet_start']

    event = Event.objects.get(id=id)
    start_time = event.start_time(delta_meet_start)
    str_=\
    "\
Ciao a tutti!\n\
Vi segnaliamo il prossimo evento in arrivo a " + event.activity.place + " in data " + formatted_date(event.date) +".\n\n"+\
event.activity.description + "\n\
\n\
Qualche dettaglio in piu:\n\
\n\
Data: "+ formatted_date(event.date) + "\n\
Ritrovo: "+ event.time.strftime('%H:%M') + "\n\
Partenza: "+ start_time.strftime('%H:%M') + "\n\
Luogo: "+ str(event.activity.place) + "\n\
Link al luogo: "+ str(event.activity.meetPlaceLink) + "\n\
\n\
Dislivello: "+ str(event.activity.gradient) + "\n\
Lunghezza: "+ str(event.activity.length) + "Km\n\
Durata: "+ str(event.activity.duration) + "\n\
\n\
Per info:\n\
\n\
Mail:justwalksinfo@libero.it\
\n\
\n\
A presto!"
    #save FB JustWalks Page event post
    filepath = path + "FB_groups_share_event_post for " + event.activity.name + ".txt"
    save_and_open(filepath, str_)

def create_WHATSAPP_post(**kwargs):

    id = kwargs['id']
    path = kwargs['path']
    delta_meet_start = kwargs['delta_meet_start']

    event = Event.objects.get(id=id)
    start_time = event.start_time(delta_meet_start)
    str_=\
    "\
Ciao a tutti!\n\
Vi segnaliamo il prossimo evento in arrivo a " + event.activity.place + " in data " +formatted_date(event.date) +".\n\n"+\
event.activity.description + "\n\
\n\
Qualche dettaglio in piu:\n\
\n\
Data: "+ formatted_date(event.date) + "\n\
Ritrovo: "+ event.time.strftime('%H:%M') + "\n\
Partenza: "+ start_time.strftime('%H:%M') + "\n\
Luogo: "+ str(event.activity.place) + "\n\
Link al luogo: "+ str(event.activity.meetPlaceLink) + "\n\
\n\
Dislivello: "+ str(event.activity.gradient) + "\n\
Lunghezza: "+ str(event.activity.length) + "Km\n\
Durata: "+ str(event.activity.duration) + "\n\
\n\
Maggiori dettagli su:\n\
\n\
https://www.justwalks.it/TravelsApp/SingleActivity/"+ str(event.id)+"\
\n\
\n\
A presto!"
    #save FB JustWalks Page event post
    filepath = path + "WHATSAPP_post for " + event.activity.name + ".txt"
    save_and_open(filepath, str_)


def create_twitter_post(**kwargs):

    id = kwargs['id']
    path = kwargs['path']
    delta_meet_start = kwargs['delta_meet_start']

    event = Event.objects.get(id=id)
    start_time = event.start_time(delta_meet_start)
    str_="\
Trekking in arrivo!:"+"\n\
\n"+\
event.activity.name + "\n\
\n\
Data: "+ formatted_date(event.date) + "\n\
Luogo: "+ str(event.activity.place) + "\n\
\n\
Ritrovo: "+ event.time.strftime('%H:%M') + "\n\
Partenza: "+ start_time.strftime('%H:%M') + "\n\
\n\
Prezzo:Gratuito\
\n\
Dislivello: "+ str(event.activity.gradient) + "\n\
Lunghezza: "+ str(event.activity.length) + "Km\n\
Durata: "+ str(event.activity.duration) + "\n\
\n\
Per info:\n\
Facebook: https://www.facebook.com/groups/221065716882364\
"
    l = len(str_)
    if l>280:
        print("Warning: Twitter post length is:" + str(l) + "(limit is 280)")
    else:
        print("Twitter post length is:" + str(l) + "(limit is 280)")

    filepath = path + "TWITTER_post for " + event.activity.name + ".txt"
    save_and_open(filepath, str_)

def save_and_open(filepath, str_):
    #save FB JustWalks Page event post
    with open(filepath, 'w') as file:
       file.write(str_)

    subprocess.Popen([notepad_path, filepath])


def create_posts(**kwargs):

    create_FB_Page_event_post(**kwargs)
    create_FB_groups_share_event_post(**kwargs)
    create_twitter_post(**kwargs)
    create_WHATSAPP_post(**kwargs)


# Create your tests here.
if __name__ == '__main__':
    #create_posts( id = 49, path="C:\\tmp\\posts\\", delta_meet_start=30)

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

    test_OutMail_create_from_event_change( id = 49,\
                                           change_type='event_incoming',\
                                           target_type='all',\
                                           simulate=False,\
                                           extra_text='')

#    test_OutMail_create_from_event_change( id = 46,\
#                                           change_type='event_date_changed',\
#                                           target_type='event_partecipants',\
#                                           simulate=False,\
#                                           extra_text='')
