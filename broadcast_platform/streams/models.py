from django.db import models
from django.db.models.deletion import CASCADE
from channels.models import Channels
from users.models import User


class Streams(models.Model):
    stream_name = models.CharField(max_length=50, null=False, blank=False, unique=True)
    stream_file = models.FileField(upload_to='stream', null=False, blank=False)
    stream_channel = models.ForeignKey(Channels, null=False, blank=False, on_delete=models.CASCADE)
    stream_cheers = models.IntegerField(default=0, null=False, blank=False)
    is_live = models.BooleanField(default=False, null=False, blank=False)

    def __str__(self):
        return self.stream_name


class Feedback(models.Model):
    stream_id = models.ForeignKey(Streams, null=False, blank=False, on_delete=CASCADE)
    user_id = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    feedback = models.TextField(null=False, blank=False)