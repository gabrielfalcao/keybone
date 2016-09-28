import argparse

parser = argparse.ArgumentParser(
    prog='keybone list',
    description='lists existing keys')


parser.add_argument('--email', action='store_true', help='only print the email of the keys')
parser.add_argument('--private', action='store_true', help='show only private keys')
parser.add_argument('--public', action='store_true', help='show only public keys')
