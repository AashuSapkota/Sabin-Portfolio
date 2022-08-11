from django.db import models

# Create your models here.
class Channels(models.Model):
    channel_name = models.CharField(max_length=250, null=False, blank=False, unique=True)
    channel_description = models.CharField(max_length=500, null=True, blank=True)
