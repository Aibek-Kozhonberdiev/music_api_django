from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.base.services import default_avatar, get_path_update_avatar
from apps.base.my_gmail import welcome_messages


class Profile(models.Model):
    avatar = models.ImageField(default=default_avatar, upload_to=get_path_update_avatar)
    description = models.TextField(max_length=2000)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

        # Sending a welcome message to email for ordinary users
        if instance.is_staff == False:
            welcome_messages(instance)
