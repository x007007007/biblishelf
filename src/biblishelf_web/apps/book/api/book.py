from rest_framework import generics
from rest_framework import serializers
from biblishelf_web.apps.main.serializer import ResourceModelSerializer

from biblishelf_web.apps.book.models import BookModel
from biblishelf_web.apps.main.models import PathModel
from django.db.models import Prefetch


class BookModelSerializer(serializers.ModelSerializer):
    resource = ResourceModelSerializer(read_only=True)
    name = serializers.CharField()

    class Meta:
        model = BookModel
        fields = (
            'resource',
            'cover',
            'name',
            'isbn',
            'publisher',
            'page_number',
            'douban_id',
        )


class BookListApiView(generics.ListCreateAPIView):
    serializer_class = BookModelSerializer

    def get_queryset(self):
        db = self.kwargs.get('db', 'default')
        return BookModel.objects.using(db).select_related(
            'resource',
            'resource__mime_type',
        ).filter(parent__isnull=True).prefetch_related(
            Prefetch('resource__pathmodel_set', queryset=PathModel.objects.using(
                db
            ).select_related(
                'repo',
            ).all())
        )
