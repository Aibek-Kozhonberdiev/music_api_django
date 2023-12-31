from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.base.services import default_avatar, get_path_update_avatar
from apps.base.my_gmail import welcome_messages


class Profile(models.Model):
    GENDER_CHOICES = [('Female', 'Female'), ('Male', 'Male')]
    avatar = models.ImageField(default=default_avatar, upload_to=get_path_update_avatar)
    description = models.TextField(max_length=2000, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=100, null=True, blank=True)
    update_to = models.DateTimeField(auto_now=True)
    key = models.CharField(max_length=225, null=True)

    def __str__(self):
        return self.user.username


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = 'Favorite'
        verbose_name_plural = 'Favorites'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'object_id', 'content_type'],
                name='unique_user_content_type_object_id'
            )
        ]

    def __str__(self):
        return f"Type: {self.content_type.name}, User: {self.user.username}"


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

        # Sending a welcome message to email for ordinary users
        if instance.is_staff == False:
            welcome_messages(instance)
