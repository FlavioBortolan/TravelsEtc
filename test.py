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

# Create your tests here.
if __name__ == '__main__':
    #test_mail()
    test_Order_open_close()
