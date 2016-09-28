import argparse

parser = argparse.ArgumentParser(
    prog='keybone recover',
    description='recovers a keybone GPG setup from an encrypted tarball')

parser.add_argument('path', help='the path to an encrypted tarball containing a new keychain')
parser.add_argument('-f', '--force', action='store_true', help='flag to force even if destination exists')
