from django.urls import path
from . import views

# SET THE NAMESPACE!
app_name = 'TravelsApp'

# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[
    path('index/',views.index,name='index'),
    path('register/',views.register,name='register'),
    path('my_account/',views.my_account,name='my_account'),
    path('user_login/',views.user_login,name='user_login'),
    #path('activities/',views.ActivityListView.as_view(), name='activities'),
    path('events/<str:filter_mode>/',views.EventListView.as_view(), name='events'),
    path("SingleActivity/<int:pk>/",views.SingleEvent.as_view(),name="single"),
    path('buyticket/<int:pk>/<str:buy_step>',views.BuyTicketView.as_view(),name="buyticket"),

]
