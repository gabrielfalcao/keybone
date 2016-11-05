# -*- coding: utf-8 -*-
from keybone.aes import encrypt
from keybone.aes import decrypt


def test_encryption():
    original = 'foobar' * 1000
    password = 's0m3 aw3s0m3 l33t5p34k'
    encrypted = encrypt(original, password)
    encrypted.should_not.equal(original)
    plain = decrypt(encrypted, password)
    plain.should.equal(original)
