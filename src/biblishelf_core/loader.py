from biblishelf_core.conf.repo import get_repo
import importlib
from collections import OrderedDict
import pkgutil
from biblishelf_core import command
import sys


class Loader(object):
    def __init__(self):
        self.plugin = OrderedDict()
        self.models = OrderedDict()

    def load_plugin_models(self):
        for module_loader, name, is_pkg in pkgutil.iter_modules():
            if(name.startswith("biblishelf_plugin_")):
                try:
                    self.models[name[len("biblishelf_plugin_"):]] = importlib.import_module("{}.models".format(name))
                except ImportError:
                    pass

    def load_plugin(self):
        from biblishelf_core import commands
        for module_loader, name, is_pkg in pkgutil.iter_modules():
            if(name.startswith("biblishelf_plugin_")):
                try:
                    self.models[name[len("biblishelf_plugin_"):]] = importlib.import_module("{}".format(name))
                except ImportError:
                    pass
                try:
                    self.models[name[len("biblishelf_plugin_"):]] = importlib.import_module("{}.commands".format(name))
                except ImportError:
                    pass


    def __enter__(self):
        self.load_plugin_models()
        self.load_plugin()
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def command_entry():
    with Loader() as loader:
        for cmd, cls in command.BaseMetaCommand.commands.items():
            if len(sys.argv) > 1:
                if cmd.lower() == sys.argv[1]:
                    cls(sys.argv[2:])
            else:
                print(cmd.lower())

def main():
    with Loader() as l:
        print(l)
    l = Loader()
    l.load_plugin()
    print(l.models)

if __name__ == "__main__":
    command_entry()

