import os

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.massage_email.my_email import send_message


def default_avatar():
    default_image_user = os.path.join(settings.STATIC_ROOT, 'project', 'img', 'default.jpeg')
    with open(default_image_user, 'rb') as img_file:
        content_file = ContentFile(img_file.read(), name=os.path.basename(default_image_user))
        return content_file


class Profile(models.Model):
    avatar = models.ImageField(default=default_avatar(), upload_to='avatar/')
    user = models.OneToOneField(User, on_delete=models.CASCADE)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        message = f"Hello, {instance.unsername}"
        send_message(message, 'email/hello_massage.html', instance)
