from django.contrib import admin
from .models import Channels

class ChannelAdmin(admin.ModelAdmin):
    admin.site.register(Channels)
