from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models

from apps.base.services import get_path_update_cover


class Music(models.Model):
    image = models.ImageField(upload_to=get_path_update_cover)
    title = models.CharField(max_length=150)
    cover = models.FileField(
        upload_to=get_path_update_cover,
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
    views = models.IntegerField(default=0)
    category = models.ManyToManyField("Category", blank=True, related_name='categories')
    album = models.ForeignKey("Album", blank=True, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.title


class Album(models.Model):
    title = models.CharField(max_length=150, db_index=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
