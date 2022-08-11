from django.urls import path
from . import views

app_name = 'channels'

urlpatterns = [
    path('create/', views.ChannelCreateView.as_view(), name='channel_create'),
    path('list/', views.ChannelListView, name='channel_list'),
    path('update/<int:pk>/', views.ChannelUpdateView.as_view(), name='channel_update'),
    path('delete/<int:pk>/', views.ChannelDeteleView, name='channel_delete'),


    path('subscribed/list/', views.SubscribedChannelList, name='subscribed_channel_list'),
]