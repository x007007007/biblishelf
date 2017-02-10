# -*- coding: utf-8 -*-

from cement.ext.ext_argparse import ArgparseController, expose


class GlobalController(ArgparseController):
    class Meta:
        label = 'base'


    def default(self):
        print("init init")
