from elgamal.elgamal import Elgamal


pb, pv = Elgamal.newkeys(256)

def encrypt(plaintext):
    return Elgamal.encrypt(plaintext, pb)

def decrypt(ciphertext):
    return Elgamal.decrypt(ciphertext, pv)
