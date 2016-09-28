import argparse

parser = argparse.ArgumentParser(
    prog='keybone import',
    description='imports a key')

parser.add_argument('key', metavar='<key>', help='as string, with linebreaks')
