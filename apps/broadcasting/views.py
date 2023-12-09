import os
import re
import mimetypes

from django.http import FileResponse, Http404, HttpResponse
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404

from . import serializers
from . import models


class PodcastViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PodcastSerializer
    queryset = models.Podcast.objects.order_by('-views', '-create_at')


class PodcastReadOnly(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.PodcastSerializer
    queryset = models.Podcast.objects.order_by('-views', '-create_at')

    def add_views(self, podcast):
        """For add views podcast
        """
        podcast.views += 1
        podcast.save()

    def parse_range_header(self, range_header, file_size):
        match = re.match(r'bytes\s*=\s*(\d+)-(\d*)', range_header)
        if match:
            start = int(match.group(1))
            end = int(match.group(2)) if match.group(2) else file_size - 1
            return start, end
        return 0, file_size - 1

    def retrieve(self, request, *args, **kwargs):
        podcast = get_object_or_404(models.Podcast, pk=self.kwargs['pk'])
        if os.path.exists(podcast.audio.path):
            self.add_views()

            # Getting the Range header from a request
            range_header = request.headers.get('Range')
            content_type, _ = mimetypes.guess_type(podcast.podcast.path)

            if range_header:
                # If there is a Range request, send part of the file
                file_size = os.path.getsize(podcast.podcast.path)
                start, end = self.parse_range_header(range_header, file_size)
                file_part = open(podcast.podcast.path, 'rb')
                file_part.seek(start)
                data = file_part.read(end - start + 1)
                file_part.close()

                response = HttpResponse(data, content_type=content_type, status=206)
                response['Content-Range'] = f'bytes {start}-{end}/{file_size}'
                response['Accept-Ranges'] = 'bytes'
                return response

            return FileResponse(open(podcast.audio.path, 'rb'), filename=podcast.audio.name)
        else:
            return Http404
