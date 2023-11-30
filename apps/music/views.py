from rest_framework import viewsets
from rest_framework.generics import get_object_or_404

from . import serializers
from . import models
from ..base.services import delete_of_file


class MusicSetView(viewsets.ModelViewSet):
    serializer_class = serializers.MusicSerializer
    queryset = models.Music.objects.order_by('-create', "-views")

    def retrieve(self, request, *args, **kwargs):
        music = get_object_or_404(models.Music, pk=self.kwargs['pk'])
        music.views += 1
        music.save()

        response = super().retrieve(request, *args, **kwargs)
        return response

    def perform_destroy(self, instance):
        delete_of_file(instance.image.path)
        delete_of_file(instance.cover.path)
        instance.delete()


class CategorySetView(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()
