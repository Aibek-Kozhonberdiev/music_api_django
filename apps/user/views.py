from django.contrib.auth.models import User
from django.http import Http404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions

from . import serializers
from . import models
from ..base.services import delete_of_file


class ProfileSetView(viewsets.ModelViewSet):
    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            get_object_or_404(models.Profile, id=self.kwargs['pk'])
        except Http404:
            return Response({'detail': "the request was not applied because it lacked valid credentials"}, status=401)

        response = super().retrieve(request, *args, **kwargs)
        return response


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

    def retrieve(self, request, *args, **kwargs):
        try:
            get_object_or_404(User, pk=self.kwargs['pk'])
        except Http404:
            return Response({'detail': "the request was not applied because it lacked valid credentials"}, status=401)

        response = super().retrieve(request, *args, **kwargs)
        return response

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
