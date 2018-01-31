# -*- coding: utf-8 -*-
# pylint: disable=unused-import
"""
compatibility support
"""

import sys

if sys.version_info.major == 3:
    if sys.version_info.minor == 4:
        JSONDecodeError = ValueError
    else:
        from json import JSONDecodeError  # NOQA
