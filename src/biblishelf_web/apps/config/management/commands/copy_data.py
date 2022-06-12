from django.core.management.base import BaseCommand, CommandError
from biblishelf_web.apps.main.models import (
    RepoModel,
    ResourceModel,
)
import os
import psutil
import json
import warnings
import uuid
import datetime
import pytz


class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        raise NotImplemented
