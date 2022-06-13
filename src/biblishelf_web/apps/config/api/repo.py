from rest_framework import generics
from rest_framework import serializers
from biblishelf_web.apps.config.models import RepoConfigModel
from biblishelf_web.apps.main.serializer import RepoModelSerializer
from django.db.models import Prefetch


class RepoConfigModelSerializer(serializers.ModelSerializer):
    repo = RepoModelSerializer(read_only=True)

    class Meta:
        model = RepoConfigModel
        fields = (
            'pk',
            'path',
            'repo',
            'repo_meta',
        )


class RepoListApiView(generics.ListCreateAPIView):
    serializer_class = RepoConfigModelSerializer
    queryset = RepoConfigModel.objects.all()



class RepoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RepoConfigModelSerializer
    queryset = RepoConfigModel.objects.all()
