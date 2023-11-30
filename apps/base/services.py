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
        content_file = ContentFile(img_file.read(), name=os.path.basename(default_image_user))
        return content_file
