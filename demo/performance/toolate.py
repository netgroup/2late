#!/usr/bin/env python

# Scriviamo 256 byte a caso (ad es. ciaociao) li cifriamo 10000 volte e calcoliamo il tempo. Decifiamo l'output 10000 volte e calcoliamo il tempo.

import hashlib

# p = 31069134934692028950630944905537189651159460682707755526095924093778156511183593429662954179295617255708928469780289762197493434048244899989786916849190107573810423123703345257358980694082224840315739601381825785406436382248054056792144385766718201057809534851287010570221145790971223666055364200864238421029379877129071893195256380298130895326631577077689165469224207711857138395801195131345503823209141871572494962521556498132021971096275972861769233335190097080498306312848481050696462502264841293579450698768576851790039950796823378185440725942901615075488706994167511851967148433888470088647570764346248151330539  # 2048 bit
# q = (p - 1) // 2
# g = 7  # group generator
ri = 1234567890
tag = "test"


def int_to_bytes(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')


def int_from_bytes(xbytes: bytes) -> int:
    return int.from_bytes(xbytes, 'big')


def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])


# get decryption key
Rsum = 0
hmsg = hashlib.sha256()
hmsg.update(int_to_bytes(ri) + tag.encode("utf8"))
# ri_tag_digest = int_from_bytes(hmsg.digest()) % q
# inverseG = pow(g, p-2, p)
# key = pow(inverseG, ri_tag_digest, p)
key = hmsg.digest()


def encrypt(plaintext):
    hmsg = hashlib.sha256()
    hmsg.update(int_to_bytes(ri) + tag.encode("utf8"))
    ri_tag_digest = hmsg.digest()  # int_from_bytes(hmsg.digest())  # this is H(Ri |tag)

    # create the new reencrypted key
    # re_encrypted_key = int_from_bytes(plaintext) * pow(g, ri_tag_digest, p) % p

    # re_enc_key_bytes = int_to_bytes(re_encrypted_key)
    return byte_xor(plaintext, ri_tag_digest)  # re_enc_key_bytes


def decrypt(ciphertext):
    # enc_skey_int = int_from_bytes(ciphertext)
    # plaintext_int = enc_skey_int * key % p
    # plaintext_bytes = int_to_bytes(plaintext_int)
    return byte_xor(ciphertext, key)  # plaintext_bytes
