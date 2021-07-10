#!/usr/bin/env python

from ecies.utils import generate_eth_key
import ecies

privKey = generate_eth_key()
privKeyHex = privKey.to_hex()
pubKeyHex = privKey.public_key.to_hex()


def encrypt(plaintext=None):
    return ecies.encrypt(pubKeyHex, plaintext)


def decrypt(ciphertext=None):
    return ecies.decrypt(privKeyHex, ciphertext)
