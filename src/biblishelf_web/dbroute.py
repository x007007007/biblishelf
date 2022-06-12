from .middleware import db_config


class AdminRouter(object):

    repo_apps = ['biblishelf_main', 'biblishelf_book']

    def db_for_read(self, model, **hints):
        "Point all operations on chinook models to 'chinookdb'"
        if model._meta.app_label in self.repo_apps:
            db = getattr(db_config, 'dbid', 'default')
            return db
        return 'default'

    def db_for_write(self, model, **hints):
        "Point all operations on chinook models to 'chinookdb'"
        if model._meta.app_label in self.repo_apps:
            db = getattr(db_config, 'dbid', 'default')
            return db
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_syncdb(self, db, model):
        return True