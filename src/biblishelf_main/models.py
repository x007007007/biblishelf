from django.db import models

# Create your models here.


class Driver(models.Model):
    name = models.CharField(max_length=128)
    uuid = models.CharField("Volumn", max_length=128)
    type = models.CharField(
        choices=(
            ("Disk", "disk"),
            ("iso/img", "img"),
            ("lfs", "lfs")
        ),
        max_length=32,
        null=True,
        blank=True
    )
    extend_info = models.TextField(
        null=True,
        blank=True
    )
    online_status = models.NullBooleanField(
        null=True,
        blank=True
    )

    def is_online(self):
        """
        :return: bool
        """
        return self.online_status

    def get_path(self):
        pass


class Resource(models.Model):
    size = models.PositiveIntegerField(default=0)
    sha = models.CharField(max_length=150, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    mine_type = models.CharField(max_length=32, null=True, blank=True)
    ed2k_hash = models.CharField(max_length=32, null=True, blank=True)


class ResourceMap(models.Model):
    resource = models.ForeignKey(Resource, related_name="Map", null=True)
    path = models.CharField(max_length=1024)
    driver = models.ForeignKey(Driver, related_name='Resources')
    create_time = models.DateTimeField(null=True, blank=True, help_text="help check out danger file")
    modify_time = models.DateTimeField(null=True, blank=True, help_text="help check out danger file")

    def get_abs_path(self):
        return os.path.join(self.driver.get_path(), self.path)


class ResourceAuthor(models.Model):
    name = models.CharField(max_length=32)


class ExtendResource(models.Model):
    name = models.CharField(max_length=64)
    resource = models.ForeignKey(ResourceMap, null=True)

    class Meta:
        abstract = True

class ConfigWatchArea(models.Model):
    driver = models.ForeignKey(Driver, related_name="WatchAreas")
    path = models.CharField(max_length=1024)