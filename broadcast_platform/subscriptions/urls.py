from django.urls import path
from . import views

app_name = 'subscriptions'

urlpatterns = [
    path('subscribe/', views.SubscribeChannelView.as_view(), name='channel_subscribe'),
    path('unsubscribe/', views.UnSubscribeChannelView.as_view(), name='channel_unsubscribe'),
    path('subscribed/users/', views.SubscribedUsersList, name='subscribed_users_list'),
]