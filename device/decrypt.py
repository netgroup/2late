import argparse
import hashlib
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import padding
from utils import int_to_bytes, int_from_bytes, read_in_chunks
from settings import HYBRID_HEADER_LEN, g, p, q

def decrypt_file(source_path, key):
    """
    Use the key to decrypt the symmetric key which is written 
    at the beginning of the file
    """
    sf = open(source_path, "rb")
    enc_skey = sf.read(HYBRID_HEADER_LEN)
    #padded_enc_skey = sf.read(HYBRID_HEADER_LEN)
    #print(f"padded_enc_skey: {padded_enc_skey}")
    ## remove the padding
    #unpadder = padding.PKCS7(HYBRID_HEADER_LEN * 8 / 2).unpadder()
    #enc_skey = unpadder.update(padded_enc_skey)
    #enc_skey += unpadder.finalize()
    enc_skey_int = int_from_bytes(enc_skey)
    print(f"enc_skey: {enc_skey_int}")
    # decrypt the symmetric key   
    skey = enc_skey_int * key % p
    skey_bytes = int_to_bytes(skey)
    print(f"sym key : {skey}")
    print(f"sym key : {skey_bytes}")
    # decrypt the file chunk by chunk
    f = Fernet(skey_bytes)
    for piece in read_in_chunks(sf):
        decrypted = f.decrypt(piece)
        print(decrypted)
    sf.close()


def main():
    parser = argparse.ArgumentParser(description='Decrypt a file')
    parser.add_argument('file', type=str, 
                        help='file to decrypt')
    parser.add_argument('key', type=int, 
                        help='Cryptographic key to decrypt')
    args = parser.parse_args()
    filename = args.file
    key = args.key
    print(f"Decrypting {filename} with key {key}")
    decrypt_file(filename, key)

if __name__ == "__main__":
    main()
