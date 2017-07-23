import six
import collections
import argparse


class BaseMetaCommand(type):
    commands = collections.OrderedDict()
    def __new__(self, name, classes, attrs):
        cmdclass = super(BaseMetaCommand, self).__new__(self, name, classes, attrs)
        if not attrs.get('abstract', False):
            self.commands[name] = cmdclass
        return cmdclass


class BaseCommand(six.with_metaclass(BaseMetaCommand)):
    abstract = True

    def __init__(self, argv):
        print(argv)
        parser = argparse.ArgumentParser(description='biblishelf command line tool')
        self.argv = argv

        self.add_arguments(parser)

        args = parser.parse_args(argv)

        self.handle(args)

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **kwargs):
        raise NotImplementedError