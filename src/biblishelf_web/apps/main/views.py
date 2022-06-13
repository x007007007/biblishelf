from django.views import static
from biblishelf_web.apps.config.models import RepoConfigModel


def portable_static(request, repo_id, path):
    repo = RepoConfigModel.get_repo_path_map()[repo_id]
    return static.serve(request, path=path, document_root=repo.path)