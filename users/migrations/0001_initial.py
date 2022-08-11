# Generated by Django 4.1 on 2022-08-10 15:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRoleModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_name', models.CharField(max_length=100)),
                ('role_description', models.TextField(blank=True, null=True)),
                ('created_by', models.CharField(max_length=100)),
                ('created_on', models.DateTimeField(default=datetime.datetime(2022, 8, 10, 20, 45, 49, 119523))),
                ('last_updated_on', models.DateTimeField(blank=True, null=True)),
                ('last_updated_by', models.CharField(blank=True, max_length=100, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_on', models.DateTimeField(blank=True, null=True)),
                ('deleted_by', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('user_email', models.EmailField(max_length=100, unique=True)),
                ('user_fullname', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('user_role', models.CharField(blank=True, max_length=255, null=True)),
                ('first', models.BooleanField(default=True, null=True)),
                ('created_on', models.DateTimeField(default=datetime.datetime(2022, 8, 10, 20, 45, 49, 117527))),
                ('created_by', models.CharField(max_length=100)),
                ('last_updated_on', models.DateTimeField(blank=True, null=True)),
                ('last_updated_by', models.CharField(blank=True, max_length=100, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_on', models.DateTimeField(blank=True, null=True)),
                ('deleted_by', models.CharField(blank=True, max_length=100, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'ordering': ('user_email',),
            },
        ),
    ]
