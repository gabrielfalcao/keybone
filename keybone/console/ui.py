#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import getpass
import logging

logger = logging.getLogger('keybone')


def get_bool(msg):
    result = ''
    while result.lower() not in ['y', 'n']:
        result = raw_input(u'\n'.join(map(unicode, [msg, '[y/n]'])))

    return result == 'y'


def get_passphrase():
    print "\033[1;30m[if the key doesn't need a password just hit ENTER twice]\033[0m"
    ppw1 = getpass.getpass('passphrase:')
    ppw2 = getpass.getpass('confirmation:')
    if ppw1 == ppw2:
        passphrase = ppw1
    else:
        logger.critical('passwords mismatch')
        raise SystemExit(1)

    return passphrase.strip() or None
