from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.db import transaction
from .models import Channels
from django.contrib import messages
from subscriptions.models import UserSubscriptions
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from users.decorators import only_admin
from django.utils.decorators import method_decorator


@method_decorator(only_admin(), name='dispatch')
class ChannelCreateView(LoginRequiredMixin, View):
    template_name = 'channels/channel_create.html'
    context_object_name = 'channel'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            channel_name = request.POST['channel_name'].lower()
            channel_description = request.POST['channel_description'].lower()
            channel = Channels(channel_name=channel_name, channel_description=channel_description)
            channel.save()
            messages.success(request, 'Channel Created Succesfully!!')
            return redirect('channels:channel_list')


@login_required(redirect_field_name='login')
def ChannelListView(request):
    context = {}
    if request.user.is_admin == True:
        channels = Channels.objects.all()
    elif request.user.is_admin == False:
        # channels = Channels.objects.all()
        subscribed_channels = UserSubscriptions.objects.filter(user_id=request.user.pk)
        subscribed_channel_list = []
        for subscribed_channel in subscribed_channels:
            subscribed_channel_list.append(subscribed_channel.channel.pk)
        channels = Channels.objects.all().exclude(pk__in=subscribed_channel_list)
    context['channels']=channels
    template_name = 'channels/channels_list.html'
    if request.method == 'POST' and request.is_ajax():
        ID = request.POST.get('id')
        channel = channels.get(id=ID)
        channel_id = channel.pk 
        channel_name = channel.channel_name
        context['channel'] = channel
        context['channel_id'] = channel_id
        context['channel_name'] = channel_name
    return render(request, template_name, context)


@login_required(redirect_field_name='login')
def SubscribedChannelList(request):
    context = {}
    template_name = 'channels/subscribed_channels_list.html'
    subscribed_channels = UserSubscriptions.objects.filter(user_id=request.user.pk)
    subscribed_channel_list = []
    for subscribed_channel in subscribed_channels:
        subscribed_channel_list.append(subscribed_channel.channel.pk)
    channels = Channels.objects.filter(pk__in=subscribed_channel_list)
    context['channels']=channels
    return render(request, template_name, context)


@method_decorator(only_admin(), name='dispatch')
class ChannelUpdateView(LoginRequiredMixin, View):
    template_name = 'channels/channel_update.html'
    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        try:
            channel = Channels.objects.get(pk=pk)
            return render(request, self.template_name, {'channel':channel})
        except Channels.DoesNotExist:
            messages.error(request, "Channel Doesn't Exists!!")
            return redirect('channels:channel_list')
    
    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        channel_name = request.POST['channel_name'].lower()
        print('channel_name:', channel_name)
        channel_description = request.POST['channel_description'].lower()
        print('channel_description: ', channel_description)
        try:
            channel = Channels.objects.get(pk=pk)
            with transaction.atomic():
                channel.channel_name = channel_name
                channel.channel_description = channel_description
                channel.save()
                print('updated description: ', channel.channel_description)
                messages.success(request, 'Channel Updated Succesfully!!')
                return redirect('channels:channel_list')
        except:
            messages.error(request, "Something Went Wrong! Please Try Again!!")
        

@login_required(redirect_field_name='login')
@only_admin()
def ChannelDeteleView(request, pk):
    try:
        channel = Channels.objects.get(pk=pk)
        channel.delete()
        messages.success(request, 'Channel Deleted Succesfully!!')
        return redirect('channels:channel_list')
    except Channels.DoesNotExist:
        messages.error(request, "Channel Doesn't Exists!!")
        return redirect('channels:channel_list')
