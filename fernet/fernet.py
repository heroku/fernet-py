__author__ = 'spersinger'

from .generator import Generator
from .verifier import Verifier

def generate(secret = None, message="", iv=None, now=None):
    """Public: generates a fernet token
    Returns the fernet token as a string.
    :param secret
    :param message
    :param options
    """
    return Generator(secret=secret, message=message, iv=iv, now=now).generate()

def verifier(secret, token, enforce_ttl=None, ttl=None, now=None):
    return Verifier(secret=secret, token=token, enforce_ttl = enforce_ttl, ttl=ttl, now=now)