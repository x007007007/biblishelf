from pathlib import Path
import os
import uuid
import datetime
import json
from sqlalchemy import create_engine
from tzlocal import get_localzone
from biblishelf_core.models import Base as DataBase


class Generator(object):
    def __init__(self, name, owner=None, path=None, timezone=None):
        self.path = path if path is not None else Path.cwd()
        self.owner = owner if owner is not None else os.environ.get('USERNAME')
        self.uuid = uuid.uuid4()
        self.repo_name = name
        self.create_time = datetime.datetime.now()
        self.tz = timezone if timezone is not None else get_localzone()


    def meta_str(self):
        return json.dumps({
            "repo": self.repo_name,
            "uuid": uuid.uuid4().hex,
            "owner": self.owner,
            "create_time": str(self.create_time),
            "tz": str(self.tz)
        })

    def generate_repo(self):
        self.path.joinpath(".bibrepo").mkdir(exist_ok=True)
        with self.path.joinpath(".bibrepo/meta.json").open("w") as fp:
            fp.write(self.meta_str())
        db_str = 'sqlite:///{}'.format(self.path.joinpath(".bibrepo/index.db"))
        engine = create_engine(db_str, echo=True)
        DataBase.metadata.create_all(engine)

def main(name, ):
    gent = Generator(name)
    gent.generate_repo()


if __name__ == "__main__":
    main("test")