# -*- coding: utf8 -*-
# __author__ = 'spersinger'

import base64

class Secret:
    class InvalidSecret(RuntimeError): pass

    def __init__(self, secret):
        if len(secret) == 32: # broken if secret uses multi-byte chars
            self.secret = secret
        else:
            try:
                self.secret = base64.urlsafe_b64decode(secret.encode('utf8'))
            except TypeError:
                self.secret = base64.b64decode(secret)
            if len(self.secret) != 32:
                raise Secret.InvalidSecret("Secret must be 32 bytes, instead got %d" % len(self.secret))

    @property
    def encryption_key(self):
        return self.secret[16:]

    @property
    def signing_key(self):
        return self.secret[0:16]

    def __repr__(self):
        return "<fernet.Secret [masked]>"

    def __unicode__(self):
        return repr(self)

    def __str__(self):
        return repr(self)
