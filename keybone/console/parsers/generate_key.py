import argparse

parser = argparse.ArgumentParser(
    prog='keybone generate',
    description='generate a key if it does not exist already.')

parser.add_argument('name', metavar='<name>', help='the user name')
parser.add_argument('email', metavar='<email>', help='the user email')
parser.add_argument('--secret', metavar='<passphrase>', help='a passphrase. If not provided it will be asked with getpass')
parser.add_argument('-n', '--no-secret', help='create without password', action='store_true', default=False)
