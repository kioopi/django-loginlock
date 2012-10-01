import sys
from django.http import HttpResponse
from django.shortcuts import render

from models import LoginCandidate
from loginlock.nullcandidate import NullCandidate

from django.conf import settings

# settings defaults
USERNAME_FIELD_NAME = 'username'
LOGIN_VIEWS = ['django.contrib.auth.view.login']
LOCKED_TEMPLATE = None

# TODO: string should be in settings or locker and localized
LOCK_MESSAGE = "Account is locked"


class LoginLocker(object):
    """
    This class holds the main functionality of loginlock.  This is just a
    collection of functions in order to make it possible alter functionality via
    subclassing.
    """
    def track_login_attempt(self, request, candidate=False):
        """
        Takes a request object (with POST-data to log-in a user) and
        creates a model-instance to record the login-attempt.
        """
        candidate = candidate or self.get_candidate(request)

        if not request.user.is_authenticated() and request.method == 'POST':
            candidate.track_attempt()

        return candidate

    def is_locked(self, request):
        """
        Takes a request object (ideally after a post to a login-view)
        and returns True if the username/ip-combination is locked.
        """
        username = self.get_username(request)
        if not username:
            return False

        candidate = self.get_candidate(request, username)

        return candidate.is_locked()

    def get_candidate(self, request, username=None):
        username = username or self.get_username(request)
        ip_address = self.get_ip_address(request)

        # in case there is no chance for a request to be locked,
        # return a NullObject-Candidate that is always unlocked.
        # Does not hit the DB.
        if not request.method == 'POST' or username is None:
            return NullCandidate()

        candidate, was_created = LoginCandidate.objects.get_or_create(
                                       username=username, ip_address=ip_address)
        return candidate

    def get_username(self, request):
        fieldname = str(getattr(settings, 'LOGINLOCK_USERNAME_FIELD_NAME',
                                                        USERNAME_FIELD_NAME))

        return request.POST.get(fieldname, None)

    def get_ip_address(self, request):
        return request.META.get('REMOTE_ADDR', '')

    def reset_attempts(self, user, request):
        candidate = self.get_candidate(request, user.username)

        candidate.attempt_count = 0
        candidate.save()

    def get_login_views(self):
        views = getattr(settings, 'LOGINLOCK_LOGIN_VIEWS', LOGIN_VIEWS)

        return map(_get_callable, views)

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
        """ Takes a view function and decorates it to... """

        if hasattr(login_func, '__LOGINLOCK_DECORATOR__'):
            return login_func

        def decorated_view(request, *args, **kwargs):
            if request.method == 'POST':
                candidate = self.get_candidate(request)
                if candidate.is_locked():
                    return self.locked_response(request)

                response = login_func(request, *args, **kwargs)
                self.track_login_attempt(request, candidate)
                return response

            return login_func(request, *args, **kwargs)

        decorated_view.__LOGINLOCK_DECORATOR__ = True

        return decorated_view

    def locked_response(self, request):
        template = getattr(settings, 'LOGINLOCK_LOCKED_TEMPLATE',
                                                       LOCKED_TEMPLATE)
        if template:
            return render(request, template, status=403)
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
