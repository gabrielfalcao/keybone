import argparse

parser = argparse.ArgumentParser(
    prog='keybone backup',
    description='generates base64 encoded backup of the whole keyring, ready to be imported again at any time')

parser.add_argument('-p', '--path', help='destination path of the encrypted tarball')
