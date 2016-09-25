from django.utils import six


class FileTypeBase(type):
    def __new__(cls, name, bases, attrs):
        res = super(FileTypeBase, cls).__new__(cls, name, bases, attrs)
        meta = attrs.get("Meta", None)
        if meta and not getattr(meta, "abstract", False):
            res.check_by_description("")
            res.get_meta_type()
        return res


class BaseFileType(six.with_metaclass(FileTypeBase)):
    class Meta:
        abstract = True

    resource = None

    @classmethod
    def check_by_description(cls, description):
        """
        :param description: from pymagic description string
        :return: bool
        """
        raise NotImplementedError("Your Type:{} Don't implement check_by_description".format(cls.__name__))

    @classmethod
    def get_meta_type(cls):
        """
        :return: a list of handle meta type
        """
        raise NotImplementedError("")

    def init(self, fp, resource):
        raise NotImplementedError("")