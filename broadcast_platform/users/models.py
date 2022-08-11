from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.hashers import make_password

class UserManager(BaseUserManager):
    use_inmigrations = True

    def _create_user(self, user_fullname, user_username, user_address, user_contact_number, user_email_address, password, **extra_fields):
        pass
        if not user_username:
            raise ValueError('The given ID must be set')
        user = self.model(user_fullname= user_fullname, user_username=user_username, 
                            user_address=user_address, user_contact_number=user_contact_number,
                             user_email_address=user_email_address, password=password,
                             **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, user_fullname, user_username, user_address, user_contact_number, user_email_address, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
    
    def create_superuser(self, user_fullname, user_username, user_address, user_contact_number, user_email_address, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self._create_user(self, user_fullname, user_username, user_address, user_contact_number, user_email_address, password, **extra_fields)



class CountryList(models.Model):
    country_name = models.CharField(null=False, blank=False, max_length=100)
    country_code = models.CharField(null=False, blank=False, max_length=4)

class User(AbstractBaseUser, PermissionsMixin):
    user_fullname = models.CharField(max_length=100, null=False, blank=False)
    user_username = models.CharField(max_length=50, null=False, blank=False, unique=True)
    user_country = models.ForeignKey(CountryList, null=False, blank=False, on_delete=models.CASCADE)
    user_address = models.CharField(max_length=250, null=False, blank=False)
    user_contact_number = models.CharField(max_length=15, null=False, blank=False, unique=True)
    user_email_address = models.EmailField(null=False, blank=False)
    password = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False, null=False, blank=False)
    is_blocked = models.BooleanField(default=False, null=False, blank=False)

    objects = UserManager()

    USERNAME_FIELD = 'user_username'
    REQUIRED_FIELDS = []

    # def save(self, *args, **kwargs):
    #     print('save password')
    #     password = make_password(self.password)
    #     # password = self.password
    #     print(password)
    #     self.password = password
    #     super().save(*args, **kwargs)

