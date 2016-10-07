#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import json
import gnupg
import logging


from plant import Node
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken

from keybone import conf
from keybone.util import GPGSerializer

node = Node(__file__).dir
logger = logging.getLogger('keybone')

uid_regex = re.compile(r'(?P<name>.*?)\s*[(](?P<metadata>[^)]+)[)]\s*[<]\s*(?P<email>[^>]+)\s*[>]\s*')


class KeyAlreadyExists(Exception):
    """Exception raised when a key already exists in the keyring"""
    def __init__(self, key):
        super(KeyAlreadyExists, self).__init__(key['email'])
        self.key = key


class InvalidKeyError(Exception):
    """Exception raised when trying to import an invalid key"""


class InvalidRecipient(Exception):
    """Exception raised when the recipient was not found in the keyring"""


class SymmetricalHelper(object):
    """helper that automatically encrypts and decrypts.

    :param key: a string with a Fernet key
    """
    def __init__(self, key):
        if not key:
            self.symmetric = None
        else:
            self.symmetric = Fernet(key)

    def encrypt(self, data):
        """
        :param data: the data to be encrypted
        """
        if self.symmetric:
            return self.symmetric.encrypt(data)
        logger.warning('the "fernet_key" setting is not available. The data will not be encrypted')
        return data

    def decrypt(self, cipher_text):
        """
        :param data: the data to be decrypted
        """
        if not self.symmetric:
            return cipher_text

        try:
            return self.symmetric.decrypt(bytes(cipher_text))
        except InvalidToken:
            return cipher_text


def ensure_secure_key_folder(path):
    """ensures that the given path is secure with permission 0700.

    :param path: the path to be secured
    :returns: the path itself
    """
    if not os.path.exists(path):
        os.makedirs(path)
    stat = os.stat(path)
    mode = oct(stat.st_mode)[-3:]
    if mode != '700':
        # side-effect: set files to 0700 mode
        logging.warning('changing mode of {0} to 0700'.format(os.path.abspath(path)))
        os.chmod(path, 0700)

    return path


class KeyBone(object):
    """Handles all key management

    :param path: the path to the key home
    :param password: the fernet key used for encrypting the key comments
    """
    def __init__(self, path=conf.key_home, password=conf.fernet_key):
        self.key_home = ensure_secure_key_folder(path)  # this has a side-effect in the file-system
        self.symmetric = SymmetricalHelper(password)
        self.gpg = gnupg.GPG(gnupghome=path)
        self.serialize = GPGSerializer(self)

    def sort_keys(self, keys):
        """sorts a list of keys by email while putting

        :param keys: a list of keys
        :returns: a sorted list
        """
        ordered = sorted(sorted(keys, key=lambda x: x.get('email', '')), key=lambda x: x.get('private', ''), reverse=True)
        uniq = []
        final = []
        for key in ordered:
            keyid = key['keyid']

            if keyid in uniq:
                continue

            uniq.append(keyid)
            final.append(key)

        return final

    def list_private_keys(self):
        """returns a sorted list of the private keys available in the keychain
        """
        return self.sort_keys(map(self.serialize.key, self.gpg.list_keys(True)))

    def list_public_keys(self):
        """returns a sorted list of the public keys available in the keychain
        """
        return self.sort_keys(map(self.serialize.key, self.gpg.list_keys(False)))

    def list_keys(self):
        """returns a list of all existing keys, public and private"""
        all_keys = []
        all_keys.extend(self.list_private_keys())
        all_keys.extend(self.list_public_keys())
        return self.sort_keys(all_keys)

    def generate_key(self, name, email, passphrase, expire_date=0, length=2048):
        """generates a key if it doesn't for the given email

        :param name: the name of the owner of the key
        :param email: the email
        :param passphrase: the passphrase for the key
        :param expire_date: the expiration date for the key (defaults to 0)
        :param length: the length the key (defaults to 2048)
        """
        for key in self.list_keys():
            if email in key['email']:
                raise KeyAlreadyExists(key)

        key_input = self.gpg.gen_key_input(**{
            "key_type": "RSA",
            "key_length": length,

            # # revogation ?
            # "subkey_type": "RSA",
            # "subkey_length": 2048,

            "name_real": name,
            "name_comment": self.symmetric.encrypt(json.dumps({
                'email': email,
                'name': name,
            })),
            "name_email": email,
            "passphrase": passphrase,
            "expire_date": expire_date,
        })
        return self.gpg.gen_key(key_input)

    def import_key(self, key):
        """imports keys from a string
        :param key: a string with the key
        """

        result = self.gpg.import_keys(key)
        if not result:
            msg = 'Invalid GPG key: {0}'.format(key)
            raise InvalidKeyError(msg)

        return result

    def get_key_for_id(self, keyid):
        """returns the key for the given id
        :param keyid: the key id
        :returns: the key dictionary of ``None``
        """

        for key in self.list_keys():
            if key['keyid'] == keyid:
                return key

    def get_key_for_fingerprint(self, fingerprint):
        """returns the key for the given fingerprint
        :param fingerprint: the fingerprint
        :returns: the key dictionary of ``None``
        """
        for key in self.list_keys():
            if key['fingerprint'] == fingerprint:
                return key

    def get_key_for_email(self, email):
        """returns the key for the given email
        :param email: the email
        :returns: the key dictionary of ``None``
        """
        for key in self.list_keys():
            if key['email'] == email:
                return key

    def get_key(self, id_fingerprint_or_email):
        """returns the key for the given recipient
        :param id_fingerprint_or_email: a key id, fingerprint or email
        :returns: the key dictionary of ``None``
        """
        return (
            self.get_key_for_fingerprint(id_fingerprint_or_email) or
            self.get_key_for_id(id_fingerprint_or_email) or
            self.get_key_for_email(id_fingerprint_or_email)
        ) or {
            'keyid': None,
            'fingerprint': None,
            'email': None,
            'passphrase': None,
        }

    def get_fingerprint(self, recipient):
        """retrieves the fingerprint
        :param recipient: a key id, fingerprint, email
        :returns: a fingerprint
        """
        key = self.get_key(recipient)
        return key['fingerprint']

    def get_keyid(self, recipient):
        """retrieves the keyid
        :param recipient: a key id, keyid, email
        :returns: a keyid
        """
        key = self.get_key(recipient)
        return key['keyid']

    def get_passphrase(self, recipient):
        """retrieves the passphrase
        :param recipient: a key id, passphrase, email
        :returns: a passphrase
        """
        key = self.get_key(recipient)
        return key.get('passphrase')

    def encrypt(self, recipient, plaintext, sign_from=None):
        """encrypts plaintext to a recipient

        :param recipient: a key id, passphrase, email
        :param plaintext: the data to be encrypted
        :param sign_from: a recipient who will sign the message
        :returns: ciphertext
        """
        fingerprint = self.get_fingerprint(recipient)
        if not fingerprint:
            msg = 'there are no keys for the recipient for email: {0}'.format(recipient)
            raise InvalidRecipient(msg)

        kw = {}
        if sign_from:
            kw['sign'] = self.get_fingerprint(sign_from)

        crypt = self.gpg.encrypt(plaintext.strip(), recipient, always_trust=True, **kw)
        if crypt.data:
            return crypt.data

        logger.error(" - ".join([crypt.status, crypt.stderr]))

    def decrypt(self, ciphertext, passphrase=None):
        """decrypts the given ciphertext as long as the key is available in the keychain

        :param ciphertext: the data to be decrypted
        :param passphrase: the passphrase used for decryption
        :returns: plaintext
        """
        crypt = self.gpg.decrypt(ciphertext.strip(), passphrase=passphrase, always_trust=True)
        if crypt.data:
            return crypt.data

        elif passphrase:
            logger.error(" - ".join([crypt.status, crypt.stderr]))
            return

        uid = self.serialize.extract_uid([crypt.stderr])
        if not uid:
            logger.error(crypt.stderr)
            return

        # TODO: check for the right key by fingerprint, emails are NOT
        # unique in a keyring

        key = self.get_key(uid['email'])
        if not key['private']:
            raise InvalidKeyError('cannot decrypt because private key is missing for: {0}'.format(uid['email']))

        passphrase = uid.get('passphrase')
        return self.decrypt(ciphertext, passphrase)

    def sign(self, recipient, data, passphrase=None):
        """signs the given text using the given recipient

        :param recipient: a key id, passphrase, email
        :param data: the data to be signed
        :returns: the signed data
        """
        keyid = self.get_keyid(recipient)
        crypt = self.gpg.sign(data, keyid=keyid, passphrase=passphrase)
        if not crypt.data:
            logger.error(crypt.stderr)
            return

        return crypt.data

    def verify(self, data):
        """verifies if the given signed data is valid

        :param data: the data
        :returns: a tuple containing (status, trust_text)
        """
        crypt = self.gpg.verify(data)
        if not crypt.status:
            logger.error(crypt.stderr)
            return

        return crypt.status, crypt.trust_text

    def delete_key(self, fingerprint):
        """generates a key if it doesn't for the given email

        :param fingerprint: the fingerprint of the key
        """
        key = self.get_key_for_fingerprint(fingerprint)
        if not key:
            return

        private = key['type'] == 'sec'
        result = []

        if private:
            result.append(self.gpg.delete_keys(fingerprint, True).status)

        result.append(self.gpg.delete_keys(fingerprint, False).status)
        return "\n".join(result)
