from rest_framework import serializers

from . import models


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = "__all__"


class MusicSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    music = serializers.FileField(required=False)
    views = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Music
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # Remove music field from output on GET request
        if self.context['request'].method == 'GET':
            data.pop('music', None)

        return data


class AlbumSerializer(serializers.ModelSerializer):
    music_set = MusicSerializer(many=True, read_only=True)

    class Meta:
        model = models.Album
        fields = "__all__"
