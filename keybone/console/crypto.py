#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import os
import statvfs
import logging

from keybone.core import KeyBone
from keybone.core import InvalidRecipient
from keybone.core import InvalidKeyError

from keybone.console.ui import get_passphrase

from keybone.console.base import get_sub_parser_argv


MAX_FILENAME = os.statvfs(os.getcwd())[statvfs.F_NAMEMAX]
logger = logging.getLogger('keybone')


def is_filename(string):
    return len(string) <= MAX_FILENAME and os.sep in string


def execute_command_encrypt():
    from keybone.console.parsers.encrypt import parser

    args = parser.parse_args(get_sub_parser_argv())

    gee = KeyBone()
    if is_filename(args.plaintext):
        if not os.path.exists(args.plaintext):
            msg = 'given encryption source appears to be a file but its path does not exist: {0}'
            logger.error(msg.format(args.plaintext))
            raise SystemExit(1)

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

    if is_filename(args.ciphertext):
        if not os.path.exists(args.ciphertext):
            msg = 'given decryption source appears to be a file but its path does not exist: {0}'
            logger.error(msg.format(args.ciphertext))
            raise SystemExit(1)

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
    status, trust_level = gee.verify(args.signed_data)

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
    signed = gee.sign(args.recipient, args.data, passphrase)

    if signed:
        print signed
