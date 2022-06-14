from django.apps import AppConfig
from django.urls import path, include

class BiblishelfBookConfig(AppConfig):
    name = 'biblishelf_web.apps.plugins.book'
    label = 'biblishelf_book'

    def ready(self):
        from biblishelf_web.urls import urlpatterns
        urlpatterns.insert(
            0,
            path(r'api/', include("biblishelf_web.apps.plugins.book.urls")),
        )