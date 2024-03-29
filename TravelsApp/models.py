import re
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import RegexValidator
import time
from dateutil.relativedelta import *
from dateutil.rrule import *


import datetime
from datetime import datetime
from  datetime import date
from datetime import timedelta

import ast

from bs4 import  BeautifulSoup

# SuperUserInformation
# User: Jose
# Email: training@pieriandata.com
# Password: testpassword

# Create your models here.
class UserProfileInfo(models.Model):

    # Create relationship (don't inherit from User!)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # pip install pillow to use this!
    # Optional: pip install pillow --global-option="build_ext" --global-option="--disable-jpeg"
    profile_pic = models.ImageField(upload_to='TravelsApp/profile_pics',blank=True)
    phone_number = models.CharField(validators=[RegexValidator(regex=r'^(( *0 *0 *| *\+) *3 *9 *)?((\d *){3})((\d *){6,7})$', message="Phone number must be entered like: 340 1461538. Up to 10 digits allowed. Only digits, no other character allowed.")], max_length=64, blank=True)
    credits = models.PositiveIntegerField(default=0)
    exp_date = models.DateField(default = timezone.now)
    is_minor = models.BooleanField(default=False)
    parent = models.ForeignKey(User, related_name='parent', on_delete=models.CASCADE, blank=True, default=None, null=True)
    activation_code = models.CharField(max_length=64, blank=True)

    USER_TYPE_CHOICES = [
        ('Std', 'Standard'),
        ('Amb', 'Ambassador'),
        ('Lead', 'Leader'),
        ('Emp', 'Employee'),
    ]
    user_type = models.CharField(
        max_length=4,
        choices=USER_TYPE_CHOICES,
        default='Std',)

    def __str__(self):
        # Built-in attribute of django.contrib.auth.models.User !
        return self.user.username

class Activity(models.Model):

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=512)
    place = models.CharField(max_length=100)
    #partecipants
    type = models.CharField(max_length=100)
    price = models.PositiveIntegerField(default = 15)
    #confirmed
    duration = models.FloatField(default = 3.5)
    activityDetail = models.CharField(max_length=2048, default="xxxxxxxxxxxxxxxxxx")
    difficultyLevel = models.CharField(max_length=8, default="E")
    length = models.FloatField(default=4)
    gradient = models.FloatField(default=300)
    streetType = models.CharField(max_length=600, default="Sterrato e asfalto")
    dogsAllowed = models.BooleanField(default=False)
    kidsAllowed = models.BooleanField(default=False)
    meetPlaceLink = models.CharField(max_length=600, default = "https://www.google.com/maps/place/45%C2%B050'14.3%22N+11%C2%B044'11.2%22E/@45.8373125,11.7342488,17z/data=!3m1!4b1!4m5!3m4!1s0x0:0x0!8m2!3d45.8373125!4d11.7364375" )
    meetPlaceDirections = models.CharField(max_length=600, default ="Verso Marostica ")
    leader = models.CharField(max_length=64)
    whatToBring = models.CharField(max_length=600, default = "Pranzo al sacco, acqua, crema solare, scarpe da trekking")
    minNumPartecipants = models.PositiveIntegerField(default=10)
    maxNumPartecipants = models.PositiveIntegerField(default=20)

    def __str__(self):
    # Built-in attribute of django.contrib.auth.models.User !
        return self.name + ' ' + self.place


class Order(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default = timezone.now)
    time = models.TimeField(default = timezone.now)
    status = models.CharField(max_length=24, default="chart")
    items = models.CharField(max_length=600, default="")
    total = models.PositiveIntegerField(default=0)
    credits_to_use = models.PositiveIntegerField(default=0)
    payment_id = models.CharField(max_length=200, default="xyz")

    #opens an order for one single event and for the specified partecipant
    #if the partecipant subscription expires before the event date, a subscripion item is addedo to the order
    @classmethod
    def open_order(cls, pk, payer, partecipant, year_subscription_price):

       print('*** open order ***: payer = ' + payer.email + ', partecipant = ' + partecipant.email)

       sub_total = 0
       max_exp_date = date.today()

       e = Event.objects.get( id = pk )
       sub_total += e.activity.price

       #check if an event requires subscription to be renewed
       subscription_expired = e.date > partecipant.userprofileinfo.exp_date

       print('cost of tickets:' + str(sub_total))

       if subscription_expired:
          sub_total += year_subscription_price
          print('with subscription:' + str(sub_total))

       #check user credits
       credits = payer.userprofileinfo.credits
       print('payer credits:' + str(credits))

       if sub_total > credits:
           print('#total sum is partially  paid with credits')
           credits_to_use = credits
           total = sub_total - credits_to_use
       else:
          print('total sum is paid with credits')
          credits_to_use = sub_total
          total = 0

       print('Total to be paid with card:' + str(total))

       items=[]
       items.append({'type':'event_ticket_purchase', 'pk': pk, 'partecipant': partecipant.email})

       if subscription_expired:
          items.append({'type':"subscription", 'partecipant': partecipant.email} )

       #Create the order
       o = Order.objects.create(user=payer, date=date.today(), time=datetime.now(), status="chart", items=str(items), total=total, credits_to_use=credits_to_use )
       o.save()
       print('Order saved:' + str(o))

       e = Event.objects.get( id = pk )

       context = {}
       context['subs_exp_date'] = partecipant.userprofileinfo.exp_date
       context['subscription_expired'] = subscription_expired
       context['year_subscription_price'] = year_subscription_price
       context['sub_total'] = sub_total
       context['total'] = total
       context['credits_to_use'] = credits_to_use
       context['event'] =  e
       context['order_id'] = o.id

       return (True, context, o)

    #closes a specific order after payment is completed
    def close(self, subscription_duration_months):

        print('*** close_order ***')
        if self.status=="completed":
            return False

        #retrive the user
        user = self.user
        print('User: ' + user.email)
        #retrive the articles in the orders
        items = ast.literal_eval(self.items)

        print('User had: ' + str(user.userprofileinfo.credits) + 'credits')
        #subtract credits used
        if self.credits_to_use > 0:
            user.userprofileinfo.credits-=self.credits_to_use
            user.userprofileinfo.save()

        print('User now has: ' + str(user.userprofileinfo.credits) + 'credits')

        try:

            for i in items:

                partecipant = User.objects.get(email=i['partecipant'])

                if i['type'] == 'event_ticket_purchase':

                    e=Event.objects.get(id=int(i['pk']))

                    print('Order contains ticket for event : ' + str(e.activity.name) +' on date:' + str(e.date))
                    print('The target partecipant is:' + i['partecipant'])
                    print('credits to be used : ' + str(self.credits_to_use))
                    print('order total:' + str(self.total))

                    #add user to event
                    e.partecipants.add(partecipant)

                    #remove him from the queue if he was in the queued_partecipants
                    if e.queued_partecipants.filter(email=partecipant.email).count()>0:
                        e.queued_partecipants.remove(partecipant)
                        print('removed user ' + partecipant.email + ' from the queue of event ' + e.activity.name)

                    #Create the ticket
                    t = Ticket.objects.create(user=partecipant, event=e, order=self, status = 'valid')
                    t.save()
                    e.save()

                elif i['type'] == 'subscription':

                    partecipant.userprofileinfo.exp_date = datetime.today() + relativedelta(months=+subscription_duration_months)
                    partecipant.userprofileinfo.save()
                    print('Order contains subscription, user subscription now expires on ' + str(user.userprofileinfo.exp_date) )

        except Exception as e:
            print('Exception processing order items:' + str(e))
            return False

        self.status = "completed"
        self.save()

        return True

    def __str__(self):
    # Built-in attribute of django.contrib.auth.models.User !
        return "ID: " + str(self.id) + ", Total: " + str(self.total) + ", credits_to_use: " + str(self.credits_to_use) + ", items: " + str(self.items)

class Event(models.Model):

    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    date = models.DateField(default = timezone.now)
    #meet time
    time = models.TimeField(default = timezone.now)
    partecipants = models.ManyToManyField(User, blank=True)
    queued_partecipants = models.ManyToManyField(User, related_name='my_queued_events', blank=True)
    confirmed = models.BooleanField(default=False)
    #how may hours prior to event begin user can still ask refund
    refund_limit_delta_hours =  models.PositiveIntegerField(default = 48)

    def start_time(self, delta):

        #inject the tour start time calculated from meet time + 30 mins
        st = datetime.combine(self.date, self.time) + timedelta(minutes = delta)
        return st.time()

    def __str__(self):
        return "ID: " + str(self.id) + ", Date: " + str(self.date) + str(self.activity)

class Ticket(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    status = models.CharField(max_length=30, default="valid")

class Setting(models.Model):

    name  = models.CharField(max_length=128)
    value = models.CharField(max_length=128)
    description = models.CharField(max_length=128)

    @classmethod
    def get_setting(cls, name):
        r = Setting.objects.get(name=name).value
        return r

    @classmethod
    def save_setting(cls, name, value, description):
        s = Setting.objects.get_or_create( name=name)[0]
        s.value = value
        s.description = description
        s.save()


    def __str__(self):
        return "name: " + str(self.name) + ", value: " + str(self.value)

class OutMail(models.Model):

    #user: the user that triggered the generation of this message
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipient')
    template = models.CharField(max_length=64)
    html = models.CharField(max_length=2048)
    subject = models.CharField(max_length=64)
    status = models.CharField(max_length=32)

    @classmethod
    def create(cls, params_dict):

        om = cls(template = params_dict['template'],   \
                 user = params_dict['user'],           \
                 recipient = params_dict['recipient'], \
                 status = 'created' )


        response = render(None, 'TravelsApp/' + om.template ,  params_dict)
        om.html = str(response.content.decode('UTF-8'))

        soup = BeautifulSoup(om.html)

        om.subject =soup.find(id='Subject').text

        om.save()

        return om

    @classmethod
    def create_from_event_change(cls, **kwargs):


        kwargs['start_time'] = kwargs['event'].start_time(kwargs['delta_meet_start'])
        kwargs['template']  = 'event_changed.html'


        om = cls.create( kwargs )
        return om

    @classmethod
    def create_from_event_change_old(cls, user, event,  server_address, change_type, change_reason, new_date_or_time, notes=''):

        dict              = {}
        dict['template']  = 'event_changed.html'
        dict['user']      = user
        dict['recipient'] = user
        dict['event'] = event
        dict['server_address'] = server_address
        dict['change_type'] = change_type
        dict['new_date_or_time'] = new_date_or_time
        dict['change_reason'] = change_reason

        if notes!='':
            dict['notes'] = notes



        om = cls.create( dict )
        return om


    #retrives the name of the server from the request
    @classmethod
    def server_address_from_request(cls, request):
        m = re.search(r"(http\w*:\/\/[\w\.\d\:]*)", request.build_absolute_uri())
        return m.group(0)

    @classmethod
    def create_from_order(cls, order, request):

        if order.status != 'completed':
            raise ValueError('Tryng to generate confirmation message from an order not yet closed')

        dict = {}
        dict['user'] = order.user

        #get the server name
        dict['server_address'] = cls.server_address_from_request(request)

        #turn request into a dictionary and merge it with existing
        #dict  =  {**dict, **vars(request)}

        #retrive the articles in the orders
        items = ast.literal_eval(order.items)
        found = False

        for i in items:

            partecipant = User.objects.get(email=i['partecipant'])

            if i['type'] == 'event_ticket_purchase':

                #generates different message based on minor status
                if partecipant.userprofileinfo.is_minor == True:

                    dict['template'] = 'event_subcription_successful_minor.html'
                    dict['minor'] = partecipant
                    dict['recipient'] = dict['user']

                else:

                    dict['template'] = 'event_subcription_successful_adult.html'
                    dict['recipient'] = partecipant

                dict['event'] = Event.objects.get(id=int(i['pk']))

                if found == True:
                    raise ValueError('Error tryng to generate message mail from order with multiple partecipants')

                found = True


        om = cls.create(dict)
        return om

    @classmethod
    def create_from_registration_code(cls, request, user, registration_code):

        dict              = {}
        dict['request']   = request
        dict['user']      = user
        dict['recipient'] = user

        #get the server name
        dict['server_address'] = cls.server_address_from_request(request)
        dict['template']  = 'create_from_registration_code.html'
        dict['registration_code']  = registration_code

        om = cls.create( dict )
        return om


    #creates a mail sent when user has bought ticket for someone else
    #ticket_target_user=minor => user has bought for a kid
    #ticket_target_user=minor => friend has bought for a friend
    @classmethod
    def create_from_site_subscription_completed(cls, user, new_user, password, ticket_target_user, request):

        dict              = {}
        dict['user']      = user
        #get the server name
        dict['server_address'] = cls.server_address_from_request(request)

        if ticket_target_user == 'minor':

            dict['recipient'] = user
            dict['minor'] = new_user
            dict['template']  = 'minor_subscibed.html'

        elif ticket_target_user == 'friend':

            dict['recipient'] = new_user
            dict['template']  = 'your_friend_subscibed_you.html'
            dict['password']  = password

        else:
            raise ValueError("Unexpected value for ticket_target_user:" + ticket_target_user)

        om = cls.create( dict )
        return om

        @classmethod
        def create_from_registration_code(cls, request, registration_code):

            dict              = {}
            dict['request']   = request
            #get the server name
            dict['server_address'] = cls.server_address_from_request(request)
            dict['template']  = 'create_from_registration_code.html'
            dict['registration_code']  = registration_code

            om = cls.create( dict )
            return om
