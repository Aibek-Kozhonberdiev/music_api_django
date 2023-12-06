import random

from django.contrib.auth.hashers import make_password, check_password

from apps.base.my_gmail import key_message
from apps.user import models


NUMBERS_KEY = '1234567890'


def key_generate(user):
    """This method creates, generates a key and caches it
    """
    key: str = ''.join(random.choice(NUMBERS_KEY) for _ in range(10))
    # Sending a key to a user via gmail
    key_message(user, key)

    profile = models.Profile.objects.get(user=user)
    profile.key = make_password(key)
    profile.save()


def key_chek(user, key):
    """Checking the authenticity of the key
    """
    profile = models.Profile.objects.get(user=user)
    raw_password = profile.key
    return check_password(key, raw_password)
