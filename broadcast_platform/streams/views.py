from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.db import transaction
from django.contrib import messages
from .models import Streams
from channels.models import Channels
from subscriptions.models import UserSubscriptions
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from users.decorators import only_admin, only_users
from django.utils.decorators import method_decorator
from subscriptions.models import Comments
from users.models import User
from .models import Feedback
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError


@method_decorator(only_admin(), name='dispatch')
class StreamUploadView(LoginRequiredMixin, View):
    template_name = 'streams/stream_upload.html'
    context_object_name = 'stream'

    def get(self, request, *args, **kwargs):
        channels = Channels.objects.all()
        return render(request, self.template_name, {'channels': channels})

    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            stream_name = request.POST['stream_name'].lower()
            stream_file = request.FILES['stream_file']
            stream_channel = request.POST['stream_channel']
            stream_live = request.POST['stream_live']
            print('stream channel: ', stream_channel)
            stream_channel = Channels.objects.get(pk=stream_channel)
            print('stream channel: ', stream_channel)
            stream = Streams(
                stream_name=stream_name, stream_file=stream_file, stream_channel=stream_channel,is_live=stream_live)
            stream.save()

            # get users email list who have subscribed the channel
            subscribed_users_id = UserSubscriptions.objects.filter(
                channel_id=stream_channel)
            users_id = []
            for subscribed_user_id in subscribed_users_id:
                if subscribed_user_id.user_id not in users_id:
                    users_id.append(subscribed_user_id.user_id)
            users = User.objects.filter(pk__in=users_id)
            email_list = []
            for user in users:
                if user.user_email_address not in email_list:
                    email_list.append(user.user_email_address)
            print('email list: ', email_list)
            # mail channel_subscribed users with notification of new stream uploaded in that particluar channel
            subject = 'Stream Uploaded'
            email_template_name = 'streams/stream_uploaded_notification.txt'
            c = {
                'email': email_list,
                'domain': '127.0.0.1:8000',
                'site_name': 'Broadcast',
                'protocol': 'http',
            }
            email = render_to_string(email_template_name, c)
            try:
                send_mail(subject, email, 'your_mail@gmail.com', email_list, fail_silently=False)
            except Exception as e:
                print(e)
            print('saved')
            messages.success(request, "Stream Uploaded Succesfully!!")
            messages.success(request, "Subscribed Users Mailed With Notification!!")
            return redirect('streams:stream_list')


@login_required(redirect_field_name='login')
@only_admin()
def StreamListView(request):
    context = {}
    streams = Streams.objects.all()
    context['streams'] = streams
    template_name = 'streams/stream_list.html'
    if request.method == 'POST' and request.is_ajax():
        ID = request.POST.get('id')
        stream = streams.get(id=ID)
        stream_id = stream.pk
        stream_name = stream.stream_name
        context['stream'] = stream
        context['stream_id'] = stream_id
        context['stream_name'] = stream_name
    return render(request, template_name, context)


@method_decorator(only_admin(), name='dispatch')
class StreamUpdateView(LoginRequiredMixin, View):
    template_name = 'streams/stream_update.html'

    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        try:
            stream = Streams.objects.get(pk=pk)
            channels = Channels.objects.all()
            context = {'stream': stream, 'channels': channels}
            return render(request, self.template_name, context)
        except Streams.DoesNotExist:
            messages.error(request, "Stream Doesn't Exists!!")
            return redirect('streams:stream_list')

    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        stream_name = request.POST['stream_name'].lower()
        print('before')
        stream_file = request.FILES['stream_file']
        print('after')
        print('stream_file:', stream_file)
        stream_channel = request.POST['stream_channel']
        stream_channel = Channels.objects.get(pk=stream_channel)
        stream_live = request.POST['stream_live']
        try:
            stream = Streams.objects.get(pk=pk)
            with transaction.atomic():
                stream.stream_name = stream_name
                stream.stream_file = stream_file
                stream.stream_channel = stream_channel
                stream.is_live = stream_live
                stream.save()
                messages.success(request, "Stream Updated Succesfully!!")
                return redirect('streams:stream_list')
        except:
            messages.error(
                request, "Something Wen't Wrong! Please Try Again!!")


@login_required(redirect_field_name='login')
@only_admin()
def StreamDeleteView(request, pk):
    try:
        stream = Streams.objects.get(pk=pk)
        stream.delete()
        messages.success(request, "Stream Deleted Succesfully!!")
        return redirect('streams:stream_list')
    except Streams.DoesNotExist:
        messages.error(request, "Stream Doesn't Exists!!")
        return redirect('streams:stream_list')


class StreamingNowList(LoginRequiredMixin, View):
    template_name = 'streams/streaming_now.html'

    def get(self, request, *args, **kwargs):
        subscribed_channels = UserSubscriptions.objects.filter(
            user_id=request.user.pk)
        subscribed_channel_list = []
        for subscribed_channel in subscribed_channels:
            subscribed_channel_list.append(subscribed_channel.channel.pk)
        print('Subscribed Channel List: ', subscribed_channel_list)
        subscribed_streams = Streams.objects.filter(
            stream_channel__in=subscribed_channel_list).filter(is_live=False)
        print('Subscribed Stream List: ', subscribed_streams)
        context = {'streams': subscribed_streams}
        return render(request, self.template_name, context)


class StreamingLiveList(LoginRequiredMixin, View):
    template_name = 'streams/streaming_live.html'

    def get(self, request, *args, **kwargs):
        subscribed_channels = UserSubscriptions.objects.filter(
            user_id=request.user.pk)
        subscribed_channel_list = []
        for subscribed_channel in subscribed_channels:
            subscribed_channel_list.append(subscribed_channel.channel.pk)
        print('Subscribed Channel List: ', subscribed_channel_list)
        subscribed_streams = Streams.objects.filter(
            stream_channel__in=subscribed_channel_list).filter(is_live=True)
        print('Subscribed Stream List: ', subscribed_streams)
        context = {'streams': subscribed_streams}
        return render(request, self.template_name, context)


class StreamItem(LoginRequiredMixin, View):
    template_name = 'streams/stream_item.html'

    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        comments = Comments.objects.filter(stream_id=pk)
        stream = Streams.objects.get(pk=pk)
        return render(request, self.template_name, {'stream': stream, 'comments': comments})


def CreateComment(request):
    if request.method == 'GET':
        print('in get')
    if request.method == 'POST':
        try:
            print('in post')
            stream_id = request.POST['stream_id']
            user_id = request.user.pk
            comment = request.POST['comment']
            print('stream_id:', stream_id)
            print('user_id:', user_id)
            print('comment:', comment)
            stream = Streams.objects.get(pk=stream_id)
            logged_user = User.objects.get(pk=user_id)
            print('stream:', stream)
            print('logged_user:', logged_user)
            comment = Comments(user_id=logged_user,
                               stream_id=stream, comment=comment)
            comment.save()
            messages.success(request, "Comment Added Succesfully!!")
            return redirect('streams:stream_item', pk=stream_id)
        except:
            messages.error(request, "Something Went Wrong!!")
            return redirect('streams:stream_item', pk=stream_id)


@method_decorator(only_admin(), name='dispatch')
class CommentList(View):
    template_name = 'streams/comments_list.html'

    def get(self, request, *args, **kwargs):
        comments = Comments.objects.filter(blacklisted=False)
        context = {'comments': comments}
        return render(request, self.template_name, context)


@only_admin()
def BlackListComment(request):
    if request.method == 'POST':
        print('in post')
        try:
            comment_id = request.POST.get('comment_id')
            print('comment is:', comment_id)
            comment = Comments.objects.get(pk=comment_id)
            comment.blacklisted = True
            comment.save()
            messages.success(request, "Comment BlackListed Succesfully!!")
            return redirect('streams:comment_list')
        except:
            messages.error(request, "Something Went Wrong!!")
            return redirect('streams:comment_list')


def CheersStream(request):
    if request.method == 'POST':
        try:
            stream_id = request.POST.get('stream_id')
            stream = Streams.objects.get(pk=stream_id)
            stream.stream_cheers += 1
            stream.save()
            messages.success(request, "You cheered the stream!!")
            return redirect('streams:stream_item', pk=stream_id)
        except:
            messages.error(request, "Something Went Wrong!!")
            return redirect('streams:stream_item', pk=stream_id)


class CreateFeedback(View):
    def post(self, request, *args, **kwargs):
        try:
            pk = kwargs['pk']
            stream = Streams.objects.get(pk=pk)
            user_id = request.user.pk
            user = User.objects.get(pk=user_id)
            print('user:', user)
            feedback_text = request.POST.get('feedback')
            feedback = Feedback(
                user_id=user, stream_id=stream, feedback=feedback_text)
            feedback.save()
            messages.success(request, "Feedback added succesfully!!")
            return redirect('streams:stream_item', pk=pk)
        except Exception as e:
            print('error:', e)
            messages.error(
                request, "Something Wen't Wrong. Please Try Again!!")
            return redirect('streams:stream_item', pk=pk)


@method_decorator(only_admin(), name='dispatch')
class ListFeedback(View):
    template_name = 'streams/feedbacks_list.html'

    def get(self, request, *args, **kwargs):
        feedbacks = Feedback.objects.all()
        context = {'feedbacks': feedbacks}
        return render(request, self.template_name, context)
