import os

from django.http import FileResponse, Http404
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404

from . import serializers
from . import models


class PodcastViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PodcastSerializer
    queryset = models.Podcast.objects.order_by('-views', '-create_at')

    def add_views(self, podcast):
        """For add views podcast
        """
        podcast.views += 1
        podcast.save()

    def retrieve(self, request, *args, **kwargs):
        podcast = get_object_or_404(models.Podcast, pk=self.kwargs['pk'])
        if os.path.exists(podcast.audio.path):
            self.add_views()
            return FileResponse(open(podcast.audio.path, 'rb'), filename=podcast.audio.name)
        else:
            return Http404
