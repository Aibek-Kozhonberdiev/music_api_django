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
    default_image_user = settings.DEFAULT_AVATAR_PATH
    with open(default_image_user, 'rb') as img_file:
        content_file = ContentFile(img_file.read(), name='default.jpeg')
        return content_file


def get_path_update_avatar(instance, file):
    """Building a path for a user avatar, format(media): img
    """
    return f"user_{instance.user.id}/avatar/{file}"


def get_path_update_music(instance, file):
    """Building a path for a user cover, format(media): img, music
    """
    return f"user_{instance.user.id}/music/{file}"


def get_path_update_album(instance, file):
    """Building a path for a user album, format(media): img
    """
    return f"user_{instance.author.id}/album/{file}"


def get_path_update_category(instance, file):
    """Building a path for a category(media): img
    """
    return f"category/{file}"


def get_path_podcast_file(instance, file):
    """Building a path for a podcast(media): img, audio
    """
    return f"user_{instance.user.id}/podcast/{file}"
