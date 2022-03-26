from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from autoslug import AutoSlugField
# Create your models here.


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    room_name = models.TextField(null=True)
    date = models.DateTimeField(
        default=timezone.now)

    def __str__(self):
        return f'{self.room_name}/{self.author}: {self.message}'
