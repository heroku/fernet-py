__author__ = 'spersinger'

import unittest
import base64

from should_dsl import should
import test_helper

from fernet.secret import Secret

class TestSecret(unittest.TestCase):
    def test_it_can_resolve_a_URL_safe_base64_encoded_32_byte_string(self):
        self.resolves_input(base64.urlsafe_b64encode("A"*16 + "B"*16))

    def test_it_can_resolve_a_base64_encoded_32_byte_string(self):
        self.resolves_input(base64.b64encode("A"*16 + "B"*16))

    def test_it_can_resolve_a_32_byte_string_without_encoding(self):
        self.resolves_input("A"*16 + "B"*16)

    def test_it_fails_loudly_when_an_invalid_secret_is_provided(self):
        secret = base64.urlsafe_b64encode("bad")
        with self.assertRaises(Secret.InvalidSecret):
            Secret(secret)

    def resolves_input(self, input):
        secret = Secret(input)

        secret.signing_key |should| equal_to("A"*16)
        secret.encryption_key |should| equal_to("B"*16)

if __name__ == '__main__':
    unittest.main()
