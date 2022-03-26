from django.db import models
# from django.contrib.auth.forms import User
from django.contrib.auth.models import User
from django.utils import timezone

# TODO: vyresit ruzne typy souboru


class Post(models.Model):
    # specialni znaky nefunguji
    caption = models.CharField(max_length=100, default="")
    image = models.ImageField(
        upload_to='post/image/%Y/%m', null=True, blank=True)
    video = models.FileField(null=True, blank=True,
                             upload_to='post/video/%Y/%m')
    file = models.FileField(null=True, blank=True, upload_to='post/file/%Y/%m')
    date = models.DateTimeField(
        default=timezone.now)  # TODO zmen tohle at to funguje
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.id)


class Comment(models.Model):
    c_post = models.ForeignKey(
        Post, related_name='c_post', on_delete=models.CASCADE, default=1)
    user = models.ForeignKey(User, related_name='user',
                             on_delete=models.CASCADE, default=2)
    comment = models.CharField(max_length=500)

    def __str__(self):
        return f'{self.id}|{self.user}'
