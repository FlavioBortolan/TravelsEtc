from django import forms
import django.contrib.auth.password_validation as pw
from django.contrib.auth.models import User
from .models import UserProfileInfo
from django.forms.utils import ErrorList

class DivErrorList(ErrorList):

    def __str__(self):
     return self.as_divs()

    def as_divs(self):
        if not self: return ''
        return '<div class="errorlist">%s</div>' % ''.join(['<div class="w3-red">%s</div>' % e for e in self])

class UserForm(forms.ModelForm):

    #username        = forms.CharField(widget=forms.TextInput(attrs={'class': "w3-input"}))
    #password        = forms.CharField(widget=forms.PasswordInput(attrs={'class': "w3-input"}))
    repeat_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': "w3-input"}))
    #email           = forms.CharField(widget=forms.EmailInput(attrs={'class': "w3-input"}))

    def clean_password(self):
        p = self.cleaned_data.get('password')
        pw.validate_password(p)
        return p

    def clean_repeat_password(self):
        p1 = self.cleaned_data.get('password')
        p2 = self.cleaned_data.get('repeat_password')

        if not p2:
            raise forms.ValidationError("You must confirm your password")
        if p1 != p2:
            raise forms.ValidationError("Your passwords do not match")
        return p2

    def clean_email(self):
        #get the email supplied trough the form
        supplied_email = self.cleaned_data['email']

        #check if someone else in the database used that email
        duplicate_users = User.objects.filter(email__iexact = supplied_email).count()

        if duplicate_users != 0:
            raise forms.ValidationError("This email is already in use.")
        return supplied_email

    class Meta():
        model = User
        #fields = ('username','email','password')
        fields = ('first_name', 'last_name', 'email','password')
        widgets = {

            'first_name':       forms.TextInput(attrs={'class': "w3-input", 'required':'True'}),
            'last_name':        forms.TextInput(attrs={'class': "w3-input", 'required':'True'}),
            'password':         forms.PasswordInput(attrs={'class': "w3-input"}),
            'email':            forms.EmailInput(attrs={'class': "w3-input"}),
        }

class UserProfileInfoForm(forms.ModelForm):

    #subscription_exp_date = forms.CharField(widget=forms.DateInput(attrs={'name': 'subscription_exp_date', 'class': "w3-input", 'disabled':'True'}))
    class Meta():

        model = UserProfileInfo
        fields = ('profile_pic', 'phone_number', 'subscription_exp_date' )
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': "w3-input", 'required':'True'}),
            'subscription_exp_date': forms.DateInput(attrs={'name': 'gino', 'class': "w3-input", 'disabled':'True'}),
            'profile_pic': forms.ClearableFileInput(attrs={'class': "w3-btn w3-blue w3-center", 'label':'ggg'}),
        }
