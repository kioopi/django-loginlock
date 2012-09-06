# -*- coding: utf-8 -*-

from version import __version__

# Bind a listener to remove locks of a username/ip-pair
# in case of successfull login.
import listeners
listeners.bind_listeners()
