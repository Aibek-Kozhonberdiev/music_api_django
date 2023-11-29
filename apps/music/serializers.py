from rest_framework import serializers

from . import models


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = "__all__"


class MusicSerializer(serializers.ModelSerializer):
    music = serializers.FileField(required=True)
    views = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Music
        fields = "__all__"
