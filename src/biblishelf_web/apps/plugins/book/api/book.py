import json

from rest_framework import generics
from rest_framework import serializers
from rest_framework import filters
from django.db.models import Count
import django.forms
from biblishelf_web.apps.main.serializer import ResourceModelSerializer

from biblishelf_web.apps.plugins.book.models import BookModel
from biblishelf_web.apps.main.models import PathModel
from django.db.models import Prefetch
import django_filters
import django_filters.constants


class BookModelSerializer(serializers.ModelSerializer):
    resource = ResourceModelSerializer(read_only=True)
    name = serializers.CharField()
    info = serializers.SerializerMethodField('get_info')

    class Meta:
        model = BookModel
        fields = (
            'pk',
            'resource',
            'cover',
            'name',
            'isbn',
            'publisher',
            'page_number',
            'douban_id',
            'info',
        )

    def get_info(self, obj):
        if obj.info:
            return json.loads(obj.info)


class BooleanEmptyCharFilter(django_filters.Filter):
    field_class = django.forms.NullBooleanField

    def filter(self, qs, value):
        from django.db.models import Q
        if value in django_filters.constants.EMPTY_VALUES:
            return qs
        if self.distinct:
            qs = qs.distinct()
        lookup = '%s__%s' % (self.field_name, self.lookup_expr)
        sub_q = Q(**{f'{self.field_name}': ""}) | Q(**{f'{self.field_name}__isnull': True})
        if not value:
            sub_q = ~sub_q
        qs = self.get_method(qs)(sub_q)
        return qs


class ExistSubSetFilter(django_filters.Filter):
    field_class = django.forms.NullBooleanField

    def filter(self, qs, value):
        from django.db.models import Q
        if value in django_filters.constants.EMPTY_VALUES:
            return qs
        res = PathModel.objects.values(
            'resource_id'
        ).annotate(
            total_count=Count('path')
        ).filter(
            total_count__gt=0
        ).values(
            'resource_id'
        )
        if value:
            qs = qs.filter(resource__in=res)
        else:
            qs = qs.exclude(resource__in=res)
        return qs


class BookFilter(django_filters.FilterSet):
    exist_isbn = BooleanEmptyCharFilter(
        label='exist isbn',
        field_name='isbn_str',
        exclude=True,
    )
    exist_douban_id = BooleanEmptyCharFilter(
        label='exist douban id',
        field_name='douban_id',
        exclude=True,
    )
    page_number = django_filters.RangeFilter()
    exist_cover = BooleanEmptyCharFilter(
        label="exist cover",
        field_name='cover',
        exclude=True
    )
    exist_path = ExistSubSetFilter(
        label='exist path',
        field_name="resource__pathmodel_set"
    )

    class Meta:
        model = BookModel
        fields = (
            'isbn',
            'publisher',
            'page_number',
            'exist_isbn',
            'exist_douban_id',
        )


class BookListApiView(generics.ListCreateAPIView):
    serializer_class = BookModelSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter)
    filter_class = BookFilter
    search_fields = (
        'name',
    )

    def get_queryset(self):
        db = self.kwargs.get('db_key', 'default')
        return BookModel.objects.using(db).select_related(
            'resource',
            'resource__mime_type',
        ).filter(parent__isnull=True).prefetch_related(
            Prefetch('resource__pathmodel_set', queryset=PathModel.objects.using(
                db
            ).select_related(
                'repo',
            ).filter(is_exist=True))
        )


class BookRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookModelSerializer

    def get_queryset(self):
        db = self.kwargs.get('db_key', 'default')
        return BookModel.objects.using(db).all()
