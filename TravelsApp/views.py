from django.shortcuts import render
from .forms import UserForm,UserProfileInfoForm
from .forms import DivErrorList
# Extra Imports for the Login and Logout Capabilities
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView)
from .models import Activity
from .models import Event
from .models import Setting

from django.contrib.auth import get_user_model
from datetime import *
import time
from dateutil.relativedelta import *
from dateutil.rrule import *
from datetime import datetime

User = get_user_model()

import logging
logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
    print("this is the index page")
    return render(request,'TravelsApp/index.html')


@login_required
def special(request):
    # Remember to also set login url in settings.py!
    # LOGIN_URL = '/TravelsApp/user_login/'
    return HttpResponse("You are logged in. Nice!")

@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return HttpResponseRedirect(reverse('index'))

def register(request):

    registered = False

    #this flag tells the html page that it is rendered because a POST was issued.
    #and will use this info to preserve the login info in case registration was not correct
    post_response = False

    if request.method == 'POST':

        post_response=True

        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        user_form = UserForm(data=request.POST, error_class=DivErrorList)
        profile_form = UserProfileInfoForm(data=request.POST, error_class=DivErrorList)

        #profile_form.is_valid()
        #print('POST:' + profile_form.cleaned_data['subscription_exp_date'])
        # Check to see both forms are valid
        if user_form.is_valid() and profile_form.is_valid():

            #get the email supplied trough the form
            supplied_email = user_form.cleaned_data['email']
            print("Supplied mail is:" + supplied_email)
            #check if someone else in the database used that email
            duplicate_users = User.objects.filter(email__iexact = supplied_email).count()

            if duplicate_users == 0:

                print("No duplicate users found")

                # Save User Form to Database
                user = user_form.save(commit=False)

                #assign username to be equal to email
                user.username = supplied_email

                user.save()

                # Hash the password
                user.set_password(user.password)

                # Update with Hashed password
                user.save()

                # Now we deal with the extra info!

                # Can't commit yet because we still need to manipulate
                profile = profile_form.save(commit=False)

                # Set One to One relationship between
                # UserForm and UserProfileInfoForm
                profile.user = user

                # Check if they provided a profile picture
                if 'profile_pic' in request.FILES:
                    print('found it')
                    # If yes, then grab it from the POST form reply
                    profile.profile_pic = request.FILES['profile_pic']

                subscription_duration_months = int(get_setting('subscription_duration_months'))

                #subscription expires after one year, when payment is implemented this will shitf after payment....
                profile.exp_date = datetime.today() + relativedelta(months=+subscription_duration_months)

                # Now save model
                profile.save()

                # Registration Successful!
                registered = True

                user = authenticate(username=supplied_email,
                                    password=user_form.cleaned_data['password'],
                                    )
                login(request, user)

            else:
                # One of the forms was invalid if this else gets called.
                print("Duplicate users where found: There are " + str(duplicate_users) + " users with email " + supplied_email)
        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors,profile_form.errors)

    #GET
    else:

        print('register:GET')
        # Just render the forms as blank.
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request,'TravelsApp/registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered,
                           'post_response': post_response })

def my_account(request):

    data_change_successful = False
    credits = request.user.userprofileinfo.credits

    if request.method == 'POST':

        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        user_form = UserForm(data=request.POST, error_class=DivErrorList)
        profile_form = UserProfileInfoForm(data=request.POST, error_class=DivErrorList)

        #disable editing email
        user_form.fields['email'].widget.attrs['disabled'] = True

        #Hide password
        user_form.fields['password'].widget = user_form.fields['email'].hidden_widget()
        user_form.fields['repeat_password'].widget = user_form.fields['repeat_password'].hidden_widget()

        #check if data is valid
        user_form.is_valid()
        profile_form.is_valid()

        # check if fields we care about are clean. a field is clean if it has been put in the 'cleaned_data' dict
        if 'first_name' in user_form.cleaned_data and 'last_name' in user_form.cleaned_data and 'phone_number' in profile_form.cleaned_data :

            request.user.first_name = user_form.cleaned_data['first_name']
            request.user.last_name = user_form.cleaned_data['last_name']

            request.user.userprofileinfo.phone_number = profile_form.cleaned_data['phone_number']
            request.user.userprofileinfo.profile_pic = profile_form.cleaned_data['profile_pic']

            request.user.save()
            request.user.userprofileinfo.save()
            data_change_successful = True

        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors,profile_form.errors)

    #GET
    else:
        # Just render the forms as blank.
        user_form = UserForm(initial = {'first_name': request.user.first_name,
                                        'last_name': request.user.last_name,
                                        'email': request.user.email,
                                        })
        profile_form = UserProfileInfoForm(initial = {'phone_number': request.user.userprofileinfo.phone_number, 'exp_date': request.user.userprofileinfo.exp_date})

        #disable editing email
        user_form.fields['email'].widget.attrs['disabled'] = True

        #Hide password
        user_form.fields['password'].widget = user_form.fields['email'].hidden_widget()
        user_form.fields['repeat_password'].widget = user_form.fields['repeat_password'].hidden_widget()


    #Discard errors on the password as we do not edit it here
    user_form.errors['password'] = None
    user_form.errors['repeat_password'] = None

    return render(request,'TravelsApp/my_account.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'data_change_successful':data_change_successful,
                           'credits': credits,})

def change_password(request):

    data_change_successful = False

    #handle POST, in case of GET we just return the forms created above
    if request.method == 'POST':

        user_form = UserForm(data=request.POST, error_class=DivErrorList)

        #Hide
        user_form.fields['first_name'].widget = user_form.fields['first_name'].hidden_widget()
        user_form.fields['last_name'].widget = user_form.fields['last_name'].hidden_widget()
        user_form.fields['email'].widget = user_form.fields['email'].hidden_widget()

        #check if data is valid
        user_form.is_valid()

        # check if fields we care about are clean. a field is clean if it has been put in the 'cleaned_data' dict
        if 'password' in user_form.cleaned_data and 'repeat_password' in user_form.cleaned_data :

            request.user.set_password(user_form.cleaned_data['password'])
            request.user.save()
            data_change_successful = True

        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors)
    else:
        user_form = UserForm()

        #Hide
        user_form.fields['first_name'].widget = user_form.fields['first_name'].hidden_widget()
        user_form.fields['last_name'].widget = user_form.fields['last_name'].hidden_widget()
        user_form.fields['email'].widget = user_form.fields['email'].hidden_widget()


    #Discard errors on the password as we do not edit it here
    user_form.errors['first_name'] = None
    user_form.errors['last_name'] = None
    user_form.errors['email'] = None

    return render(request,'TravelsApp/change_password.html',
                          {'user_form':user_form,
                           'data_change_successful': data_change_successful})

def user_login(request):

    #change this to login with a username=mail

    if request.method == 'POST':
        # First get the username and password supplied
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=email, password=password)

        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request,user)
                # Send the user back to some page.
                # In this case their homepage.
                return HttpResponseRedirect(reverse('index'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used email: {} and password: {}".format(email,password))

            return render(request, 'TravelsApp/login.html', {'post_response': 'failed login', 'err_message': 'Invalid email or password, please try again'})
    else:
        #Nothing has been provided for username or password.
        return render(request, 'TravelsApp/login.html', {})

class EventListView(LoginRequiredMixin, ListView):

    login_url = '/login/'
    redirect_field_name = 'events'
    template_name = 'TravelsApp/event_list.html'
    model = Event

    #defines the set of elments to be shown (GET)
    #note: *args    = positional arguments in the url call
    #      **kwargs = name-based arguments in the url call
    def get_queryset(self,*args, **kwargs):
        print('***get_queryset: kwargs' + str(**kwargs) + '***')
        if self.kwargs['filter_mode']=='current_user':
            logger.error('filter_mode:' + self.kwargs['filter_mode'] + ', verranno mostrate solo le attivita dell utente attuale')
            return(self.request.user.event_set.all())

        elif self.kwargs['filter_mode']=='all':
            logger.error('filter_mode:' + self.kwargs['filter_mode'] + ', verranno mostrate tutte le attivita')
            return(Event.objects.all())

    #defines the context dictionary to be used to render page during GET
    def get_context_data(self, **kwargs):
        print('***get_context_data: kwargs' + str(kwargs) + '***')
        context  = super().get_context_data(**kwargs)
        context['filter_mode'] = self.kwargs['filter_mode']

        if self.kwargs['filter_mode']=='current_user':
            logger.error('filter_mode:' + self.kwargs['filter_mode'] + ', verranno mostrate solo le attivita dell utente attuale')

            user_events = self.request.user.event_set.all()
            context['event_list']       = user_events.filter(date__gte = date.today())


        elif self.kwargs['filter_mode']=='current_user_past':
            logger.error('filter_mode:' + self.kwargs['filter_mode'] + ', verranno mostrate solo le attivita passate dell utente attuale')

            user_events = self.request.user.event_set.all()
            context['event_list']  = user_events.filter(date__lt = date.today())

        elif self.kwargs['filter_mode']=='all':
            logger.error('filter_mode:' + self.kwargs['filter_mode'] + ', verranno mostrate tutte le attivita')

            #exclude past events
            context['event_list'] = Event.objects.filter(date__gte = date.today())

        delta_months = 2
        start_date = time.strftime("%Y-%M-%d", time.strptime(str(date.today()), '%Y-%M-%d'))
        context['start_date'] = start_date

        end_date = time.strftime("%Y-%M-%d", time.strptime(str(date.today() + relativedelta(months=+delta_months)), '%Y-%M-%d'))
        context['end_date'] = end_date

        context['delta_months'] = delta_months

        print('GET:start_date: ' + start_date)
        print('GET:end_date: ' + end_date)

        return context

    #Handles the 'POST' request from the client browser
    def post(self, request, *args, **kwargs):
        logger.error('POST: filter_mode:' + self.kwargs['filter_mode'] + ', verranno mostrate le attivita corrispondenti ai filtri')

        #get the filter criteria from the POST request(city, start_date etc)
        #these values comes from the form field inside the web page
        city = request.POST.get("city")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        type = request.POST.get("type")
        difficultyLevel = request.POST.get("difficultyLevel")
        confirmed = request.POST.get("confirmed")

        #Log filter values for debug purposes
        logger.error('POST data:')
        logger.error('City:' + city)
        logger.error('StartDate:' + str(start_date))
        logger.error('EndDate:' + str(end_date))
        query = {}

        #incremental filter by active fields
        filtered_events = Event.objects.all()

        #exclude past events
        filtered_events = filtered_events.filter(date__gte = date.today())

        if city:
            filtered_events = filtered_events.filter(activity__place__iexact = city)

        if type!='NoSelection' and type !='':
            print('filtering events with type =*' + type + '*')
            filtered_events = filtered_events.filter(activity__type = type)

        if confirmed!='NoSelection' and confirmed !='':
            print('filtering events with confirmed =*' + str(confirmed) + '*')
            if confirmed == 'confirmed':
                filtered_events = filtered_events.filter(confirmed = True)

        if difficultyLevel!='NoSelection' and difficultyLevel !='':
            print('filtering events with difficultyLevel =*' + difficultyLevel + '*')
            filtered_events = filtered_events.filter(activity__difficultyLevel = difficultyLevel)

        if start_date:
            print('filtering events with start date >' + start_date )
            filtered_events = filtered_events.filter(date__gte = start_date)

        if end_date:
            print('filtering events with end date >' + end_date)
            filtered_events = filtered_events.filter(date__lte = end_date)



        #renders the page with the context dictionary elements set to the values
        #previously calculated
        return render(request,
                      self.template_name,
                      {'event_list': filtered_events,
                       'filter_mode':'apply_filter',
                       'city': city,
                       'start_date': time.strftime("%Y-%M-%d", time.strptime(start_date, '%Y-%M-%d')),
                       'end_date': end_date,
                       'type': type,
                       'difficultyLevel': difficultyLevel,
                       'confirmed': confirmed

                       })

#EVENT MANAGEMENT
class SingleEvent(DetailView):
    model = Event

    def get_queryset(self,*args, **kwargs):
        #logger.error('get_queryset:Selected single activity')
        return(Event.objects.filter(id=self.kwargs['pk']))

    def get_context_data(self,**kwargs):
        context  = super().get_context_data(**kwargs)

        if self.request.user.event_set.filter(id=self.kwargs['pk']).count()>0:
            context['user_already_has_this_ticket'] = True
            logger.error('The user already has this ticket')
        else:
            context['user_already_has_this_ticket'] = False
            logger.error('The user does not have this ticket')

        if self.request.user.my_queued_events.filter(id=self.kwargs['pk']).count()>0:
            context['queued_to_this_event'] = True
            logger.error('The user is queued to the event')
        else:
            context['queued_to_this_event']  = False
            logger.error('The user is not queued to the event')


        event = Event.objects.filter(id=self.kwargs['pk'])[0]

        #inject the name of the image of the event
        context['event_image_name'] = 'Images/' + event.activity.name + '.jpg'

        #inject the tour start time calculated from meet time + 30 mins
        dt = datetime.combine(event.date, event.time) + timedelta(minutes=30)
        context['start_time'] = dt.time

        #detect if it is possible to ask for refund
        refund_limit_time = dt - timedelta(hours=48)
        if  refund_limit_time > datetime.now() and context['user_already_has_this_ticket']:
            context['can_ask_refund'] = True
            print('The guy can have his money back as:' + str(refund_limit_time) + '>' + str(datetime.now()))
        else:
            context['can_ask_refund'] = False
            print('The guy cannot have his money back as:' + str(refund_limit_time) + '<' + str(datetime.now()))

        return context

class BuyTicketView(TemplateView):
    template_name = "TravelsApp/buyticket.html"

    def get_context_data(self,**kwargs):
        context  = super().get_context_data(**kwargs)
        context['Event_pk'] =  kwargs['pk']
        context['buy_step'] =  kwargs['buy_step']

        #if the purchase is confirmed add this activity to user's Activities
        if kwargs['buy_step']=='confirmed':
            a = Event.objects.get(id=kwargs['pk'])
            a.partecipants.add(self.request.user)

        return context

class AskRefundView(TemplateView):
    template_name = "TravelsApp/ask_refund.html"

    def get_context_data(self,**kwargs):
        context  = super().get_context_data(**kwargs)
        context['event'] = Event.objects.get(id=kwargs['pk'])
        context['refund_step'] =  kwargs['refund_step']

        return context

    #Handles the 'POST' request from the client browser
    def post(self, request, *args, **kwargs):

        refund = request.POST.get("refund")
        print('Post: refund requested: ' + str(refund))

        context  = super().get_context_data(**kwargs)
        context['event'] = Event.objects.get(id=kwargs['pk'])
        context['refund_step'] =  2

        #check if user is subscribed, this is to avoid a user arrives here with the 'back' button after having already unsubscribed
        if request.user in context['event'].partecipants.all():

            context['user_subscribed'] = True

            if refund == 'Credits':
                #add value of the event to user's Credits
                request.user.userprofileinfo.credits += context['event'].activity.price
                print ('refunding Credits...')
                request.user.userprofileinfo.save()
                context['event'].partecipants.remove(request.user)
                context['event'].save()
                print ('done')
            else:
                #bank transfer to Card
                print ('Connecting to bank...')
                print ('Refund done')
        else:
            print ('user is not subscibed...')
            context['user_subscribed'] = False

        return render(request,
                      self.template_name,
                      context)

class QueueToEventView(TemplateView):
    template_name = "TravelsApp/queue_to_event.html"

    #Handles the 'POST' request from the client browser
    def get(self, request, *args, **kwargs):

        print('QueueToEventView.POST')
        context  = super().get_context_data(**kwargs)
        context['event'] = Event.objects.get(id=kwargs['pk'])

        #Is the user queued to this event
        if context['event'].queued_partecipants.filter(username=request.user.username).count()>0 :
            context['user_queued'] = True
        else:
            context['user_queued'] = False

        #Gestire il caso in cui l'utente è già in coda ma chiede di essere accodato nel html


        if kwargs['command'] == 'add_me':
            #add current user to the queue
            context['event'].queued_partecipants.add(request.user)
            context['event'].save()
            context['cmd']  ='add_me'
            print ('user added to queue')


        elif kwargs['command'] == 'remove_me':
            #remove current user to the queue
            context['event'].queued_partecipants.remove(request.user)
            context['event'].save()
            context['cmd']  = 'remove_me'
            print ('user removed from queue')


        return render(request,
                      self.template_name,
                      context)

def get_setting(name):
    r = Setting.objects.get(name=name).value
    return r

def save_setting(name, value, description):
    s = Setting.objects.get_or_create( name=name)[0]
    s.value = value
    s.description = description
    s.save()
