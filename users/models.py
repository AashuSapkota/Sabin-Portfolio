from django.db import models
import datetime


from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    use_in_migrations: True

    def _create_user(self, user_email, user_fullname, password, user_role, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not user_email:
            raise ValueError('The given Id must be set')
        # email = self.normalize_email(email)
        user = self.model(user_email=user_email, user_fullname=user_fullname,
                          password=password, user_role=user_role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, user_email, user_fullname, user_role, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(user_email, password, **extra_fields)

    def create_superuser(self, user_email, user_fullname, password, user_role, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(user_email, user_fullname, password, user_role, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    user_email = models.EmailField(max_length=100, unique=True)
    user_fullname = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    user_role = models.CharField(max_length=255, null=True, blank=True)
    first = models.BooleanField(default=True, null=True)
    created_on = models.DateTimeField(default=datetime.datetime.now())
    created_by = models.CharField(max_length=100, null=False, blank=False)
    last_updated_on = models.DateTimeField(null=True, blank=True)
    last_updated_by = models.CharField(max_length=100, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(null=True, blank=True)
    deleted_by = models.CharField(max_length=100, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'user_email'
    REQUIRED_FIELDS = []
    class Meta:
        ordering = ('user_email',)
        verbose_name = _('user')
        verbose_name_plural = _('users')


class UserRoleModel(models.Model):
    role_name = models.CharField(max_length=100, null=False, blank=False)
    role_description = models.TextField(null=True, blank=True)
    created_by = models.CharField(max_length=100, null=False, blank=False)
    created_on = models.DateTimeField(default=datetime.datetime.now())
    last_updated_on = models.DateTimeField(null=True, blank=True)
    last_updated_by = models.CharField(max_length=100, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(null=True, blank=True)
    deleted_by = models.CharField(max_length=100, null=True, blank=True)


class UserRolePrevilegeModel(models.Model):
    role_id = models.CharField(max_length=100, null=False, blank=False)
    user_id = models.CharField(max_length=100, null=False, blank=False)
    menu_code = models.CharField(max_length=100, null=False, blank=False)
    create_rights = models.BooleanField(null=False, blank=False)
    retrieve_rights = models.BooleanField(null=False, blank=False)
    update_rights = models.BooleanField(null=False, blank=False)
    delete_rights = models.BooleanField(null=False, blank=False)


class MenuListModel(models.Model):
    is_root = models.BooleanField(default=False)
    menu_name = models.CharField(max_length=100, null=False, blank=False)
    menu_link = models.CharField(max_length=500, null=True, blank=True)
    menu_icon = models.CharField(max_length=250, null=True, blank=True)
    is_submenu = models.BooleanField(default=False)
    submenu_name = models.CharField(max_length=100, null=True, blank=True)
    submenu_link = models.CharField(max_length=500, null=True, blank=True)
    submenu_icon = models.CharField(max_length=250, null=True, blank=True)
    
    class Meta:
        ordering = ('id',)


