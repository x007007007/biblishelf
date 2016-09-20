from django.contrib import admin
from .models import ResourceMap, Driver, ConfigWatchArea, Resource
# Register your models here.
import os, re


class DriverAdmin(admin.ModelAdmin):
    list_display = ('name', 'uuid')


class ResourceMapAdmin(admin.ModelAdmin):
    readonly_fields = ('path',)
    list_display = ('path',)
    search_fields = ('path',)
    list_filter = ('driver',)


class ConfigWatchAreaAdmin(admin.ModelAdmin):
    list_display = ('driver', 'path')
    list_filter = ('driver',)


class ResourceAdmin(admin.ModelAdmin):
    readonly_fields = ('size', 'sha')
    search_fields = ('name', 'sha')
    list_display = ('name', 'sha', 'size')

    def action_get_name(self, request, queryset):
        for r in queryset:
            filenames = set()
            for rm in ResourceMap.objects.filter(resource=r):
                filenames.add(rm.path.split(os.sep)[-1].strip())
            if len(filenames) == 1:
                r.name = filenames.pop()
                r.save(update_fields=('name',))
            else:
                res = {}
                for k in list(filenames):
                    res[k] = 0
                    if re.search("[\u4e00-\u9fa5]+", k):
                        res[k] += 1
                    res[k] += (100 - len(k)) / 100
                for k, v in res.items():
                    if v >= max(res.values()):
                        r.name = k
                        print(k)
                        r.save(update_fields=('name',))

    actions = (action_get_name,)

admin.site.register(ResourceMap, ResourceMapAdmin)
admin.site.register(Driver, DriverAdmin)
admin.site.register(ConfigWatchArea, ConfigWatchAreaAdmin)
admin.site.register(Resource, ResourceAdmin)