from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from . import serializers
from . import models
from .serializers import UserSerializer


class ProfileSetView(viewsets.ModelViewSet):
    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileSerializer


class UserSetView(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        user_data = {
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return Response(user_data, status=201)


    def retrieve(self, request, *args, **kwargs):
        try:
            get_object_or_404(User, pk=self.kwargs['pk'])
        except Http404:
            return Response({'detail': "the request was not applied because it lacked valid credentials"}, status=401)

        response = super().retrieve(request, *args, **kwargs)
        return response


class UserCreate(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        user_data = {
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return Response(user_data, status=201)
