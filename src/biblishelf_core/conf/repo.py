from pathlib import Path
from collections import namedtuple
from ..models import Base
from sqlalchemy.orm import sessionmaker
import json
from sqlalchemy import create_engine
import os


class NotExistRepoError(FileNotFoundError):
    pass


class RepoError(Exception):
    pass


class RepoConfig(object):
    debug = False

    def __init__(self, path):
        self.path = Path(path) if not isinstance(path, Path) else path
        if not self.path.exists():
            raise FileExistsError(path)
        if not self.path.joinpath(".bibrepo").exists():
            raise NotExistRepoError(path)
        meta_path = self.path.joinpath(".bibrepo/meta.json")
        if not meta_path.exists():
            raise RepoError(path)
        else:
            with meta_path.open() as fp:
                try:
                    self.meta = namedtuple('meta', json.load(fp))
                except json.JSONDecodeError as e:
                    raise RepoError(e.msg)
        self.db_path = self.path.joinpath(".bibrepo/index.db")
        if not self.db_path.exists():
            raise RepoError("database not exist")
        else:
            self.engine = create_engine('sqlite:///{}'.format(self.db_path), echo=self.debug)
            self.Session = sessionmaker(bind=self.engine)


current_repo = None

def get_repo(path=None):
    path = os.path.abspath(path or '.')
    if isinstance(path, str):
        path = Path(path)
    while True:
        try:
            current_repo = RepoConfig(path)
            return current_repo
        except NotExistRepoError:
            if len(path.parts) > 1:
                path = path.parent
            else:
                return None