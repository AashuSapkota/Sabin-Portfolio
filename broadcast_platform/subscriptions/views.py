from django.conf import urls
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import UserSubscriptions
from users.models import User
from channels.models import Channels
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from streams.models import Streams
from .models import Comments
from django.http import HttpResponseRedirect, request


class SubscribeChannelView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        print('---------POST----------')
        channel_id = request.POST.get('id')
        print('Channel_id:', channel_id)
        user_id = request.user.pk
        print('user_id:', user_id)
        try:
            channel = Channels.objects.get(pk=channel_id)
            logged_in_user = User.objects.get(pk=user_id)
            print('channel:', channel)
            print('user:', logged_in_user)
            subscription = UserSubscriptions.objects.create(user= logged_in_user, channel=channel)
            subscription.save()
            messages.success(request, "Channel Subscribed Succesfully!!")
            return redirect('channels:channel_list')
        except :
            messages.error(request, "Something Went Wrong!!")
            return redirect('channels:channel_list')



class UnSubscribeChannelView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            channel_id = request.POST.get('id')
            print('Channel_id:', channel_id)
            user_id = request.user.pk
            print('user_id:', user_id)
            subscription = UserSubscriptions.objects.filter(user=user_id).filter(channel=channel_id).first()
            print('Subscription:', subscription)
            subscription.delete()
            messages.success(request, "Channel UnSubscribed Succesfully!!")
            return redirect('channels:channel_list')
        except :
            messages.error(request, "Something Went Wrong!!")
            return redirect('channels:channel_list')


@login_required(redirect_field_name='login')
def SubscribedUsersList(request):
    template_name = 'subscriptions/subscribed_users.html'
    context = {}
    if request.method == 'GET':
        subscriptions = UserSubscriptions.objects.all()
        users = []
        for subscription in subscriptions:
            user = subscription.user
            if user not in users:
                users.append(user)
            context['users'] = users
            # print('user:', user)
            # usr_subs = UserSubscriptions.objects.select_related().filter(user=user)
            # print('urs_subs: ', usr_subs)
            # context['user'] = user
            # context['usr_subs'] = usr_subs
        # context['subscriptions'] = subscriptions

        # usr_subs = UserSubscriptions.objects.filter(user=3)
        
        # context['usr_subs'] =usr_subs 
        
        return render(request, template_name, context)







