#!/usr/bin/env python
from toolate import encrypt as toolate_encrypt, decrypt as toolate_decrypt
from toolate_mod import encrypt as toolate_mod_encrypt, decrypt as toolate_mod_decrypt

from aes import encrypt as aes_encrypt, decrypt as aes_decrypt
from rsa import encrypt as rsa_encrypt, decrypt as rsa_decrypt
from abe import encrypt as abe_encrypt, decrypt as abe_decrypt
from ecies_primitives import encrypt as ecies_encrypt, decrypt as ecies_decrypt

from time import perf_counter


# simulate 256 byte AES key
plaintext = b"ciaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociao"
ciphertext = None
iterations = 1

encryptors = {
    "toolate": {"encrypt": toolate_encrypt, "decrypt": toolate_decrypt},
    "toolate_mod": {"encrypt": toolate_mod_encrypt, "decrypt": toolate_mod_decrypt},
    "aes": {"encrypt": aes_encrypt, "decrypt": aes_decrypt},
    "rsa": {"encrypt": rsa_encrypt, "decrypt": rsa_decrypt},
    "abe": {"encrypt": abe_encrypt, "decrypt": abe_decrypt},
    "ecies": {"encrypt": ecies_encrypt, "decrypt": ecies_decrypt},
}

for enc, functions in encryptors.items():
    print(f"===== Testing {enc} ======")
    encrypt, decrypt = functions["encrypt"], functions["decrypt"]

    # Start the stopwatch / counter
    t1_start = perf_counter()
    for i in range(iterations):
        ciphertext = encrypt(plaintext)
    # Stop the stopwatch / counter
    t1_stop = perf_counter()
    print(f"Encryption time for {iterations} iterations:", t1_stop-t1_start)
    print("Average time for encryption:", (t1_stop-t1_start)/iterations)

    # Start the stopwatch / counter
    t1_start = perf_counter()
    for i in range(iterations):
        decoded = decrypt(ciphertext)
    # Stop the stopwatch / counter
    t1_stop = perf_counter()
    print(f"Decryption time for {iterations} iterations:", t1_stop-t1_start)
    print("Average time for decryption:", (t1_stop-t1_start)/iterations)
