__author__ = 'spersinger'
import base64
import time
import struct
import traceback
import pdb

from .bit_packing import BitPacking
from .configuration import Configuration
from .encryption import Encryption
from .secret import Secret

class Token:
    class InvalidToken(ValueError):
        def __init__(self, message):
            super(Token.InvalidToken, self).__init__(message)

    # Internal: the default token version
    DEFAULT_VERSION = 0x80
    # Internal: max allowed clock skew for calculating TTL
    MAX_CLOCK_SKEW  = 60

    def __init__(self, token=None, secret=None, enforce_ttl=None, ttl = None, now = None):
        self.token = token
        self.secret = Secret(secret)
        self.enforce_ttl = enforce_ttl if enforce_ttl is not None else Configuration.enforce_ttl
        self.ttl = ttl if ttl is not None else Configuration.ttl
        self.__now = now
        self.errors = []

    def __unicode__(self):
        return self.token

    def __str__(self):
        return unicode(self)

    def valid(self):
        self.validate()
        return len(self.errors) == 0

    def message(self):
        if self.valid():
            try:
                return Encryption.decrypt(key = self.secret.encryption_key,
                                         ciphertext = self.encrypted_message,
                                         iv = self.iv)
            except Exception, e:
                raise Token.InvalidToken("bad decrypt: %s" % str(e))
        else:
            raise Token.InvalidToken(", ".join(["%s %s" % (key,msg) for key,msg in self.errors]))


    @staticmethod
    def generate(secret=None, message=None, iv=None, now=None):
        if secret is None:
            raise Token.InvalidToken("Secret not provided")

        secretObj = Secret(secret)
        encrypted_message, iv = Encryption.encrypt(
            key = secretObj.encryption_key,
            message = message,
            iv = iv
        )
        issued_timestamp = long(now) if now is not None else long(time.time())

        payload = struct.pack("B", Token.DEFAULT_VERSION) + \
            BitPacking.pack_int64_bigendian(issued_timestamp) + \
            iv + \
            encrypted_message
        mac = Encryption.hmac_digest(secretObj.signing_key, payload)
        return Token(base64.urlsafe_b64encode(payload + mac), secret=secret)

    def __unicode__(self):
        return self.token

    # private

    @property
    def decoded_token(self):
        if not hasattr(self, '__decoded_token'):
            token = self.token
            if isinstance(token, unicode):
                token = token.encode('utf8')
            self.__decoded_token = base64.urlsafe_b64decode(token)
        return self.__decoded_token

    @property
    def version(self):
        return struct.unpack("B", self.decoded_token[0])[0]

    @property
    def received_signature(self):
        dec_token = self.decoded_token
        return dec_token[len(dec_token) - 32:]

    @property
    def issued_timestamp(self):
        return BitPacking.unpack_int64_bigendian(self.decoded_token[1:(1+8)])

    @property
    def iv(self):
        return self.decoded_token[9:(9+16)]

    @property
    def encrypted_message(self):
        return self.decoded_token[25:len(self.decoded_token)-32]

    def validate(self):
        self.errors = []
        if self.valid_base64():
            if self.unknown_token_version():
                self.errors.append(("version", "is unknown"))
            elif self.enforce_ttl == True and not self.issued_recent_enough():
                self.errors.append(("issued_timestamp", "is too far in the past: token expired"))
            else:
                if not self.signatures_match():
                    self.errors.append(("signature", "does not match"))
                if self.unacceptable_clock_skew():
                    self.errors.append(("issued_timestamp", "is too far in the future"))
                if not self.ciphertext_multiple_of_block_size():
                    self.errors.append(("ciphertext", "is not a multiple of block size"))
        else:
            self.errors.append(("token", "invalid base64"))

    @property
    def regenerated_mac(self):
        return Encryption.hmac_digest(self.secret.signing_key, self.signing_blog)

    @property
    def signing_blog(self):
        return struct.pack("B", self.version) + \
                BitPacking.pack_int64_bigendian(self.issued_timestamp) + \
                self.iv + \
                self.encrypted_message

    def valid_base64(self):
        try:
            self.decoded_token
            return True
        except TypeError:
            return False

    def signatures_match(self):
        regenerated_bytes = bytearray(self.regenerated_mac)
        received_bytes    = bytearray(self.received_signature)
        return reduce(
            lambda accum, nextbyte: accum | nextbyte ^  regenerated_bytes.pop(0),
            received_bytes, 0) == 0

    def issued_recent_enough(self):
        good_till = self.issued_timestamp + (self.ttl if self.ttl else 0)
        return good_till >= self.now

    def unacceptable_clock_skew(self):
        return self.issued_timestamp >= (self.now + Token.MAX_CLOCK_SKEW)

    def ciphertext_multiple_of_block_size(self):
        return (len(self.encrypted_message) % Encryption.AES_BLOCK_SIZE) == 0

    def unknown_token_version(self):
        return Token.DEFAULT_VERSION != self.version

    def find_error(self, findKey):
        try:
            return [msg for key, msg in self.errors if key == findKey].pop()
        except IndexError:
            return None

    @property
    def now(self):
        return (self.__now or long(time.time()))

