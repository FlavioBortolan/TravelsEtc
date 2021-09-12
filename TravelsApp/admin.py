from django.contrib import admin
from .models import UserProfileInfo, Activity, Event, Setting, Order, Ticket, OutMail

# Register your models here.
admin.site.register(UserProfileInfo)
admin.site.register(Activity)
admin.site.register(Event)
admin.site.register(Setting)
admin.site.register(Order)
admin.site.register(Ticket)
admin.site.register(OutMail)
