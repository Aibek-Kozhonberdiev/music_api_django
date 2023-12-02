import os

from django.http import Http404, FileResponse
from rest_framework import viewsets, parsers
from rest_framework.generics import get_object_or_404

from . import serializers
from . import models
from ..base.services import delete_of_file


class MusicSetView(viewsets.ModelViewSet):
    serializer_class = serializers.MusicSerializer
    parser_classes = (parsers.MultiPartParser, )
    queryset = models.Music.objects.order_by('-create', "-views")

    def add_views(self):
        """ When listening, adds views by 1
        """
        music = models.Music.objects.get(pk=self.kwargs['pk'])
        music.views += 1
        music.save()

    # def retrieve(self, request, *args, **kwargs):
    #     music = get_object_or_404(models.Music, id=self.kwargs['pk'])
    #     if os.path.exists(music.music.path):
    #         self.add_views()
    #         return FileResponse(open(music.music.path, 'rb'), filename=music.music.name)
    #     else:
    #         return Http404

    def perform_destroy(self, instance):
        delete_of_file(instance.image.path)
        delete_of_file(instance.music.path)
        instance.delete()


class CategorySetView(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()


class AlbumSetView(viewsets.ModelViewSet):
    serializer_class = serializers.AlbumSerializer
    queryset = models.Album.objects.all()
