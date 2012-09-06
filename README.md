#Django Loginlock

Another Django App that prevents repeated login attempts.

Loginlock blocks attempts on a username+ip base.

## Installation

* Add 'loginlock' to your INSTALLED_APPS.
* Add 'loginlock.middleware.LoginLockMiddleware' to your 
MIDDLEWARE_CLASSES.
* Run _manage.py migrate loginlock_ or _manage.py syncdb_

## Settings

## Customizing
