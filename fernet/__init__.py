# -*- coding: utf-8 -*-
"""
Fernet security library
Ported from: https://github.com/fernet/fernet-rb
"""

__version__ = '1.0.0'
__author__ = "Scott Persinger"
__contact__ = "scottp@heroku.com"
__docformat__ = "restructuredtext"

# -eof meta-

from .fernet import generate, verifier
from token import Token
from configuration import Configuration
