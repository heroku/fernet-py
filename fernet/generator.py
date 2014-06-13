__author__ = 'spersinger'

from .token import Token

class Generator:
    def __init__(self, secret=None, message=None, iv=None, now=None):
        """Internal: Initializes a generator.
        """
        self.secret = secret
        self.message = message
        self.iv = iv
        self.now = now

    def generate(self):
        """Internal: generates a secret token
        """
        message = self.message
        if isinstance(message, unicode):
            message = message.encode('utf8')

        token = Token.generate(secret = self.secret,
                               message=message,
                               iv=self.iv,
                               now=self.now)
        return str(token)

    def __repr__(self):
        return "<fernet.Generator secret=[masked] message=%s>" % self.message

