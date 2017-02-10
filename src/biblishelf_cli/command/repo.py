# -*- coding: utf-8 -*-

from cement.ext.ext_argparse import ArgparseController, expose


class RepoController(ArgparseController):
    class Meta:
        label = 'repo_controller'
        stacked_on = 'base'
        stacked_type = 'embedded'
        arguments = [
        ]
        

    def default(self):
        print("repo init")
    
    @expose(
        help="biblishelf repo"
    )
    def repo(self):
        print("repo status")