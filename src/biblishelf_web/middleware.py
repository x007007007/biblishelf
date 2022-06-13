import threading
import django.core.handlers
db_config = threading.local()


class DynDBRouterByURLConfigMiddleWare():
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if 'db_key' in view_kwargs:
            db_key = view_kwargs['db_key']
            db_config.db_key = db_key
        else:
            db_config.db_key = 'default'
        return view_func(request, *view_args, **view_kwargs)


