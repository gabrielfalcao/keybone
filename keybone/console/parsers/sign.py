import argparse

parser = argparse.ArgumentParser(
    prog='keybone sign',
    description='signs the given data for the given keyid')

parser.add_argument('recipient', metavar='<recipient>', help='any identification for the key: fingerprint, id or email')
parser.add_argument('data', metavar='<data>', help='the content to be signed')
parser.add_argument('--secret', metavar='<passphrase>', help='a passphrase if necesssary')
parser.add_argument('--no-secret', help='set this flag if the destination key doesn not have a secret', action='store_true', default=False)
