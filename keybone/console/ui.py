#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals


def get_bool(msg):
    result = ''
    while result.lower() not in ['y', 'n']:
        result = raw_input(u'\n'.join(map(unicode, [msg, '[y/n]'])))

    return result == 'y'
