import sys
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic.simple import direct_to_template

from models import LoginCandidate

from settings import LOGINLOCK_USERNAME_FIELD_NAME, LOGINLOCK_LOGIN_VIEWS, LOGINLOCK_LOCKED_TEMPLATE

LOCK_MESSAGE = "Account is locked"


class LoginLocker(object):
    """
    This class holds the main functionality of loginlock.  This is not just a
    collection of functions in order to make it possible alter functionality via
    subclassing.
    """
    def track_login_attempt(self, request):
        """
        Takes a request object (with POST-data to log-in a user) and
        creates a model-instance to record the login-attempt.
        """
        username = self.get_username(request)
        ip_address = self.get_ip_address(request)

        print 'tracking ', username, ip_address

        candidate, was_created = LoginCandidate.objects.get_or_create(
                                       username=username, ip_address=ip_address)
        candidate.attempt_count += 1
        candidate.save()
        return candidate

    def is_locked(self, request):
        """
        Takes a request object (ideally after a post to a login-view)
        and returns True if the username/ip-combination is locked.
        """
        username = self.get_username(request)
        if not username:
            return False
        ip_address = self.get_ip_address(request)

        print 'check lock ', username, ip_address

        candidate, was_created = LoginCandidate.objects.get_or_create(
                                       username=username, ip_address=ip_address)

        return candidate.is_locked()

    def get_username(self, request):
        return request.POST.get(LOGINLOCK_USERNAME_FIELD_NAME, None)

    def get_ip_address(self, request):
        return request.META.get('REMOTE_ADDR', '')

    def reset_attempts(self, user, request):
        username = user.username
        ip_address = self.get_ip_address(request)

        candidate, was_created = LoginCandidate.objects.get_or_create(
                                      username=username, ip_address=ip_address)

        candidate.attempt_count = 0
        candidate.save()

    def get_login_views(self):
        return map(_get_callable, LOGINLOCK_LOGIN_VIEWS)

    def decorate_views(self):
        """
        Applies the wrapper to watch for login attempts to a list of views
        """
        for view in self.get_login_views():
            self.decorate_view(view)

    def decorate_view(self, view):
        module_name = view.__module__
        __import__(module_name)
        setattr(sys.modules[module_name], view.__name__,
                self.watch_login_attempts(view))

    def watch_login_attempts(self, login_func):
        """ Takes a view function and decorates it to..."""

        if hasattr(login_func, '__LOGINLOCK_DECORATOR__'):
            return login_func

        def decorated_view(request, *args, **kwargs):
            if request.method == 'POST':
                if self.track_login_attempt(request).is_locked():
                    return self.locked_response(request)

            return login_func(request, *args, **kwargs)

        decorated_view.__LOGINLOCK_DECORATOR__ = True

        return decorated_view

    def locked_response(self, request):
        if LOGINLOCK_LOCKED_TEMPLATE:
            return direct_to_template(request,
                                      template=LOGINLOCK_LOCKED_TEMPLATE,
                                      status=403)
        return HttpResponse(LOCK_MESSAGE, status=403)


def _get_module_and_func(modulestring):
    parts = modulestring.split('.')
    module = '.'.join(parts[:-1])
    func = parts[-1]
    return (module, func)


def _get_callable(dotpath):
    modname, funcname = _get_module_and_func(dotpath)
    __import__(modname)
    return getattr(sys.modules[modname], funcname)
