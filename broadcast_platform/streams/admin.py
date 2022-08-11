from django.contrib import admin
from .models import Streams


class StreamAdmin(admin.ModelAdmin):
    admin.site.register(Streams)