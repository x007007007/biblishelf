from django.db import models


class RepoModel(models.Model):
    uuid = models.UUIDField(unique=True, null=False)
    is_main = models.BooleanField(default=False)
    is_portable = models.BooleanField(default=True)
    media_type = models.CharField(
        choices=(
            ("disc", "disc"),
            ("ssd", "ssd"),
            ("usb-disc", "usb-disc"),
            ("cd", "cd"),
            ("usb-ssd", 'usb-ssd'),
            ("tf/sd", "tf-sd"),
            ("samba", "samba"),
            ("cloud", "cloud")
        ),
        max_length=32
    )
    