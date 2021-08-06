from django.urls import path, re_path
from . import views

# SET THE NAMESPACE!
app_name = 'TravelsApp'

# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[
    path('index/',views.index,name='index'),
    path('register/',views.register,name='register'),
    path('my_account/',views.my_account,name='my_account'),
    path('change_password/',views.change_password,name='change_password'),
    path('user_login/',views.user_login,name='user_login'),
    #path('activities/',views.ActivityListView.as_view(), name='activities'),
    path('events/<str:filter_mode>/',views.EventListView.as_view(), name='events'),
    #path("SingleActivity/<int:pk>/",views.SingleEvent.as_view(),name="single"),
    re_path(r'SingleActivity/(?P<pk>[0-9]{1,})/.*',views.SingleEvent.as_view(),name="single"),
    path('buyticket/<int:pk>/<str:buy_step>/<int:total>/<int:credits_to_use>',views.BuyTicketView.as_view(),name="buyticket"),
    path('queue_to_event/<int:pk>/<str:command>',views.QueueToEventView.as_view(),name="queue_to_event"),
    path('ask_refund/<int:pk>/<str:refund_step>',views.AskRefundView.as_view(),name="ask_refund"),
    path('card_pay/<int:amount>/<int:order_id>',views.CardPayView.as_view(),name="card_pay"),
    path('create_payment_intent/',views.create_payment_intent,name="create_payment_intent"),
    path('stripe_webhook/',views.stripe_webhook,name="stripe_webhook"),

]
