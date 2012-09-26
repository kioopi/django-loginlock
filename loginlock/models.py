try:
    from django.utils import timezone as datetime
except ImportError:
    from datetime import datetime

from django.db import models
from loginlock.settings import LOGINLOCK_MAX_TRIES, LOGINLOCK_LOCK_TIMEOUT


class LoginCandidate(models.Model):
    username = models.CharField('Username', max_length=255)
    ip_address = models.IPAddressField('IP Address', null=True)
    attempt_count = models.PositiveIntegerField('attempt_count', default=0)
    last_attempt_at = models.DateTimeField('Last attempt', auto_now=True)

    def track_attempt(self):
        self.attempt_count += 1
        self.save()

    def tried_too_often(self):
        return self.attempt_count >= LOGINLOCK_MAX_TRIES
    tried_too_often.boolean = True

    def lock_timed_out(self, timestamp=None):
        """ Returns True if the Candidate is locked out.
            Takes an optional timestap for a point in time to check
            against. Defaults to now."""
        if not timestamp:
            timestamp = datetime.now()
        return timestamp > self.last_attempt_at + LOGINLOCK_LOCK_TIMEOUT
    lock_timed_out.boolean = True

    def is_locked(self, timestamp=None):
        return self.tried_too_often() and not self.lock_timed_out(timestamp)
    is_locked.boolean = True

    def __unicode__(self):
        lock = 'locked' if self.is_locked() else 'not locked'
        return u'%d login attempts by %s as of %s: %s.' % (
                    self.attempt_count, self.username, self.last_attempt_at, lock)

    class Meta:
        ordering = ['-last_attempt_at']
        unique_together = (("username", "ip_address"),)
