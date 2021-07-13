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

from django.contrib.auth import get_user_model
from datetime import date
import time

User = get_user_model()

import logging
logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
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

        # Check to see both forms are valid
        if user_form.is_valid() and profile_form.is_valid():

            # Save User Form to Database
            user = user_form.save()

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

            # Now save model
            profile.save()

            # Registration Successful!
            registered = True

            user = authenticate(username=user_form.cleaned_data['username'],
                                password=user_form.cleaned_data['password'],
                                )
            login(request, user)

        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors,profile_form.errors)
    #GET
    else:
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

def user_login(request):

    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

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
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        #Nothing has been provided for username or password.
        return render(request, 'TravelsApp/login.html', {})

#class ActivityListView(LoginRequiredMixin, ListView):

    #login_url = '/login/'
#    redirect_field_name = 'activities'

    #model = Activity

    #def get_queryset(self):
    #    return Activity.objects.order_by('date')


class EventListView(LoginRequiredMixin, ListView):

    login_url = '/login/'
    redirect_field_name = 'events'
    template_name = 'TravelsApp/event_list.html'
    model = Event

    #defines the set of elments to be shown (GET)
    #note: *args    = positional arguments in the url call
    #      **kwargs = name-based arguments in the url call
    def get_queryset(self,*args, **kwargs):

        if self.kwargs['filter_mode']=='current_user':
            logger.error('filter_mode:' + self.kwargs['filter_mode'] + ', verranno mostrate solo le attivita dell utente attuale')
            return(self.request.user.event_set.all())

        elif self.kwargs['filter_mode']=='all':
            logger.error('filter_mode:' + self.kwargs['filter_mode'] + ', verranno mostrate tutte le attivita')
            return(Event.objects.all())

    #defines the context dictionary to be used to render page during GET
    def get_context_data(self, **kwargs):
        context  = super().get_context_data(**kwargs)
        context['filter_mode'] = self.kwargs['filter_mode']
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

        #Log filter values for debug purposes
        logger.error('POST data:')
        logger.error('City:' + city)
        logger.error('StartDate:' + str(start_date))
        logger.error('EndDate:' + str(end_date))

        #Retrive the events filtered by selected criteria
        filtered_events = Event.objects.filter(activity__place__iexact = city,
                                               dateTime__gte = start_date,
                                               dateTime__lte = end_date,
                                               activity__type__iexact = type )

        #renders the page with the context dictionary elements set to the values
        #previously calculated
        return render(request,
                      self.template_name,
                      {'event_list': filtered_events,
                       'filter_mode':'apply_filter',
                       'city': city,
                       'start_date': time.strftime("%Y-%M-%d", time.strptime(start_date, '%Y-%M-%d')),
                       'end_date': end_date,
                       'type': type

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
            context['user_already_has_this_ticket'] = 'true'
            logger.error('The user already has this ticket')
        else:
            context['user_already_has_this_ticket'] = 'false'
            logger.error('The user does not have this ticket')

        #inject the name of the image of the event
        context['event_image_name'] = 'Images/' + Event.objects.filter(id=self.kwargs['pk'])[0].activity.name + '.jpg'

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
