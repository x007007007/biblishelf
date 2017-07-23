from ..conf.register import iter_callback
from ..repo.generate import Generator
from ..command import BaseCommand


class Init(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('name')


    def handle(self, name, *args, **kwargs):
        generater = Generator(name)
        generater.generate_repo()


