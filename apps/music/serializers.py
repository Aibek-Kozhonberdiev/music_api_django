from rest_framework import serializers

from . import models
from ..base.services import delete_of_file


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

    def update(self, instance, validated_data):
        delete_of_file(instance.image.path)
        delete_of_file(instance.music.path)
        return super().update(instance, validated_data)


class AlbumSerializer(serializers.ModelSerializer):
    music_set = MusicSerializer(many=True, read_only=True)

    class Meta:
        model = models.Album
        fields = "__all__"

    def update(self, instance, validated_data):
        delete_of_file(instance.image.path)
        return super().update(instance, validated_data)
