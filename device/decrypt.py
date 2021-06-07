import argparse
import hashlib
import os
from cryptography.fernet import Fernet

HYBRID_KEY_LEN = 10

def decrypt_file(source_path, key):
    """
    Use the key to decrypt the symmetric key which is written 
    at the beginning of the file
    """
    sf = open(source_path, "rb")
    f = Fernet(key)
    # TODO capire chiave
    enc_skey = sf.read(HYBRID_KEY_LEN)
    # TODO da bytes a intero...
    skey = enc_skey * key % p
    def read_in_chunks(file_object, chunk_size=1024):
        """Lazy function (generator) to read a file piece by piece.
        Default chunk size: 1k."""
        while True:
            data = file_object.read(chunk_size)
            if not data:
                break
            yield data
    for piece in read_in_chunks(sf):
        decrypted = f.decrypt(piece)
        print(decrypted)
    sf.close()


def main():
    parser = argparse.ArgumentParser(description='Decrypt a file')
    parser.add_argument('file', type=str, 
                        help='file to decrypt')
    parser.add_argument('key', type=str, 
                        help='Cryptographic key to decrypt')
    args = parser.parse_args()
    f = args.file
    key = args.key

if __name__ == "__main__":
    main()
