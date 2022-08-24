# Generated by Django 3.1.8 on 2021-04-21 04:17

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailforms', '0004_add_verbose_name_plural'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wagtailcore', '0060_fix_workflow_unique_constraint'),
        ('wagtailredirects', '0006_redirect_increase_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('wagtailimages', '0023_add_choose_permissions'),
        ('home', '0009_auto_20210421_1001'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ServicesPage',
            new_name='ServicesList',
        ),
    ]
