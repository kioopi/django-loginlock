from django.conf import settings as django_settings
import loginlock.locker

Locker = getattr(django_settings, 'LOGINLOCK_LOCKER_CLASS',
                                  loginlock.locker.LoginLocker)


class LoginLockMiddleware(object):
    def __init__(self, *args, **kwargs):
        locker = Locker()
        locker.decorate_views()
