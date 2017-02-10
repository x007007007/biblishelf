# -*- coding: utf-8 -*-

from cement.ext.ext_argparse import ArgparseController, expose


class InitController(ArgparseController):
    class Meta:
        label = 'init_controller'
        stacked_on = 'base'
        stacked_type = 'embedded'
        arguments = [
            (['--base-foo'], dict(help='base foo option')),
        ]

    def default(self):
        print("init init")

    @expose(
        arguments=[
            (['--command1-opt'],
             dict(help='option under command1', action='store_true'))
        ],
        help='init biblishelf repo',
    )
    def init(self):
        print("init repo")
