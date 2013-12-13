__author__ = 'spersinger'

import unittest
import base64
import time

from should_dsl import should
import test_helper

from fernet.token import Token
from fernet.encryption import Encryption

class TestToken(unittest.TestCase):
    def setUp(self):
        self.secret = 'odN/0Yu+Pwp3oIvvG8OiE5w4LsLrqfWYRb3knQtSyKI='

    def test_it_is_invalid_with_a_bad_MAC_signature(self):
        generated = Token.generate(secret= self.secret,
                                       message='hello')

        def bogus_hmac(key, bytes):
            return "1" * 32

        Encryption.__dict__['hmac_digest'] = staticmethod(bogus_hmac)

        token = Token(str(generated), secret = self.secret)
        token.valid() |should| be(False)

        token.find_error('signature') |should| include('does not match')


    def test_it_is_invalid_if_too_old(self):
        generated = Token.generate(secret=self.secret,
                                       message='hello',
                                       now=long(time.time()) - 61)
        token = Token(str(generated), enforce_ttl=True,
                                              ttl=60,
                                              secret=self.secret)
        token.valid() |should| be(False)
        token.find_error('issued_timestamp') |should| include("is too far in the past: token expired")

    def test_it_is_invalid_with_a_large_clock_skew(self):
        generated = Token.generate(secret=self.secret,
                                       message='hello',
                                       now=long(time.time())+61)
        token = Token(str(generated), secret=self.secret)

        token.valid() |should| be(False)
        token.find_error('issued_timestamp') |should| include("is too far in the future")

    def test_it_is_invalid_with_bad_base64(self):
        token = Token('bad', secret=self.secret)

        token.valid() |should| be(False)
        token.find_error('token') |should| include("invalid base64")

    def test_it_is_invalid_with_an_unknown_token_version(self):
        token = Token(base64.urlsafe_b64encode("xxxxxx"), secret=self.secret)

        token.valid() |should| be(False)
        token.find_error('version') |should| include("is unknown")

    def test_message_refuses_to_decrypt_if_invalid(self):
        secret = 'odN/0Yu+Pwp3oIvvG8OiE5w4LsLrqfWYRb3knQtSyKI='

        generated = Token.generate(secret=secret,
                                       message='hello',
                                       now=long(time.time()+61))
        token = Token(str(generated), secret=secret)

        token.valid() |should| be(False)
        with self.assertRaises(Token.InvalidToken):
          token.message()

    def test_it_gives_back_the_original_message_in_plain_text(self):
        token = Token.generate(secret=self.secret,
                                   message='hello')
        token.valid() |should| be(True)
        token.message() |should| equal_to('hello')


if __name__ == '__main__':
    unittest.main()
