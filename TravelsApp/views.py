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
        profile_form = UserProfileInfoForm(initial = {'phone_number': request.user.userprofileinfo.phone_number,})

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
                            'data_change_successful':data_change_successful})



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
