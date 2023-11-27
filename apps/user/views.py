from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers
from . import models


class ProfileSetView(viewsets.ModelViewSet):
    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileSerializer


class UserSetView(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            get_object_or_404(User, pk=self.kwargs['pk'])
        except Http404:
            return Response({'error': "the request was not applied because it lacked valid credentials"}, status=401)

        super().retrieve(request, *args, **kwargs)


class UserCreate(APIView):
    def post(self, request):
        pass
