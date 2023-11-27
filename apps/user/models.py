from django.contrib.auth.models import User
from django.contrib.staticfiles import finders
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


def default_avatar():
    file_path = finders.find('profile/img/default.jpg')

    with open(file_path, 'rb') as file:
        return file


class Profile(models.Model):
    avatar = models.ImageField(default=default_avatar(), upload_to='avatar/')
    user = models.OneToOneField(User, on_delete=models.CASCADE)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
