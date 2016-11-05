#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import logging

from keybone.lib.core import KeyBone
from keybone.lib.core import InvalidRecipient
from keybone.lib.core import InvalidKeyError

from keybone.console.ui import get_passphrase

from keybone.console.base import get_sub_parser_argv
from keybone.console.util import is_file_and_exists

logger = logging.getLogger('keybone')


def execute_command_encrypt():
    from keybone.console.parsers.encrypt import parser

    args = parser.parse_args(get_sub_parser_argv())

    gee = KeyBone()
    if is_file_and_exists(args.plaintext):
        plaintext = io.open(args.plaintext, 'rb').read()

    else:
        plaintext = args.plaintext

    try:
        print gee.encrypt(args.recipient, plaintext, sign_from=args.sign_from)
    except InvalidRecipient as e:
        logger.error("failed to encrypt: {0}".format(e))
        raise SystemExit(1)


def execute_command_decrypt():
    from keybone.console.parsers.decrypt import parser

    args = parser.parse_args(get_sub_parser_argv())
    gee = KeyBone()
    if args.secret:
        passphrase = args.secret
    elif args.no_secret:
        passphrase = None
    else:
        passphrase = get_passphrase()

    if is_file_and_exists(args.ciphertext):
        ciphertext = io.open(args.ciphertext, 'rb').read()

    else:
        ciphertext = args.ciphertext

    try:
        plaintext = gee.decrypt(ciphertext, passphrase)

    except InvalidKeyError as e:
        logger.error("failed to decrypt: {0}".format(e))
        raise SystemExit(1)

    if plaintext:
        print plaintext


def execute_command_verify():
    from keybone.console.parsers.verify import parser

    args = parser.parse_args(get_sub_parser_argv())
    gee = KeyBone()

    if is_file_and_exists(args.signed_data):
        signed_data = io.open(args.signed_data, 'rb').read()

    else:
        signed_data = args.signed_data

    result = gee.verify(signed_data)
    if not result:
        print "Failed to verify"
        raise SystemExit(1)

    status, trust_level = result
    if 'signature valid' not in status.strip():
        print status, trust_level
        raise SystemExit(1)

    print ": ".join([status, trust_level])


def execute_command_sign():
    from keybone.console.parsers.sign import parser

    args = parser.parse_args(get_sub_parser_argv())
    if args.secret:
        passphrase = args.secret
    elif args.no_secret:
        passphrase = None
    else:
        passphrase = get_passphrase()

    gee = KeyBone()

    if is_file_and_exists(args.data):
        data = io.open(args.data, 'rb').read()

    else:
        data = args.data

    signed = gee.sign(args.recipient, data, passphrase)

    if signed:
        print signed
