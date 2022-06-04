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

def test_mail():

    e=Event.objects.all()[0]
    user = User.objects.filter(email='flavio.bortolan@gmail.com')[0]

    company_mail = Settings.get_setting('company_email')
    smtp_server = Settings.get_setting('company_email_smtp_server')
    pw          = Settings.get_setting('company_email_password')

    #m = Mailer(sender='roberto.ferro1996@gmail.com', smtp_server = "smtp.gmail.com", password = 'margherita1')
    m = Mailer(sender=company_mail, smtp_server = smtp_server, password = pw)
    m.login()

    response = render(None, 'TravelsApp/free_ticket_message.html', {'event':e, 'user': user})
    html=str(response.content.decode('UTF-8'))

    m.send_mail(user.email, "buongiorno da mailer", html, html)
    m.quit()

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

    for usr in evt.partecipants.all():
        print ( "Mail: " + usr.username + " Nome: " + usr.first_name + " Cognome: " + usr.last_name)

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

def test_OutMail_create_from_event_change(id, target_type):

    event = Event.objects.get(id=id)

    if target_type == "event_partecipants":

        tgt = event.partecipants.all()

    elif target_type=="all":

        tgt = User.objects.all()
        #tgt = User.objects.get(email ="flavio.bortolan@gmail.com")

    for user in tgt:
        om = OutMail.create_from_event_change(user, event, "https://flaviobortolan.pythonanywhere.com/", 'event_incoming', '', '', "")
        r=flush(om)

    #print(om.subject)
    #print(om.html)

# Create your tests here.
if __name__ == '__main__':

    #populate_dummy_users(users_count = 10)
    #test_mail()
    #test_Order_open_close()
    #test_OutMail_create_from_site_subscription_completed()
    #print_event_partecipants_mail_name_surname(21)
    #print_event_partecipants_name_surname(27)
    #print_users()
    #print_outmail_name_surname(19)
    #test_request('http://127.0.0.1:8000/TravelsApp/events/all/')
    #test_mail_validation('Roberto_son_of_flavio.bortolan@gmail.com')
    #test_logging("ciao ciao")
    test_OutMail_create_from_event_change(27, 'all')
