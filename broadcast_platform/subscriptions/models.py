from datetime import datetime
from django.db import models
from django.db.models.base import Model
from channels.models import Channels
from users.models import User
from streams.models import Streams


class UserSubscriptions(models.Model):
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channels, null=False, blank=False, on_delete=models.CASCADE)



class Comments(models.Model):
    user_id = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    stream_id = models.ForeignKey(Streams, null=False, on_delete=models.CASCADE)
    comment = models.TextField(null=False, blank=False)
    blacklisted = models.BooleanField(default=False)
    date = models.DateTimeField(default=datetime.now, null=False, blank=False)

