import argparse

parser = argparse.ArgumentParser(
    prog='keybone delete',
    description='delete a key if it does not exist already.')

parser.add_argument('recipient', metavar='<recipient>', help='the recipient to encrypt the data to')
parser.add_argument('-f', '--force', action='store_true', help='delete without confirmation')
