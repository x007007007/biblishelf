from django.core.files.storage import FileSystemStorage
from django.core.files.storage import validate_file_name
from django.core.files.storage import File
from biblishelf_web.apps.config.models import RepoConfigModel


class PortableStorage(FileSystemStorage):
    _location = None
    def __init__(self):
        super(PortableStorage, self).__init__()

    @property
    def location(self):
        return self._location

    def url(self, name):
        return f"/portable/storage/{name}"

    def save(self, name, content, max_length=None, using=None):
        self._using = using
        repo = RepoConfigModel.get_repo_path_map()[using]
        assert isinstance(repo, RepoConfigModel)
        self._location = repo.path

        if name is None:
            name = content.name

        if not hasattr(content, "chunks"):
            content = File(content, name)

        name = self.get_available_name(name, max_length=max_length)
        name = self._save(name, content)
        # Ensure that the name returned from the storage system is still valid.
        validate_file_name(name, allow_relative_path=True)
        return f"{using}/{name}"
