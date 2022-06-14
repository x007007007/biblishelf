import traceback
from django.dispatch import receiver
from django.apps import AppConfig
from biblishelf_web.signals import db_config_loss_signal


@receiver(db_config_loss_signal)
def reload_database_map(sender=None, lose_key=None, **kwargs):
    from .models import RepoConfigModel  # or...
    for config in RepoConfigModel.objects.only('path').all():
        if k := config.update_database_map():
            if lose_key and lose_key == k:
                break
            print(f"config db: {k}")


class BiblishelfConfigConfig(AppConfig):

    name = 'biblishelf_web.apps.config'
    label = 'biblishelf_config'

    def ready(self):
        reload_database_map()
