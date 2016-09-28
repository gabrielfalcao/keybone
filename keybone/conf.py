#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logging
import coloredlogs
from plant import Node
from milieu import Environment

self = sys.modules[__name__]


SUPPORTED_CONFIG_PATHS = map(os.path.abspath, [
    os.path.expanduser('~/.keybone.yml'),
])


def get_env(path):
    if os.path.exists(path):
        env = Environment.from_file(path)
    else:
        env = Environment()
    return env


def initialize_config(self, path, env):
    coloredlogs.install(level=logging.INFO, show_hostname=False, fmt='[%(name)s] %(levelname)s %(message)s')
    if os.path.exists(path):
        stat = os.stat(path)
        mode = oct(stat.st_mode)[-3:]
        if mode != '700':
            logging.warning('changing mode of {0} to 0700'.format(os.path.abspath(path)))
            os.chmod(path, 0700)

    self.path = path
    self.node = Node(path)
    self.fernet_key = env.get('fernet_key')
    self.key_home = self.node.dir.join(os.path.expanduser(env.get('key_home') or './keybone-keyring'))


def setup_from_config_path(self, path):
    env = get_env(path)
    initialize_config(self, path, env)


fallback_config_path = os.path.join(os.getcwd(), '.keybone.yml')

for config_path in SUPPORTED_CONFIG_PATHS:
    if os.path.exists(config_path):  # pragma: no cover
        fallback_config_path = config_path

keybone_config_path = os.getenv('KEYBONE_CONFIG_PATH') or fallback_config_path

setup_from_config_path(self, keybone_config_path)
