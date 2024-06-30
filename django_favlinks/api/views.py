from rest_framework import viewsets
from django_favlinks.models import Bookmark
from . import serializers


class BookmarkViewSet(viewsets.ModelViewSet):
    queryset = Bookmark.objects.prefetch_related("tags").all()
    serializer_class = serializers.BookmarkSerializer
