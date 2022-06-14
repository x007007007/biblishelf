import threading
import django.core.handlers
db_config = threading.local()
from django.db import connections
from .signals import db_config_loss_signal
from django.http import HttpResponseNotFound


class DynDBRouterByURLConfigMiddleWare():
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if 'db_key' in view_kwargs:
            db_key = view_kwargs['db_key']
            if db_key not in connections.databases:
                db_config_loss_signal.send(sender=DynDBRouterByURLConfigMiddleWare, db_key=db_key)
            if db_key not in connections.databases:
                return HttpResponseNotFound()
            db_config.db_key = db_key
        else:
            db_config.db_key = 'default'
        return view_func(request, *view_args, **view_kwargs)


