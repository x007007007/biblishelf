# -*- coding: utf-8 -*-

from cement.ext.ext_argparse import ArgparseController, expose


class SearchController(ArgparseController):
    class Meta:
        label = 'search_controller'
        stacked_on = 'base'
        stacked_type = 'embedded'
        arguments = [
        ]

    def default(self):
        print("status init")

    @expose(
        arguments=[
            (['--command1-opt'],
             dict(help='option under command1', action='store_true'))
        ],
        help='search index',
    )
    def search(self):
        print("search index")