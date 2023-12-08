from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models

from apps.base.services import get_path_podcast_file
from apps.music.models import Category


class Podcast(models.Model):
    icon = models.ImageField(upload_to=get_path_podcast_file)
    title = models.CharField(max_length=225)
    description = models.TextField(max_length=2000)
    audio = models.FileField(
        upload_to=get_path_podcast_file,
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    'mp3',
                    'wav',
                    'ogg'
                ]
            )
        ]
    )
    create_at = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, blank=True)
    views = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Podcast: {self.user.username}"
