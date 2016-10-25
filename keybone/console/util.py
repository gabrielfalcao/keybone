# -*- coding: utf-8 -*-
import os
import statvfs

MAX_FILENAME = os.statvfs(os.getcwd())[statvfs.F_NAMEMAX]


def expand_path(path):
    return os.path.abspath(os.path.expanduser(path))


def is_a_valid_filename(string):
    return len(string) <= MAX_FILENAME and os.sep in string


def is_file_and_exists(string):
    path = expand_path(string)
    return is_a_valid_filename(path) and os.path.exists(path)
