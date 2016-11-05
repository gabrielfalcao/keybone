#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytz
from datetime import datetime

from Crypto import Random
from Crypto.Cipher import AES

from cryptography.hazmat.primitives.hashes import SHA256 as CRYPO_SHA256
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend


iterations = 5000
# http://eli.thegreenplace.net/2010/06/25/aes-encryption-of-files-in-python-with-pycrypto
# http://bityard.blogspot.com/2010/10/symmetric-encryption-with-pycrypto-part.html
# https://moxie.org/blog/the-cryptographic-doom-principle/
BLOCK_SIZE = 32
IV_SIZE = 16
LINE_WRAP = 80


def wrap_lines(string, limit=LINE_WRAP):
    string = string.encode('rot13')
    return b"\n".join([string[i:i + limit] for i in range(0, len(string), limit)])


def unwrap_lines(string):
    return b"".join(string.splitlines()).decode('rot13')


def get_key_and_iv(passphrase, iv=None):
    IV = iv or Random.new().read(IV_SIZE)
    backend = default_backend()
    kdf = PBKDF2HMAC(
        algorithm=CRYPO_SHA256(),
        length=BLOCK_SIZE,
        salt=IV,
        iterations=iterations,
        backend=backend)

    key = kdf.derive(passphrase)

    return key, IV


def get_aes_cbc(passphrase, iv=None):
    key, iv = get_key_and_iv(passphrase, iv)
    aes = AES.new(key, AES.MODE_CBC, iv)
    return aes


def encrypt(plaintext, passphrase):
    aes = get_aes_cbc(passphrase)
    padded = pad(plaintext.encode('base64'))
    return (aes.IV + aes.encrypt(padded)).encode('hex').encode('bz2').encode('base64')


def decrypt(ciphertext, passphrase):
    unwrapped = ciphertext.decode('base64').decode('bz2').decode('hex')
    iv = unwrapped[:IV_SIZE]
    encrypted = unwrapped[IV_SIZE:]
    aes = get_aes_cbc(passphrase, iv=iv)
    padded = aes.decrypt(encrypted)
    unpadded = unpad(padded)
    plaintext = unpadded.decode('base64')
    return plaintext


def pad(string, blocksize=BLOCK_SIZE):
    length = len(string)
    padmax = blocksize - length
    padsize = padmax % blocksize
    padbyte = chr(padsize)
    return string + (padsize * padbyte)


def unpad(string, blocksize=BLOCK_SIZE):
    length = len(string)
    return string[:-ord(string[length - 1:])]


letter = """Hey Torvalds, it seems like someone exploited short-id collisions
on PGP keys and could be pushing malware to the kernel mainstream

Check this out: https://pgp.mit.edu/pks/lookup?search=0x00411886&op=index

Search Result of 0x00411886 is:
Fake Linus Torvalds: 0F6A 1465 32D8 69AE E438  F74B 6211 AA3B [0041 1886]
Real Linus Torvalds: ABAF 11C6 5A29 70B1 30AB  E3C4 79BE 3E43 [0041 1886]

Cheers,
Sn0wden

{0}
""".format(datetime.now(tz=pytz.utc).strftime('%B %d, %Y (%z)'))
