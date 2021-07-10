#!/usr/bin/env python

import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP

random_generator = Random.new().read
key = RSA.generate(4096, random_generator)  # generate pub and priv key
publickey = key.publickey()  # pub key export for exchange

key = PKCS1_OAEP.new(key)
publickey = PKCS1_OAEP.new(publickey)


def encrypt(plaintext):
    encrypted = publickey.encrypt(plaintext)
    return encrypted


def decrypt(ciphertext):
    decrypted = key.decrypt(ciphertext)
    return decrypted
