from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models

from apps.base.services import get_path_update_music, get_path_update_category


class Music(models.Model):
    image = models.ImageField(upload_to=get_path_update_music)
    title = models.CharField(max_length=150)
    music = models.FileField(
        upload_to=get_path_update_music,
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    'mp3',
                    'wav'
                ]
            )
        ]
    )
    create = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
    category = models.ManyToManyField("Category", blank=True, related_name='categories')
    album = models.ForeignKey("Album", blank=True, null=True, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Category(models.Model):
    image = models.ImageField(upload_to=get_path_update_category)
    title = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.title


class Album(models.Model):
    title = models.CharField(max_length=150, db_index=True)
    create = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
