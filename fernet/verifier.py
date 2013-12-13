__author__ = 'spersinger'

from .token import Token

class Verifier:
    class UnknownTokenVersion(RuntimeError): pass

    def __init__(self, secret=None, token=None, enforce_ttl=None, ttl=None, now=None):
        self.token = Token(token, secret=secret, enforce_ttl=enforce_ttl, ttl=ttl, now=now)

    def valid(self):
        return self.token.valid()

    @property
    def message(self):
        return self.token.message()

    def __repr__(self):
        return "<Fernet::Verifier secret=[masked] token=%s message={%s}" % (self.token, self.message)

    def __unicode__(self):
        return repr(self)

    def __str__(self):
        return unicode(self)
