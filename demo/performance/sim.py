#!/usr/bin/env python
from toolate import encrypt, decrypt


plaintext = b"ciao"
ciphertext = None

ciphertext = encrypt(plaintext)
decrypt(ciphertext)
