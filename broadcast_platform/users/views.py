from django.conf.urls import url
from django.http.response import BadHeaderError, HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from users.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from django.contrib import messages
from django.views.generic.list import ListView
from django.contrib.auth.hashers import make_password, check_password
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .decorators import only_admin
from django.utils.decorators import method_decorator
from broadcast_platform.settings import EMAIL_HOST_USER
from .load_country_data import load_data
from .models import CountryList

class UserLoginView(View):
    def get(self, request, *args, **kwargs):
        print('Get Method')

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        try:
            usr = User.objects.get(user_username=username)
            user = authenticate(request, user_username=username,
                                password=password)
            if user is None:
                messages.error(request, "Incorrect Password")
                return redirect('login')
            elif user is not None:
                login(request, user)
                return redirect('/')
        except User.DoesNotExist:
            messages.error(request, "Incorrect Username")
            return redirect('login')


class UserLogout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('/accounts/login/')


class UserRegisterView(View):
    template_name = 'users/users_register.html'
    context_object_name = 'user'

    def get(self, request, *args, **kwargs):
        countries = CountryList.objects.all()
        return render(request, self.template_name, {'countries':countries})

    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            user_fullname = request.POST['full_name'].lower()
            user_username = request.POST['username'].lower()
            user_address = request.POST['address'].lower()
            user_contact_number = request.POST['contact_number']
            user_email_address = request.POST['email_address']
            user_country = request.POST['user_country']
            password = request.POST['password']
            password = make_password(password)
            country = CountryList.objects.get(pk=user_country)

            user = User(user_fullname=user_fullname, user_username=user_username, user_address=user_address,
                        user_contact_number=user_contact_number, user_email_address=user_email_address, 
                        user_country=country, password=password)
            user.save()
            messages.success(request, 'User Account Created')
            return redirect('/accounts/login/')


@login_required(redirect_field_name='login')
@only_admin()
def UserListView(request):
    context = {}
    users = User.objects.filter(is_admin=False).filter(is_blocked=False)
    if request.method == 'POST' and request.is_ajax():
        print('inside post')
        ID = request.POST.get('id')
        user = users.get(id=ID)
        user_id = user.pk
        user_name = user.user_fullname
        context['user'] = user
        context['user_id'] = user_id
        context['user_name'] = user_name
    context['users'] = users
    template_name = 'users/users_list.html'
    return render(request, template_name, context)



class UserUpdateView(LoginRequiredMixin, View):
    template_name = 'users/users_update.html'
    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        try:
            user = User.objects.get(pk=pk)
            countries = CountryList.objects.all()
            print('countries:', countries)
            return render(request, self.template_name, {'user':user, 'countries':countries})
        except User.DoesNotExist:
            messages.error(request, "User Doesn't Exists !!")
            return redirect('users:user_list')
    
    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        user_fullname = request.POST['full_name'].lower()
        user_username = request.POST['username'].lower()
        user_address = request.POST['address'].lower()
        user_contact_number = request.POST['contact_number']
        user_email_address = request.POST['email_address']
        user_country = request.POST['user_country']
        country = CountryList.objects.get(pk=user_country)
        try:
            user = User.objects.get(pk=pk)
            with transaction.atomic():
                user.user_fullname = user_fullname
                user.user_username = user_username
                user.user_address = user_address
                user.user_contact_number = user_contact_number
                user.user_email_address = user_email_address
                user.user_country = country
                user.save()
                return redirect('users:user_list')
        except:
            messages.error(request, "Something Wen't Wrong! Please Try Again!!")
            return redirect('users:user_list')


@login_required(redirect_field_name='login')
@only_admin()
def UserDeleteView(request, pk):
    try:
        user = User.objects.get(id=pk)
        user.delete()
        messages.success(request, "User Deleted Succesfully!!")
        return redirect('users:user_list')
    except User.DoesNotExist:
        messages.error(request, "User Doesn't Exists!!")
        return redirect('users:user_list')



class UserDetailView(LoginRequiredMixin, View):
    template_name = 'users/users_profile.html'
    def get(self, request, *args, **kwargs):
        countries = CountryList.objects.all()
        pk = kwargs['pk']
        user = User.objects.get(pk=pk)
        return render(request, self.template_name, {'user':user, 'countries':countries})


@login_required(redirect_field_name='login')
@only_admin()
def AdminListView(request):
    context = {}
    users = User.objects.filter(is_admin=True)
    if request.method == 'POST' and request.is_ajax():
        print('inside post')
        ID = request.POST.get('id')
        user = users.get(id=ID)
        user_id = user.pk
        user_name = user.user_fullname
        context['user'] = user
        context['user_id'] = user_id
        context['user_name'] = user_name
    context['users'] = users
    template_name = 'users/admins_list.html'
    return render(request, template_name, context)



@method_decorator(only_admin(), name='dispatch')
class AdminCreateView(LoginRequiredMixin, View):
    template_name = 'users/admin_create.html'
    context_object_name = 'user'

    def get(self, request, *args, **kwargs):
        coutries = CountryList.objects.all()
        return render(request, self.template_name, {'countries':coutries})

    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            user_fullname = request.POST['full_name'].lower()
            user_username = request.POST['username'].lower()
            user_address = request.POST['address'].lower()
            user_contact_number = request.POST['contact_number']
            user_email_address = request.POST['email_address']
            user_country = request.POST['user_country']
            password = request.POST['password']
            password = make_password(password)
            country = CountryList.objects.get(pk=user_country)

            user = User(user_fullname=user_fullname, user_username=user_username, user_address=user_address,
                        user_contact_number=user_contact_number, user_email_address=user_email_address,
                        password=password, user_country=country, is_admin = True)
            user.save()
            messages.success(request, 'User Account Created')
            return redirect('users:admin_list')



@method_decorator(only_admin(), name='dispatch')
class AdminUpdateView(LoginRequiredMixin, View):
    template_name = 'users/admin_update.html'
    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        try:
            user = User.objects.get(pk=pk)
            countries = CountryList.objects.all()
            return render(request, self.template_name, {'user':user, 'countries':countries})
        except User.DoesNotExist:
            messages.error(request, "Admin Doesn't Exists !!")
            return redirect('users:admin_list')
    
    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        user_fullname = request.POST['full_name'].lower()
        user_username = request.POST['user_name'].lower()
        user_address = request.POST['address'].lower()
        user_contact_number = request.POST['contact_number']
        user_email_address = request.POST['email_address']
        user_country = request.POST['user_country']
        country = CountryList.objects.get(pk=user_country)
        try:
            user = User.objects.get(pk=pk)
            with transaction.atomic():
                user.user_fullname = user_fullname
                user.user_username = user_username
                user.user_address = user_address
                user.user_contact_number = user_contact_number
                user.user_email_address = user_email_address
                user.user_country = country
                user.save()
                return redirect('users:admin_list')
        except:
            messages.error(request, "Something Wen't Wrong! Please Try Again!!")
            return redirect('users:admin_list')



class ChangePasswordView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        user = User.objects.get(id=pk)
        old_password = request.POST['old_password']
        verify_password = check_password(old_password, user.password)
        new_password = request.POST['new_password']
        new_password = make_password(new_password)
        if verify_password == True:
            user.password = new_password
            user.save()
            logout(request)
            return redirect('login')
        else:
            messages.error(request, "Current Password Doesn't Match !!")
            return redirect('users:user_detail', pk=pk)


def password_reset_request(request):
    if request.method == 'POST':
        email_address = request.POST['email_address']
        associated_user = User.objects.filter(user_email_address = email_address)
        if associated_user.exists:
            for user in associated_user:
                subject = 'Password Reset Request'
                email_template_name = 'registration/password_reset_email.txt'
                c = {
                    'email': user.user_email_address,
                    'domain': 'http://localhost:8095/',
                    'site_name': 'Broadcast',
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                }

                email = render_to_string(email_template_name, c)
                try:
                    # for smtp.EmailBackend
                    send_mail(subject, email, EMAIL_HOST_USER, [user.user_email_address], fail_silently=False)
                    # for console.EmailBackend
                    # send_mail(subject, email, 'your_mail@gmail.com', [user.user_email_address], fail_silently=False)
                    messages.success(request, "Please check your mail and follow instructions.")
                    return redirect('login')
                except BadHeaderError:
                    messages.error(request, "Something Wen't Wrong. Please Try Again!!")
                    return redirect('login')


def password_reset(request):
    if request.method == 'POST':
        try:
            url_string = request.POST['url_string']
            uid = url_string[33:35]
            uid_decoded = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=uid_decoded)
            password = request.POST['password']
            password_hashed = make_password(password)
            user.password = password_hashed
            user.save()
            logout(request)
            messages.success(request, 'Password Reset: Succesfull. Please Login!!')
            return redirect('login')
        except:
            messages.error(request, "Something Wen't Wrong. Please Try Again!!")
            return redirect('login')


@method_decorator(only_admin(), name='dispatch')
class BlockUser(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            pk=kwargs['pk']
            user = User.objects.get(pk=pk)
            user.is_blocked = True
            user.save()
            messages.success(request, "User Blocked Succesfully!!")
            return redirect('users:list')
        except:
            messages.error(request,'Something Went Wrong!!')
            return redirect('users:list')

@method_decorator(only_admin(), name='dispatch')
class UnBlockUser(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            print('here in post')
            pk=kwargs['pk']
            user = User.objects.get(pk=pk)
            user.is_blocked = False
            user.save()
            messages.success(request, "User UnBlocked Succesfully!!")
            return redirect('users:blocked_user_list')
        except:
            messages.error(request,'Something Went Wrong!!')
            return redirect('users:blocked_user_list')


@method_decorator(only_admin(), name='dispatch')
class BlockedUsersList(LoginRequiredMixin, View):
    template_name = 'users/blocked_users.html'
    def get(self, request, *args, **kwargs):
        users = User.objects.filter(is_admin=False).filter(is_blocked=True)
        context = {'users':users}
        return render(request, self.template_name, context)



class ContactAdmin(LoginRequiredMixin, View):
    template_name = 'users/contact_admin.html'
    def get(self, request, *args, **kwargs):
        print('inget')
        print('hello from get')
        return render(request, self.template_name)
    def post(self, request, *args, **kwargs):
        print('inpost')
        user_name = request.POST.get('name')
        user_email = request.POST.get('email')
        email_subject = request.POST.get('subject')
        email_message = request.POST.get('message')
        print('user_name: ', user_name)
        print('user_email: ', user_email)
        print('email_subject: ', email_subject)
        print('email_message: ', email_message)
        subject = 'Password Reset Request'
        email_template_name = 'users/user_contact_admin.txt'
        c = {
            'email': user_email,
            'domain': '127.0.0.1:8000',
            'site_name': 'Broadcast',
            'user_name': user_name,
            'email_subject': email_subject,
            'email_message': email_message,
            'protocol': 'http',
        }
        email = render_to_string(email_template_name, c)
        try:
            # for smtp.EmailBackend
            # send_mail(subject, email, EMAIL_HOST_USER, [user.user_email_address], fail_silently=False)
            # for console.EmailBackend
            send_mail(subject, email, 'your_mail@gmail.com', [user_email], fail_silently=False)
            messages.success(request, "Your message has been registered. You will be contacted via mail shortly!!")
            return redirect('users:contact_admin')
        except Exception as e:
            print(e)
            messages.error(request, "Something Wen't Wrong. Please Try Again!!")
            return redirect('users:contact_admin')


# class CountryData(View):
#     def get(self, request, *args, **kwargs):
#         print('inside post')
#         load_data()
#     def get(self, request, *args, **kwargs):
#         print('inside post')
#         load_data()