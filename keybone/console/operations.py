#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import io
import logging

from keybone import conf
from keybone.util import BackupManager
from keybone.util import get_all_keyring_nodes
from keybone.util import initialize_key_home
from keybone.console.ui import get_bool
from keybone.console.base import get_sub_parser_argv


logger = logging.getLogger('keybone')


def execute_command_generate_backup():
    from keybone.console.parsers.backup import parser

    args = parser.parse_args(get_sub_parser_argv())
    manager = BackupManager(conf.key_home, conf.path)

    print manager.generate_backup(args.path)


def execute_command_recover_from_backup():
    from keybone.console.parsers.recover import parser

    args = parser.parse_args(get_sub_parser_argv())
    manager = BackupManager(conf.key_home, conf.path)

    with io.open(args.path, 'rb') as fd:
        data = fd.read()

    manager.recover_backup(data, conf.path, args.force)


def execute_command_quickstart():
    from keybone.console.parsers.quickstart import parser

    args = parser.parse_args(get_sub_parser_argv())

    data, path = initialize_key_home(args.conf_path, args.home, args.force)
    width = max(map(len, data.splitlines()))

    print "\033[1;30m{0}".format('-' * width)
    print data.strip()
    print '-' * width
    print "\033[0m\033[1;33myou might want do add the following line to your ~/.bashrc", "\033[0m"
    print "export KEYBONE_CONFIG_PATH='{0}'".format(path)
    print


def execute_command_wipe():
    from keybone.console.parsers.wipe import parser

    args = parser.parse_args(get_sub_parser_argv())
    should_backup = not args.no_backup

    if should_backup:
        manager = BackupManager(conf.key_home, conf.path)
        manager.generate_backup(path=args.backup_path)

    deleted = False
    for node in get_all_keyring_nodes():
        if not os.path.exists(node.path):
            continue

        agreed = False
        if args.force:
            agreed = True
        else:
            agreed = get_bool('delete file: {0} ?'.format(node.path))

        if agreed:
            os.unlink(node.path)
            logger.warning('deleting: {0}'.format(node.path))
            deleted = True

    if not deleted:
        print "{0} already empty".format(conf.path)

    if should_backup:
        logger.info('a backup was generated at: {0}'.format(args.backup_path))
