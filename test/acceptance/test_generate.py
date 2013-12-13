# -*- coding: utf8 -*-
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

from fernet.generator import Generator

class TestGeneratorSpec(unittest.TestCase):
    def test_it_generates_tokens_according_to_the_spec(self):
        path = os.path.join(os.path.dirname(__file__), "../fernet-spec/generate.json")
        generate_json = json.loads(open(path).read())

        for packet in generate_json:
            dt = parse(packet['now'])
            now = long(time.mktime(dt.timetuple())) - 3600
            #print "Now: %ld" % now
            #print "Expected: %s" % packet['token']

            generator = Generator(secret   = packet['secret'],
                                  message  = packet['src'],
                                  iv       = "".join(map(chr, packet['iv'])),
                                  now      = now)
            generator.generate() |should| equal_to(packet['token'])


if __name__ == '__main__':
    unittest.main()
