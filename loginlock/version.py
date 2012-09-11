# -*- coding: utf-8 -*-

VERSION = (0, 0, 3)

try:
    __version__ = '%s.%s.%s-%s' % VERSION
except TypeError:
    __version__ = '%s.%s.%s' % VERSION
