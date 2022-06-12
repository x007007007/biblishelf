from rest_framework import generics
from rest_framework import serializers
from biblishelf_web.apps.main.models import ResourceModel
from biblishelf_web.apps.main.models import RepoModel
from biblishelf_web.apps.main.models import PathModel
from biblishelf_web.apps.main.models import MimeTypeModel


class RepoModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = RepoModel
        fields = [
            'uuid'
        ]


class PathModelSerializer(serializers.ModelSerializer):
    path = serializers.CharField(read_only=True)
    repo = RepoModelSerializer(read_only=True)

    class Meta:
        model = PathModel
        fields = [
            'path',
            'repo',
        ]


class MimeTypeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MimeTypeModel
        fields = [
            'pk',
            'mime',
        ]


class ResourceModelSerializer(serializers.ModelSerializer):
    path = PathModelSerializer(many=True, source="pathmodel_set")

    class Meta:
        model = ResourceModel
        fields = [
            'size',
            'mime_type',
            'path',
        ]


