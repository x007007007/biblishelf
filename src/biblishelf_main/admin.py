from django.contrib import admin
from .models import ResourceMap, Repo, ConfigWatchArea, Resource
from django.utils.safestring import mark_safe
from django.core import urlresolvers
# Register your models here.
import os
import re


class ResrouceMapInline(admin.TabularInline):
    model = ResourceMap


class RepoAdmin(admin.ModelAdmin):
    readonly_fields = ('dev_path',)
    list_display = ('name', 'uuid', 'uri', 'fs', 'dev_path', 'last_online_time')

    def action_refresh_mount_point(self, request, queryset):
        Repo.refresh_mount_db()

    actions = (action_refresh_mount_point,)


class ResourceMapAdmin(admin.ModelAdmin):
    readonly_fields = ('path',)
    list_display = ('path',)
    search_fields = ('path',)
    list_filter = ('repo',)


class ConfigWatchAreaAdmin(admin.ModelAdmin):

    list_display = ('repo', 'path')
    list_filter = ('repo',)


class ResourceAdmin(admin.ModelAdmin):
    readonly_fields = ('size', 'sha', 'md5', 'ed2k_hash', 'mine_type', 'show_all_resource_path')
    search_fields = ('name', 'sha', 'mine_type')
    list_display = ('name', 'sha', 'size')
    list_filter = ('mine_type',)

    def show_all_resource_path(self, obj):
        rm_list = []
        for rm in obj.Map.all():
            print(rm)
            change_url = urlresolvers.reverse('admin:biblishelf_main_resourcemap_change', args=(rm.pk,))
            rm_list.append(
                '<a href="{}" tager="_blank">path:{}</a>'.format(change_url, rm.get_abs_path())
            )
        return mark_safe("<br />".join(rm_list))

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
admin.site.register(Repo, RepoAdmin)
admin.site.register(ConfigWatchArea, ConfigWatchAreaAdmin)
admin.site.register(Resource, ResourceAdmin)