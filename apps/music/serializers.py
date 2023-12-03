from rest_framework import serializers

from . import models


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = "__all__"


class MusicSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    music = serializers.FileField(required=False, write_only=True)
    views = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Music
        fields = "__all__"


class AlbumSerializer(serializers.ModelSerializer):
    music_set = MusicSerializer(many=True, read_only=True)

    class Meta:
        model = models.Album
        fields = "__all__"
