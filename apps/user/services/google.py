from django.contrib.auth.models import User
from google.oauth2 import id_token
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from google.auth.transport import requests

from . import base_auth
from .. import serializers


def check_google_auth(google_user: serializers.GoogleAuthSerializer) -> dict:
    try:
        id_token.verify_oauth2_token(
            google_user['token'], requests.Request(), settings.GOOGLE_CLIENT_ID
        )
    except ValueError:
        raise AuthenticationFailed(code=403, detail='Bad token Google')

    user = User.objects.get_or_create(username=google_user['name'], email=google_user['email'])

    return base_auth.create_token(user)
