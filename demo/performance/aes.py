#!/usr/bin/env python
from Crypto.Cipher import AES

key = b'Sixteen byte key'
#Scriviamo 256 byte a caso (ad es. ciaociao) li cifriamo 10000 volte e calcoliamo il tempo. Decifiamo l'output 10000 volte e calcoliamo il tempo.
def encrypt(plaintext):
  global nonce, tag
  cipher = AES.new(key, AES.MODE_EAX)
  nonce = cipher.nonce
  ciphertext, tag = cipher.encrypt_and_digest(data)
  return ciphertext


def decrypt(ciphertext):
  global nonce, tag
  cipher2 = AES.new(key, AES.MODE_EAX, nonce=nonce)
  plaintext = cipher2.decrypt(ciphertext)
  return plaintext
  '''  try:
    cipher2.verify(tag)
    print("The message is authentic:", plaintext)
  except ValueError:
    print("Key incorrect or message corrupted")'''