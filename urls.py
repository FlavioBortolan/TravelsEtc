from django.urls import path
from . import views

# SET THE NAMESPACE!
app_name = 'TravelsApp'

# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[
    path('index/',views.register,name='index'),
    path('register/',views.register,name='register'),
    path('user_login/',views.user_login,name='user_login'),
    path('activities/',views.ActivityListView.as_view(), name='activities'),
    path("activities<pk>/",views.SingleActivity.as_view(),name="single"),

]
