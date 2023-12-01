import os

from django.conf import settings
from django.core.files.base import ContentFile


def delete_of_file(path_file):
    """Deleting an old file
    """
    if os.path.exists(path_file):
        os.remove(path_file)


def default_avatar():
    """To create a default avatar
    """
    default_image_user = os.path.join(settings.STATIC_ROOT, 'project', 'img', 'default.jpeg')
    with open(default_image_user, 'rb') as img_file:
        content_file = ContentFile(img_file.read(), name='default.jpeg')
        return content_file


def get_path_update_avatar(instance, file):
    """Building a path for a user avatar, format(media): img
    """
    return f"avatar/user_{instance.user.id}/{file}"


def get_path_update_music(instance, file):
    """Building a path for a user cover, format(media): img, music
    """
    return f"music/user_{instance.user.id}/{file}"
