import argparse

parser = argparse.ArgumentParser(
    prog='keybone decrypt',
    description='decrypts the data to a known recipient')

parser.add_argument('ciphertext', metavar='<ciphertext>', help='the content to be decrypted')
parser.add_argument('--secret', metavar='<passphrase>', help='a passphrase')
