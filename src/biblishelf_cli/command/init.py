# -*- coding: utf-8 -*-
import os
from cement.ext.ext_argparse import ArgparseController, expose
from django.db import ConnectionHandler
from django.conf import settings as dj_settings
from django.conf import global_settings as dj_global_setting
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
        db_path = os.path.join(os.path.abspath(os.curdir), '.biblishelf/db.sqlite3')
        connections = ConnectionHandler({
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': db_path,
            }
        })
        connection = connections['default']
        dj_settings.configure(default_settings=dj_global_setting,
            **{
            'INSTALLED_APPS': [
                'biblishelf_main',
            ],
            "DATABASES": {
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': db_path,
                }
            }
        })
        from django.apps import apps
        apps.populate(dj_settings.INSTALLED_APPS)
        from django.db.migrations.executor import MigrationExecutor
        from django.db.migrations.autodetector import MigrationAutodetector
        from django.db.migrations.executor import MigrationExecutor
        from django.db.migrations.loader import AmbiguityError
        from django.db.migrations.state import ModelState, ProjectState

        connection.prepare_database()
        executor = MigrationExecutor(connection, self.migration_progress_callback)

        executor.loader.check_consistent_history(connection)
        conflicts = executor.loader.detect_conflicts()
        if conflicts:
            name_str = "; ".join(
                "%s in %s" % (", ".join(names), app)
                for app, names in conflicts.items()
            )
            raise Exception(
                "Conflicting migrations detected; multiple leaf nodes in the "
                "migration graph: (%s).\nTo fix them run "
                "'python manage.py makemigrations --merge'" % name_str
            )
        targets = executor.loader.graph.leaf_nodes()
        plan = executor.migration_plan(targets)
        pre_migrate_state = executor._create_project_state(with_applied_migrations=True)
        pre_migrate_apps = pre_migrate_state.apps
        post_migrate_state = executor.migrate(
            targets, plan=plan, state=pre_migrate_state.clone(), fake=False,
            fake_initial=False,
        )
        post_migrate_apps = post_migrate_state.apps

        with post_migrate_apps.bulk_update():
            model_keys = []
            for model_state in post_migrate_apps.real_models:
                model_key = model_state.app_label, model_state.name_lower
                model_keys.append(model_key)
                post_migrate_apps.unregister_model(*model_key)
        post_migrate_apps.render_multiple([
            ModelState.from_model(apps.get_model(*model)) for model in model_keys
        ])

        # Send the post_migrate signal, so individual apps can do whatever they need
        # to do at this point.
        # emit_post_migrate_signal(
        #    self.verbosity, self.interactive, connection.alias, apps=post_migrate_apps, plan=plan,
        # )

    def migration_progress_callback(self, action, migration=None, fake=False):
        if self.verbosity >= 1:
            compute_time = self.verbosity > 1
            if action == "apply_start":
                if compute_time:
                    self.start = time.time()
                self.stdout.write("  Applying %s..." % migration)
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
                self.stdout.write("  Unapplying %s..." % migration)
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
                self.stdout.write("  Rendering model states...")
                self.stdout.flush()
            elif action == "render_success":
                elapsed = " (%.3fs)" % (time.time() - self.start) if compute_time else ""
                self.stdout.write(self.style.SUCCESS(" DONE" + elapsed))

