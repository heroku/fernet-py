__author__ = 'spersinger'
import os

from M2Crypto.EVP import Cipher, HMAC

class Encryption:
    AES_BLOCK_SIZE = 16
    DECODE = 0
    ENCODE = 1

    @staticmethod
    def encrypt(message = None, key = None, iv = None):
        if iv is None:
            iv = os.urandom(16)

        message = message.encode('utf8')
        cipher = Cipher(alg='aes_128_cbc', key=key, iv=iv, op=Encryption.ENCODE)
        return (cipher.update(message) + cipher.final(), iv)

    @staticmethod
    def decrypt(ciphertext = None, key = None, iv = None):
        decipher = Cipher(alg='aes_128_cbc', key=key, iv=iv, op=Encryption.DECODE)
        return decipher.update(ciphertext) + decipher.final()

    @staticmethod
    def hmac_digest(key, bytes):
        hmac = HMAC(key, 'sha256')
        hmac.update(bytes)
        return hmac.digest()
