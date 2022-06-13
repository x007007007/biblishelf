import os.path

from django.views import static
from biblishelf_web.apps.config.models import RepoConfigModel
from biblishelf_web.apps.main.models import PathModel


def portable_static(request, repo_id, path):
    repo = RepoConfigModel.get_repo_path_map()[repo_id]
    return static.serve(request, path=path, document_root=repo.path)


def portable_path(request, repo_id, path_id):
    repo = RepoConfigModel.get_repo_path_map()[repo_id]
    if not (path_obj := PathModel.objects.using(repo_id).filter(id=path_id).first()):
        path_obj.is_exist = False
        path_obj.save(update_fields=('is_exist',), using=repo_id)
    return static.serve(request, path=path_obj.path, document_root=repo.path)