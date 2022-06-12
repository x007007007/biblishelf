import threading
import django.core.handlers
db_config = threading.local()


class AdminRouterConfigMiddleWare():
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if 'dbid' in view_kwargs:
            dbid = view_kwargs.pop('dbid')
            db_config.dbid = dbid

        return view_func(request, *view_args, **view_kwargs)
        