#!/usr/bin/env python
from toolate import encrypt as toolate_encrypt, decrypt as toolate_decrypt
from time import perf_counter


# simulate 256 byte AES key
plaintext = b"ciaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociaociao"
ciphertext = None
iterations = 1000

encrypt, decrypt = toolate_encrypt, toolate_decrypt

# Start the stopwatch / counter
t1_start = perf_counter()
for i in range(iterations):
    ciphertext = encrypt(plaintext)
    #print(f"ciphertext: {ciphertext}")
# Stop the stopwatch / counter
t1_stop = perf_counter()
print(f"Encryption time for {iterations} iterations:", t1_stop-t1_start)

# Start the stopwatch / counter
t1_start = perf_counter()
for i in range(iterations):
    decoded = decrypt(ciphertext)
    #print(f"plaintext: {decoded}")
# Stop the stopwatch / counter
t1_stop = perf_counter()
print(f"Decryption time for {iterations} iterations:", t1_stop-t1_start)
