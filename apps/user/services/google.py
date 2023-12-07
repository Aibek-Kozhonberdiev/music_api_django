from django.contrib.auth.models import User
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework_simplejwt.tokens import RefreshToken

from .. import serializers


def check_google_auth(google_user: serializers.GoogleAuthSerializer) -> dict:
    try:
        id_token.verify_oauth2_token(
            google_user['token'], requests.Request(), settings.GOOGLE_CLIENT_ID
        )
    except ValueError:
        raise AuthenticationFailed(code=403, detail='Bad token Google')

    user = User.objects.get_or_create(username=google_user['name'], email=google_user['email'])
    refresh = RefreshToken.for_user(user)

    return {
        'user': serializers.GoogleAuthSerializer(user).data,
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
