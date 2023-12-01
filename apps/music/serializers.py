from rest_framework import serializers

from . import models


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = "__all__"


class CoverSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    cover = serializers.FileField(required=False)
    views = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Music
        fields = "__all__"


class AlbumSerializer(serializers.ModelSerializer):
    cover_set = CoverSerializer(many=True, read_only=True)

    class Meta:
        model = models.Album
        fields = "__all__"
