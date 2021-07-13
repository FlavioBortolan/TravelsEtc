from django.contrib import admin
from .models import UserProfileInfo, Activity, Event

# Register your models here.
admin.site.register(UserProfileInfo)
admin.site.register(Activity)
admin.site.register(Event)
