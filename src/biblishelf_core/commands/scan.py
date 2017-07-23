from ..conf.register import iter_callback
from ..conf.repo import get_repo
from ..command import BaseCommand


class Scan(BaseCommand):

    def handle(self, *args, **kwargs):
        repo = get_repo()