# -*- coding: utf-8 -*-
import os
from cement.ext.ext_argparse import ArgparseController, expose
from django.db import ConnectionHandler
from django.db.migrations.autodetector import MigrationAutodetector
from django.db.migrations.executor import MigrationExecutor
import sys
import time

class InitController(ArgparseController):
    class Meta:
        label = 'init_controller'
        stacked_on = 'base'
        stacked_type = 'embedded'
        arguments = [
            (['--base-foo'], dict(help='base foo option')),
        ]

    class style:
        @staticmethod
        def SUCCESS(self, *args, **kwargs):
            print(*args, **kwargs)

    def default(self):
        pass

    verbosity = 5
    stdout = sys.stdout

    @expose(
        arguments=[
            (['--command1-opt'],
             dict(help='option under command1', action='store_true'))
        ],
        help='init biblishelf repo',
    )
    def init(self):
        print(os.path.abspath(os.curdir))
        connections = ConnectionHandler({
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(os.path.abspath(os.curdir), '.biblishelf/db.sqlite3'),
            }
        })
        connection = connections['default']
        connection.prepare_database()

        executor = MigrationExecutor(connection, self.migration_progress_callback)

    def migration_progress_callback(self, action, migration=None, fake=False):
        if self.verbosity >= 1:
            compute_time = self.verbosity > 1
            if action == "apply_start":
                if compute_time:
                    self.start = time.time()
                self.stdout.write("  Applying %s..." % migration, ending="")
                self.stdout.flush()
            elif action == "apply_success":
                elapsed = " (%.3fs)" % (time.time() - self.start) if compute_time else ""
                if fake:
                    self.stdout.write(" FAKED" + elapsed)
                else:
                    self.stdout.write(" OK" + elapsed)
            elif action == "unapply_start":
                if compute_time:
                    self.start = time.time()
                self.stdout.write("  Unapplying %s..." % migration, ending="")
                self.stdout.flush()
            elif action == "unapply_success":
                elapsed = " (%.3fs)" % (time.time() - self.start) if compute_time else ""
                if fake:
                    self.stdout.write(self.style.SUCCESS(" FAKED" + elapsed))
                else:
                    self.stdout.write(self.style.SUCCESS(" OK" + elapsed))
            elif action == "render_start":
                if compute_time:
                    self.start = time.time()
                self.stdout.write("  Rendering model states...", ending="")
                self.stdout.flush()
            elif action == "render_success":
                elapsed = " (%.3fs)" % (time.time() - self.start) if compute_time else ""
                self.stdout.write(self.style.SUCCESS(" DONE" + elapsed))

