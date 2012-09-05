import datetime
from django.conf import settings as django_settings
# from django.contrib.auth import views as auth_views
# from django.utils.importlib import import_module

# should timezone be used? is there a difference in timedelta
# try:
#     from django.utils import timezone as datetime
# except ImportError:
#     from datetime import datetime


LOGINLOCK_MAX_TRIES = int(getattr(django_settings, 'LOGINLOCK_MAX_TRIES ', 2))
LOGINLOCK_LOCK_TIMEOUT = getattr(django_settings, 'LOGINLOCK_LOCK_TIMEOUT ',
                                            datetime.timedelta(minutes=15))
LOGINLOCK_USERNAME_FIELD_NAME = str(getattr(django_settings,
                                 'LOGINLOCK_USERNAME_FIELD_NAME', 'username'))

LOGINLOCK_LOGIN_VIEWS = getattr(django_settings, 'LOGINLOCK_LOGIN_VIEWS',
                                           ['django.contrib.auth.view.login'])

# the stuff above is just too ugly. there has to be a better way.
# this below does not work
# def defsetting(name, default, cast=lambda x: x):
#     globals()[name] = cast(getattr(django_settings, name, default))

# [defsetting(*setting) for setting in [
#     ('LOGINLOCK_MAX_TRIES ', 5, int),
#     ('LOGINLOCK_LOCK_TIMEOUT ', datetime.timedelta(minutes=15)),
#     ('LOGINLOCK_USERNAME_FIELD_NAME', 'username', str),
#     ('LOGINLOCK_LOGIN_VIEWS', [auth_views.login]),
# ]]
