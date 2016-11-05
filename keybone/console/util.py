# -*- coding: utf-8 -*-
import sys
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


def max_line_length(content):
    return max(map(len, content.splitlines()))


def make_separator(content):
    return '-' * max_line_length(content)


def footer(content):
    return "\n\r{0}\r\n(length:{1})\033[0m".format(make_separator(content), len(content))


def header(title, color, content):
    return "\033[1;0{3}m{0}\n\r{2}\n\r{1}\n\r".format(make_separator(content), make_separator(title), title, color)


def output_to_fd(fd, *content):
    fd.write(" ".join(map(unicode, *content)))
    fd.write("\n")
    fd.flush()


def output_to_stderr(*content):
    output_to_fd(sys.stderr, *content)


class UI(object):

    class color:
        red = 31
        green = 32
        yellow = 33

    @staticmethod
    def yellow(title, content):
        output_to_stderr(
            header(title, UI.color.yellow, content),
            content,
            footer(content),
        )

    @staticmethod
    def green(title, content):
        output_to_stderr(
            header(title, UI.color.green, content),
            content,
            footer(content),
        )

    @staticmethod
    def red(title, content):
        output_to_stderr(
            header(title, UI.color.red, content),
            content,
            footer(content),
        )
