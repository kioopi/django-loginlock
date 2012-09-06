import datetime
from django.conf import settings as dsettings
# from django.contrib.auth import views as auth_views
# from django.utils.importlib import import_module

# should timezone be used? is there a difference in timedelta
# try:
#     from django.utils import timezone as datetime
# except ImportError:
#     from datetime import datetime


LOGINLOCK_MAX_TRIES = int(getattr(dsettings, 'LOGINLOCK_MAX_TRIES ', 2))
LOGINLOCK_LOCK_TIMEOUT = getattr(dsettings, 'LOGINLOCK_LOCK_TIMEOUT ',
                                            datetime.timedelta(minutes=15))
LOGINLOCK_USERNAME_FIELD_NAME = str(getattr(dsettings,
                                 'LOGINLOCK_USERNAME_FIELD_NAME', 'username'))

LOGINLOCK_LOGIN_VIEWS = getattr(dsettings, 'LOGINLOCK_LOGIN_VIEWS',
                                           ['django.contrib.auth.view.login'])

LOGINLOCK_LOCKED_TEMPLATE = getattr(dsettings, 'LOGINLOCK_LOCKED_TEMPLATE',
                                                                         None)

# the stuff above is just too ugly. there has to be a better way.
# this below does not work
# def defsetting(name, default, cast=lambda x: x):
#     globals()[name] = cast(getattr(dsettings, name, default))

# [defsetting(*setting) for setting in [
#     ('LOGINLOCK_MAX_TRIES ', 5, int),
#     ('LOGINLOCK_LOCK_TIMEOUT ', datetime.timedelta(minutes=15)),
#     ('LOGINLOCK_USERNAME_FIELD_NAME', 'username', str),
#     ('LOGINLOCK_LOGIN_VIEWS', [auth_views.login]),
# ]]
