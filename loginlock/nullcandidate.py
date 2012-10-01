class NullCandidate(object):
    """
        A null object for LoginCandidate.
        Used in situation when there is supposed to no lock whatsoever.
        This doesn't hit the database and is always unlocked.
    """
    def track_attempt(self):
        pass

    def save(self):
        pass

    def tried_too_often(self):
        return False
    tried_too_often.boolean = True

    def lock_timed_out(self, timestamp=None):
        return False
    lock_timed_out.boolean = True

    def is_locked(self, timestamp=None):
        return False
    is_locked.boolean = True

    def __unicode__(self):
        return u'LoginCandidate NullObject'
