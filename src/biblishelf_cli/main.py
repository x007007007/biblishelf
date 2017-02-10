from cement.core import foundation
from cement.utils.misc import init_defaults
from . import command


defaults = init_defaults('biblishelf_cli')

class BiblishelfCli(foundation.CementApp):
    class Meta:
        label = "bilishelf_cli"
        handlers = [
            command.GlobalController,
            command.InitController,
            command.StatusController,
            command.SearchController,
            command.RepoController,
            command.PluginController,
        ]


def main():
    with BiblishelfCli(config_defaults=defaults) as app:
        app.run()


if __name__ == "__main__":
    main()
