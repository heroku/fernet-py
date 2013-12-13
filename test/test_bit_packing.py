__author__ = 'spersinger'
import unittest

from should_dsl import should
import test_helper

import fernet
from fernet.bit_packing import BitPacking

class TestBitPacking(unittest.TestCase):
    VALUE_TO_BYTES = {
        0x0000000000000000 : [ 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
        0x00000000000000FF : [ 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF ],
        0x000000FF00000000 : [ 0x00, 0x00, 0x00, 0xFF, 0x00, 0x00, 0x00, 0x00 ],
        0x00000000FF000000 : [ 0x00, 0x00, 0x00, 0x00, 0xFF, 0x00, 0x00, 0x00 ],
        0xFF00000000000000 : [ 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
        0xFFFFFFFFFFFFFFFF : [ 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF ]
    }

    def pretty(self, bytea):
        return "".join("0x{0:x}".format(b) for b in bytea)

    def bytestr(self, bytea):
        return "".join([chr(b) for b in bytea])

    def test_it_encodes_and_decodes_properly(self):
        for value, bytes in TestBitPacking.VALUE_TO_BYTES.iteritems():
            pretty_bytes = self.pretty(bytes).rjust(20)
            bytestr = self.bytestr(bytes)
            BitPacking.pack_int64_bigendian(value) |should| equal_to(bytestr)

            BitPacking.unpack_int64_bigendian(bytestr) |should| equal_to(value)

if __name__ == '__main__':
    unittest.main()
