from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import RegexValidator

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
    credits = models.PositiveIntegerField(default=10)
    exp_date = models.DateField(default = timezone.now)

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
    description = models.CharField(max_length=600)
    place = models.CharField(max_length=100)
    #partecipants
    type = models.CharField(max_length=100)
    price = models.PositiveIntegerField(default = 15)
    #confirmed
    duration = models.FloatField(default = 3.5)
    activityDetail = models.CharField(max_length=600, default="Andremo su per la collina e poi giu per la collina")
    difficultyLevel = models.CharField(max_length=8, default="E")
    length = models.FloatField(default=4)
    gradient = models.FloatField(default=300)
    streetType = models.CharField(max_length=600, default="Sterrato e asfalto")
    dogsAllowed = models.BooleanField(default=0)
    kidsAllowed = models.BooleanField(default=0)
    meetPlaceLink = models.CharField(max_length=600, default = "https://www.google.com/maps/place/45%C2%B050'14.3%22N+11%C2%B044'11.2%22E/@45.8373125,11.7342488,17z/data=!3m1!4b1!4m5!3m4!1s0x0:0x0!8m2!3d45.8373125!4d11.7364375" )
    meetPlaceDirections = models.CharField(max_length=600, default ="Verso Marostica ")
    leader = models.CharField(max_length=64)
    whatToBring = models.CharField(max_length=600, default = "Pranzo al sacco, acqua, crema solare, scarpe da trekking")
    minNumPartecipants = models.PositiveIntegerField(default=10)
    maxNumPartecipants = models.PositiveIntegerField(default=20)

    def __str__(self):
    # Built-in attribute of django.contrib.auth.models.User !
        return "ID: " + str(self.id) + ", Place: " + self.place + ", Leader: " + self.leader

class Order(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default = timezone.now)
    time = models.TimeField(default = timezone.now)
    status = models.CharField(max_length=24, default="chart")
    items = models.CharField(max_length=600, default="")
    total = models.PositiveIntegerField(default=0)
    credits_to_use = models.PositiveIntegerField(default=0)
    payment_id = models.CharField(max_length=200, default="xxx")

    def __str__(self):
    # Built-in attribute of django.contrib.auth.models.User !
        return "ID: " + str(self.id) + ", Total: " + str(self.total) + ", credits_to_use: " + str(self.credits_to_use) + ", items: " + str(self.items)

class Event(models.Model):

    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    date = models.DateField(default = timezone.now)
    time = models.TimeField(default = timezone.now)
    partecipants = models.ManyToManyField(User)
    queued_partecipants = models.ManyToManyField(User, related_name='my_queued_events')
    confirmed = models.BooleanField(default=0)

    def __str__(self):
        return "ID: " + str(self.id) + ", Date: " + str(self.date) + str(self.activity)

class Ticket(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

class Setting(models.Model):

    name  = models.CharField(max_length=128)
    value = models.CharField(max_length=128)
    description = models.CharField(max_length=128)

    def __str__(self):
        return "name: " + str(self.name) + ", value: " + str(self.value)
