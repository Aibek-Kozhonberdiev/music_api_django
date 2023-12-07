from django.contrib.auth.models import User
from django.http import Http404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions

from . import serializers
from . import models
from .services import google
from .services.key_generate import key_generate, key_chek
from ..base.services import delete_of_file


class ProfileSetView(viewsets.ModelViewSet):
    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            get_object_or_404(models.Profile, id=self.kwargs['pk'])
        except Http404:
            return Response({'detail': "the request was not applied because it lacked valid credentials"}, status=401)

        return super().retrieve(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        raise Http404


class UserSetView(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        user_data = {
            'user': serializers.UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        # Add the full URL for the avatar
        user_data['user']['profile']['avatar'] = request.build_absolute_uri(user_data['user']['profile']['avatar'])

        return Response(user_data, status=201)

    @swagger_auto_schema(
        operation_description='To change your profile',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "username": openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.FORMAT_PASSWORD),
                'password2': openapi.Schema(type=openapi.FORMAT_PASSWORD),
                "email": openapi.Schema(type=openapi.FORMAT_EMAIL),
                "key": openapi.Schema(type=openapi.FORMAT_PASSWORD, description='The key is received by the user when sending a request to a special endpoint by mail')
            }
        )
    )
    def update(self, request, *args, **kwargs):
        key = request.data.get('key')
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        if key_chek(user, key) is False:
            return Response({"key": "the key does not match or has expired"}, status=400)

        return super().update(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        try:
            get_object_or_404(User, pk=self.kwargs['pk'])
        except Http404:
            return Response({'detail': "the request was not applied because it lacked valid credentials"}, status=401)

        return super().retrieve(request, *args, **kwargs)

    def perform_destroy(self, instance):
        delete_of_file(instance.profile.avatar.path)
        instance.delete()


class UserCreate(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description='Creating a user without using a token',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "username": openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.FORMAT_PASSWORD),
                'password2': openapi.Schema(type=openapi.FORMAT_PASSWORD),
                "email": openapi.Schema(type=openapi.FORMAT_EMAIL),
            }
        )
    )
    def post(self, request, *args, **kwargs):
        serializer = serializers.UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        user_data = {
            'user': serializers.UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        # Add the full URL for the avatar
        user_data['user']['profile']['avatar'] = request.build_absolute_uri(user_data['user']['profile']['avatar'])

        return Response(user_data, status=201)


class FavoriteSetView(viewsets.ModelViewSet):
    queryset = models.Favorite.objects.all()
    serializer_class = serializers.FavoriteSerializer

    def get_queryset(self):
        return models.Favorite.objects.filter(user=self.request.user)


class KeyPostView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description='Required to generate a confirmation key when the user password is lost',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "email": openapi.Schema(type=openapi.FORMAT_EMAIL),
            }
        )
    )
    def post(self, request):
        try:
            email = request.data.get('email')
            user = get_object_or_404(User, email=email)
            key_generate(user)
            return Response({'detail': "The key was successfully generated"}, status=201)
        except Http404:
            return Response({'detail': "the request was not applied because it lacked valid credentials"}, status=401)


@api_view(["POST"])
def google_auth(request):
    """Authorization confirmation via Google
    """
    google_data = serializers.GoogleAuthSerializer(data=request.data)
    if google_data.is_valid():
        user_data = google.check_google_auth(google_data.data)
        return Response(user_data)
    else:
        return AuthenticationFailed(code=403, detail='Bad data Google')
