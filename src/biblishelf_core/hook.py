from six import with_metaclass
import collections
from biblishelf_core.conf.repo import current_repo


class HookerError(Exception):
    pass


class HookerMeta(type):
    abstract = True

    hooker = collections.OrderedDict()

    def __new__(self, name, classes, attrs):
        cmdclass = super(HookerMeta, self).__new__(self, name, classes, attrs)
        if not attrs.get('abstract', False):
            hook_point = getattr(cmdclass, 'point', None)
            if hook_point is None:
                raise HookerError("need hooker point")
            self.hooker[hook_point] = cmdclass
        return cmdclass

    @classmethod
    def get_hooker_by_name(cls, name):
        return cls.hooker.get(name)

class BaseHooker(with_metaclass(HookerMeta)):
    @property
    def point(self):
        raise NotImplementedError

    @classmethod
    def get_hooker(cls):
        return HookerMeta.hooker.get(cls.point)


class ScanHooker(BaseHooker):
    point = 'scan'
    resource = None


    def __init__(self, resource):
        self.repo =  current_repo
        print('hooker', current_repo)
        self.resource = resource

    def get_fragment(self, fragment, size, number, total):
        raise NotImplementedError

    def get_fp(self, fp):
        raise NotImplementedError
