
from biblishelf_core.conf.register import register_callback


def test():
    print("test_ register call back")

register_callback("generate", test)

from .hook import *