import argparse

parser = argparse.ArgumentParser(
    prog='keybone show',
    description='show details from a keyid')

parser.add_argument('recipient', metavar='<recipient>', help='any identification for the key: fingerprint, id or email')
