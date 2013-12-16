__author__ = 'spersinger'
import os

try:
    import M2Crypto
    from M2Crypto.EVP import Cipher, HMAC
except ImportError:
    # Fall back to pycrypto
    from Crypto.Cipher import AES
    from Crypto.Hash import SHA256
    from Crypto.Hash.HMAC import HMAC


class Encryption:
    AES_BLOCK_SIZE = 16
    DECODE = 0
    ENCODE = 1

    @staticmethod
    def encrypt(message = None, key = None, iv = None):
        if iv is None:
            iv = os.urandom(16)

        message = message.encode('utf8')
        if 'M2Crypto' in globals():
            return Encryption.m2crypto_encrypt(message, key, iv)
        else:
            return Encryption.pycrypto_encrypt(message, key, iv)

    @staticmethod
    def decrypt(ciphertext = None, key = None, iv = None):
        if 'M2Crypto' in globals():
            return Encryption.m2crypto_decrypt(ciphertext, key, iv)
        else:
            return Encryption.pycrypto_decrypt(ciphertext, key, iv)

    @staticmethod
    def hmac_digest(key, bytes):
        if 'M2Crypto' in globals():
            return Encryption.m2crypto_hmac_digest(key, bytes)
        else:
            return Encryption.pycrypto_hmac_digest(key, bytes)


    # M2Crypto

    @staticmethod
    def m2crypto_encrypt(message, key, iv):
        cipher = Cipher(alg='aes_128_cbc', key=key, iv=iv, op=Encryption.ENCODE)
        return (cipher.update(message) + cipher.final(), iv)

    @staticmethod
    def m2crypto_decrypt(ciphertext, key, iv):
        decipher = Cipher(alg='aes_128_cbc', key=key, iv=iv, op=Encryption.DECODE)
        return decipher.update(ciphertext) + decipher.final()

    @staticmethod
    def m2crypto_hmac_digest(key, bytes):
        hmac = HMAC(key, 'sha256')
        hmac.update(bytes)
        return hmac.digest()

    # Pycrypto

    @staticmethod
    def pycrypto_encrypt(message, key, iv):
        BS = 16
        pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
        cipher = AES.new(key=key, mode=AES.MODE_CBC, IV=iv)
        return (cipher.encrypt(pad(message)), iv)

    @staticmethod
    def pycrypto_decrypt(ciphertext, key, iv):
        decipher = AES.new(key=key, mode=AES.MODE_CBC, IV=iv)
        unpad = lambda s : s[0:-ord(s[-1])]
        return unpad(decipher.decrypt(ciphertext))

    @staticmethod
    def pycrypto_hmac_digest(key, bytes):
        hmac = HMAC(key, digestmod = SHA256)
        hmac.update(bytes)
        return hmac.digest()
