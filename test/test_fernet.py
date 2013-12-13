import sys
import unittest
import os.path
import time
import base64

from should_dsl import should, should_not

import test_helper

import fernet

class TestFernet(unittest.TestCase):
    def setUp(self):
        self.secret = 'JrdICDH6x3M7duQeM8dJEMK4Y5TkBIsYDw1lPy35RiY='
        self.bad_secret = 'badICDH6x3M7duQeM8dJEMK4Y5TkBIsYDw1lPy35RiY='

    def tearDown(self):
        fernet.Configuration.run()

    def test_it_can_verify_tokens_it_generates(self):
        token = fernet.generate(self.secret, 'harold@heroku.com')

        verifier = fernet.verifier(self.secret, token)
        verifier.valid() |should| be(True)
        verifier.message |should| equal_to('harold@heroku.com')


    def test_it_fails_with_a_bad_secret(self):
        token = fernet.generate(self.secret, 'harold@heroku.com')

        verifier = fernet.verifier(self.bad_secret, token)
        verifier.valid() |should| be(False)

        with self.assertRaises(fernet.Token.InvalidToken):
            verifier.message()

    def test_it_fails_if_the_token_is_too_old(self):
        token = fernet.generate(self.secret, 'harold@heroku.com', now = (long(time.time()) - 61))
        verifier = fernet.verifier(self.secret, token)
        verifier.valid() |should| be(False)

    def test_it_can_ignore_ttl_enforcement(self):
        fernet.Configuration.enforce_ttl = True
        token = fernet.generate(self.secret, 'harold@heroku.com')
        verifier = fernet.verifier(self.secret, token, enforce_ttl=False, now=long(time.time()) + 9999)

        verifier.valid() |should| be(True)

    def test_it_can_ignore_ttl_enforcement_via_global_config(self):
        fernet.Configuration.enforce_ttl = False
        token = fernet.generate(self.secret, 'harold@heroku.com')
        verifier = fernet.verifier(self.secret, token, now=long(time.time()) + 9999)

        verifier.valid() |should| be(True)

    def test_it_does_not_send_the_message_in_plain_text(self):
        token = fernet.generate(self.secret, 'password1')

        base64.urlsafe_b64decode(token) |should_not| contain('password1')

    def test_it_allows_overriding_enforce_ttl_on_a_verifier(self):
        fernet.Configuration.enforce_ttl = True
        fernet.Configuration.ttl = 0

        token = fernet.generate(self.secret, 'password1')
        verifier = fernet.verifier(self.secret, token)
        verifier.enforce_ttl = False

        verifier.valid() |should| be(True)
        verifier.message |should| equal_to('password1')


if __name__ == '__main__':
    unittest.main()
