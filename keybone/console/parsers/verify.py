import argparse

parser = argparse.ArgumentParser(
    prog='keybone verify',
    description='verifies the given data for the given keyid'
)

parser.add_argument('signed_data', metavar='<signed-data>', help='the signed data to be verified')
