from rest_framework import generics
from rest_framework import serializers
from biblishelf_web.apps.config.models import RepoConfigModel
from django.db.models import Prefetch


class RepoConfigModelSerializer(serializers.ModelSerializer):
    repo = serializers.SerializerMethodField('get_database_config_key', read_only=True)

    class Meta:
        model = RepoConfigModel
        fields = (
            'pk',
            'path',
            'repo',
            'repo_meta',
        )

    def get_database_config_key(self, obj):
        return obj.get_database_config_key()


class RepoListApiView(generics.ListCreateAPIView):
    serializer_class = RepoConfigModelSerializer
    queryset = RepoConfigModel.objects.all()



class RepoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RepoConfigModelSerializer
    queryset = RepoConfigModel.objects.all()
