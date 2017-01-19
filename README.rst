KeyBone 0.4.2 - PGP for humans
================================

.. image:: https://readthedocs.org/projects/keybone/badge/?version=latest
   :target: http://keybone.readthedocs.io/en/latest/?badge=latest

.. image:: https://travis-ci.org/gabrielfalcao/keybone.svg?branch=master
   :target: https://travis-ci.org/gabrielfalcao/keybone

.. image:: https://codecov.io/gh/gabrielfalcao/keybone/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/gabrielfalcao/keybone


KeyBone makes it easy to manage public and private GPG keys and
encrypt/decrypt strings and files.

Features:
---------

- Slick command-line interface
- Extra layer of security: the keyring is encrypted using a vault password
- Provides a command-line utility that checks if the config file and
  keychain are safely stored in the filesystem.
- Easily create,list,revogate and sign keys
- Easily encrypt and decrypt files and one-off strings

Installing dependencies on Mac OSX (homebrew)
=============================================

1. Ensure `GnuPG <https://gnupg.org/>`_  >= ``2.1.15`` is installed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash


    brew uninstall -y --force gnupg && brew unlink gnupg2 && brew link --overwrite --force gnupg2


In your virtualenv
==================


.. code:: bash

    pip install keybone



Notes
-----

* Talk about: https://blog.cryptographyengineering.com/2014/08/13/whats-matter-with-pgp/
