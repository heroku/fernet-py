__author__ = 'spersinger'

import sys
import unittest
import os.path
import time
import base64
import json
import time

from should_dsl import should, should_not
from dateutil.parser import parse

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from fernet.verifier import Verifier, Token

class TestVerifySpec(unittest.TestCase):
    def test_it_verifies_tokens_according_to_the_spec(self):
        path = os.path.join(os.path.dirname(__file__), "../fernet-spec/verify.json")
        verify_json = json.loads(open(path).read())

        for packet in verify_json:
            dt = parse(packet['now'])
            now = long(time.mktime(dt.timetuple())) - 3600

            verifier = Verifier(token    = packet['token'],
                                secret   = packet['secret'],
                                now      = now,
                                ttl      = packet['ttl_sec'])

            verifier.message |should| equal_to(packet['src'])

    def test_invalid_tokens(self):
        path = os.path.join(os.path.dirname(__file__), "../fernet-spec/invalid.json")
        invalid_json = json.loads(open(path).read())

        for packet in invalid_json:
            dt = parse(packet['now'])
            now = long(time.mktime(dt.timetuple())) - 3600

            verifier = Verifier(token    = packet['token'],
                                secret   = packet['secret'],
                                now      = now,
                                ttl      = packet['ttl_sec'])
            with self.assertRaises(Token.InvalidToken):
                print("Resulting message: %s" % verifier.message)


if __name__ == '__main__':
    unittest.main()
