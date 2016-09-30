#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from keybone.core import KeyBone
from keybone.core import InvalidRecipient
from keybone.core import InvalidKeyError

from keybone.console.ui import get_passphrase

from keybone.console.base import get_sub_parser_argv


logger = logging.getLogger('keybone')


def execute_command_encrypt():
    from keybone.console.parsers.encrypt import parser

    args = parser.parse_args(get_sub_parser_argv())
    gee = KeyBone()
    try:
        print gee.encrypt(args.recipient, args.plaintext, args.sign_from)
    except InvalidRecipient as e:
        logger.error("failed to encrypt: {0}".format(e))
        raise SystemExit(1)


def execute_command_decrypt():
    from keybone.console.parsers.decrypt import parser

    args = parser.parse_args(get_sub_parser_argv())
    gee = KeyBone()
    if args.secret:
        passphrase = args.secret
    else:
        passphrase = get_passphrase()

    try:
        plaintext = gee.decrypt(args.ciphertext, passphrase)
    except InvalidKeyError as e:
        logger.error("failed to decrypt: {0}".format(e))
        raise SystemExit(1)

    if plaintext:
        print plaintext


def execute_command_verify():
    from keybone.console.parsers.verify import parser

    args = parser.parse_args(get_sub_parser_argv())
    gee = KeyBone()
    status, trust_level = gee.verify(args.signed_data)

    if 'signature valid' not in status.strip():
        print status, trust_level
        raise SystemExit(1)

    print ": ".join([status, trust_level])


def execute_command_sign():
    from keybone.console.parsers.sign import parser

    args = parser.parse_args(get_sub_parser_argv())
    gee = KeyBone()
    signed = gee.sign(args.recipient, args.data, args.secret)

    if signed:
        print signed
