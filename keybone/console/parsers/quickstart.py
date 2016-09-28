import argparse

parser = argparse.ArgumentParser(
    prog='keybone quickstart',
    description='initializes a new keybone key home, which includes generating a fernet key to encrypt the key metadata')

parser.add_argument('conf_path', help='the path to the config file')
parser.add_argument('-f', '--force', action='store_true', help='flag to force even if destination exists')
parser.add_argument('--home', default='keys', help='the path to the key home. Defaults to a "keys" folder relative to the config file path')
