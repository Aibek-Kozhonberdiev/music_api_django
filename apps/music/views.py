import re
import os
import mimetypes

from django.http import Http404, FileResponse, HttpResponse
from rest_framework import viewsets, parsers
from rest_framework.generics import get_object_or_404

from . import serializers
from . import models
from ..base.services import delete_of_file


class MusicSetView(viewsets.ModelViewSet):
    serializer_class = serializers.MusicSerializer
    parser_classes = (parsers.MultiPartParser, )
    queryset = models.Music.objects.order_by('-create', "-views")

    def add_views(self, music):
        """ When listening, adds views by 1
        """
        music.views += 1
        music.save()

    def retrieve(self, request, *args, **kwargs):
        music = get_object_or_404(models.Music, id=self.kwargs['pk'])
        if os.path.exists(music.music.path):
            self.add_views(music)

            # Getting the Range header from a request
            range_header = request.headers.get('Range')
            content_type, _ = mimetypes.guess_type(music.music.path)

            if range_header:
                # If there is a Range request, send part of the file
                file_size = os.path.getsize(music.music.path)
                start, end = self.parse_range_header(range_header, file_size)
                file_part = open(music.music.path, 'rb')
                file_part.seek(start)
                data = file_part.read(end - start + 1)
                file_part.close()

                response = HttpResponse(data, content_type=content_type, status=206)
                response['Content-Range'] = f'bytes {start}-{end}/{file_size}'
            else:
                # Otherwise we send the entire file
                data = open(music.music.path, 'rb').read()
                response = FileResponse(open(music.music.path, 'rb'), content_type=content_type)

            response['Accept-Ranges'] = 'bytes'
            return response
        else:
            raise Http404

    def parse_range_header(self, range_header, file_size):
        match = re.match(r'bytes\s*=\s*(\d+)-(\d*)', range_header)
        if match:
            start = int(match.group(1))
            end = int(match.group(2)) if match.group(2) else file_size - 1
            return start, end
        return 0, file_size - 1

    def perform_destroy(self, instance):
        delete_of_file(instance.image.path)
        delete_of_file(instance.music.path)
        instance.delete()


class CategorySetView(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()
    pagination_class = None


class AlbumSetView(viewsets.ModelViewSet):
    serializer_class = serializers.AlbumSerializer
    queryset = models.Album.objects.all()
