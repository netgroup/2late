#!/usr/bin/env python
from toolate import encrypt as toolate_encrypt, decrypt as toolate_decrypt
from aes import encrypt as aes_encrypt, decrypt as aes_decrypt
from aont import pad, unpad

from time import perf_counter


# simulate 256 byte AES key
plaintext = b"abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd"
ciphertext = None
iterations = 10000

encryptors = {
    "toolate": {"encrypt": toolate_encrypt, "decrypt": toolate_decrypt},
    "aes": {"encrypt": aes_encrypt, "decrypt": aes_decrypt},
    #"aont": {"encrypt": pad, "decrypt": unpad},
}

for enc, functions in encryptors.items():
    print(f"Testing {enc}")
    encrypt, decrypt = functions["encrypt"], functions["decrypt"]

    # print(f"plaintext: {plaintext} ({len(plaintext)})")

    # Start the stopwatch / counter
    t1_start = perf_counter()
    for i in range(iterations):
        ciphertext = encrypt(plaintext)
        # print(f"ciphertext: {ciphertext} ({len(ciphertext)})")
    # Stop the stopwatch / counter
    t1_stop = perf_counter()
    print(f"Encryption time for {iterations} iterations:", t1_stop-t1_start)
    print(f"Average encryption time:", (t1_stop-t1_start)/iterations)

    # Start the stopwatch / counter
    t1_start = perf_counter()
    for i in range(iterations):
        decoded = decrypt(ciphertext)
        # print(f"plaintext: {decoded} ({len(decoded)})")
    # Stop the stopwatch / counter
    t1_stop = perf_counter()
    print(f"Decryption time for {iterations} iterations:", t1_stop-t1_start)
    print(f"Average decryption time:", (t1_stop-t1_start)/iterations)
