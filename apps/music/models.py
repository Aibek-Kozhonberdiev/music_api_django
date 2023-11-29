from django.contrib.auth.models import User
from django.db import models


class Music(models.Model):
    image = models.ImageField(upload_to='music_img/')
    title = models.CharField(max_length=150)
    music = models.FileField(upload_to='music/')
    create = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)
    category = models.ForeignKey("Category", null=True, blank=True, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Category(models.Model):
    title = models.CharField(max_length=100, db_index=True)
