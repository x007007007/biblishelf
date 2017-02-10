# -*- coding: utf-8 -*-

from cement.ext.ext_argparse import ArgparseController, expose


class PluginController(ArgparseController):
    class Meta:
        label = 'plugin_controller'
        stacked_on = 'base'
        stacked_type = 'embedded'
        arguments = [
        ]

    def default(self):
        print("plugin init")

    @expose(
        help="plugin info"
    )
    def plugins(self):
        print("plugin status")