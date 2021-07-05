import argparse
import hashlib
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import padding
from utils import int_to_bytes, int_from_bytes, read_in_chunks
from settings import SYM_KEY_LEN, TOO_LATE_SIGNATURE_LEN, TOO_LATE_HEADER_LEN, g, p, q


def decrypt_file(source_path, key):
    """
    Use the key to decrypt the file at source_path.
    File is encrypted using hybrid encryption. 
    The symmetric key, at the beginning of the file, is encrypted with 2late.
    """
    # get the header containing the encrypted symkey
    sf = open(source_path, "rb")
    assert(sf.read(TOO_LATE_SIGNATURE_LEN) == b'2l8')
    enc_skey = sf.read(SYM_KEY_LEN)
    enc_skey_int = int_from_bytes(enc_skey)
    print(f"enc_skey: {enc_skey_int}")
    # decrypt the symmetric key
    skey = enc_skey_int * key % p
    skey_bytes = int_to_bytes(skey)
    print(f"sym key : {skey}")
    print(f"sym key (bytes) : {skey_bytes}")
    # decrypt the file chunk by chunk using symkey
    f = Fernet(skey_bytes)
    for piece in read_in_chunks(sf):
        decrypted = f.decrypt(piece)
        print(decrypted)
        # TODO: save somewhere the decryption output
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
