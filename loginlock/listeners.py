import django.contrib.auth.signals as auth_signals
import loginlock.locker

from django.conf import settings as django_settings
Locker = getattr(django_settings, 'LOGINLOCK_LOCKER_CLASS',
                                   loginlock.locker.LoginLocker)


def reset_login_attempts(sender, user, request, **kwargs):
    Locker().reset_attempts(user, request)


def bind_listeners():
    auth_signals.user_logged_in.connect(reset_login_attempts)
