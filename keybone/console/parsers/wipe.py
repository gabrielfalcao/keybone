import argparse
from datetime import datetime

parser = argparse.ArgumentParser(
    prog='keybone wipe',
    description='wipes the whole keybone setup')

DEFAULT_BACKUP_NAME = '{0}.backup.keybone'.format(datetime.utcnow().strftime('%H-%M-%S_%Y-%m-%s'))

parser.add_argument('-n', '--no-backup', action='store_true', help='with this flag no backup will be generated')
parser.add_argument('-f', '--force', action='store_true', help='delete all without confirmation')
parser.add_argument('--backup-path', default=DEFAULT_BACKUP_NAME, help='the path to the backup file')
