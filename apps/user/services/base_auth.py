from rest_framework_simplejwt.tokens import RefreshToken

from .. import serializers


def create_token(user):
    refresh = RefreshToken.for_user(user)

    return {
        'user': serializers.GoogleAuthSerializer(user).data,
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
