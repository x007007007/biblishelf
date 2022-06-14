from django.db.models.fields.files import ImageFile
from django.db.models.fields.files import ImageField
from django.db.models.fields.files import FieldFile
from django.db.models.fields.files import FileDescriptor
from django.db.models.fields.files import _
from biblishelf_web.apps.main.storage import PortableStorage

class PortableImageFileDescriptor(FileDescriptor):
    """
    Just like the FileDescriptor, but for ImageFields. The only difference is
    assigning the width/height to the width_field/height_field, if appropriate.
    """

    def __set__(self, instance, value):
        previous_file = instance.__dict__.get(self.field.attname)
        super().__set__(instance, value)

        # To prevent recalculating image dimensions when we are instantiating
        # an object from the database (bug #11084), only update dimensions if
        # the field had a value before this assignment.  Since the default
        # value for FileField subclasses is an instance of field.attr_class,
        # previous_file will only be None when we are called from
        # Model.__init__().  The ImageField.update_dimension_fields method
        # hooked up to the post_init signal handles the Model.__init__() cases.
        # Assignment happening outside of Model.__init__() will trigger the
        # update right here.
        if previous_file is not None:
            self.field.update_dimension_fields(instance, force=True)


class PortableImageFieldFile(ImageFile, FieldFile):
    def delete(self, save=True):
        # Clear the image dimensions cache
        if hasattr(self, "_dimensions_cache"):
            del self._dimensions_cache
        super().delete(save)

    def save(self, name, content, save=True, using=None):
        name = self.field.generate_filename(self.instance, name)
        self.name = self.storage.save(name, content, max_length=self.field.max_length, using=using)
        setattr(self.instance, self.field.attname, self.name)
        self._committed = True

        # Save the object because it has changed, unless save is False
        if save:
            self.instance.save(using=using)

class PortableImageField(ImageField):
    attr_class = PortableImageFieldFile
    descriptor_class = PortableImageFileDescriptor
    description = _("PortableImage")

    def __init__(self, *args, **kwargs):
        kwargs['storage'] = PortableStorage
        super(PortableImageField, self).__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        from biblishelf_web.apps.plugins.book.models import BookModel
        assert isinstance(model_instance, BookModel)
        file = getattr(model_instance, self.attname)
        if file and not file._committed:
            # Commit the file to storage prior to saving the model
            file.save(file.name, file.file, save=False, using=model_instance._state.db)
        return file

    def save(self, name, content, save=True, using=None):
        name = self.field.generate_filename(self.instance, name)
        self.name = self.storage.save(name, content, max_length=self.field.max_length, using=using)
        setattr(self.instance, self.field.attname, self.name)
        self._committed = True

        # Save the object because it has changed, unless save is False
        if save:
            self.instance.save(using=using)