from rest_framework import serializers

from . import models


class PodcastSerializer(serializers.ModelSerializer):
    icon = serializers.ImageField(required=False)
    audio = serializers.FileField(required=False, write_only=True)
    views = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Podcast
        fields = "__all__"

