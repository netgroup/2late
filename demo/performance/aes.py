#!/usr/bin/env python
from Crypto.Cipher import AES
key = b'Sixteen byte key'
cipher = AES.new(key, AES.MODE_CTR)
nonce = cipher.nonce


def encrypt(plaintext):
    ciphertext = cipher.encrypt(plaintext)
    return ciphertext


def decrypt(ciphertext):
    # cipher.initial_value(0)
    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext
