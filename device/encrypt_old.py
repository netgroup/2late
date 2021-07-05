"""
Perform initial encryption of data in DATA, placing encrypted data in ENCDATA
"""
import argparse
import hashlib
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import padding
from utils import int_to_bytes, int_from_bytes, read_in_chunks
from settings import HYBRID_HEADER_LEN, R0, g, p, q

def encrypt_file(source_path, dest_path):
    """
    Read source file from source path.
    Apply hybrid encryption on source file.
    Encrypt the sym key with 2Late.
    Write the encrypted content on dest_path, prepending the encrypted key.
    """
    print(f"Encrypting {source_path} to {dest_path}")

    # encrypt source file in dest file
    sf = open(source_path, "rb")
    df = open(dest_path, "wb")

    # get a random sym key
    key = Fernet.generate_key()
    f = Fernet(key)

    # get the subdir name, to compute H(R1|subdir)
    subdir_name = source_path.split('/')[-2]
    print(f"subdir name is {subdir_name}")
    # get R0_msg
    # add the salt taken from the directory name
    hmsg =  hashlib.sha256()
    hmsg.update(int_to_bytes(R0) + subdir_name.encode("utf8"))
    R0_msg = int_from_bytes(hmsg.digest()) # H(R0|subdir)

    # encrypt the symmetric key as key * g^{H(R0|dirname)} 
    assert(len(int_to_bytes(p)) > len(hmsg.digest())) # key < p
    encrypted_key = int_from_bytes(key) * pow(g, R0_msg, p) % p
    print(f"Key is {key}")
    print(f"Encrypted key is {encrypted_key}")
    # encrypt all the piece of the original file

    assert(len(int_to_bytes(encrypted_key)) == HYBRID_HEADER_LEN)
    df.write(int_to_bytes(encrypted_key))
    # encrypt and write the file content
    for piece in read_in_chunks(sf):
        print(piece)
        encrypted = f.encrypt(piece)
        df.write(encrypted)
    sf.close()
    df.close()

def main():
    parser = argparse.ArgumentParser(description='Encrypt a data repository')
    parser.add_argument('source', type=str, 
                        help='folder containing data to encrypt')
    parser.add_argument('target', type=str, 
                        help='target folder to place encrypted data')
    args = parser.parse_args()
    src = args.source
    target = args.target

    try:
        os.mkdir(target)
    except OSError:
        print ("Creation of the directory %s failed" % target)
    else:
        print ("Successfully created the directory %s " % target)

    for subdir in os.listdir(src):
        target_subdir = os.path.join(target, subdir)
        source_subdir = os.path.join(src, subdir)
        os.mkdir(target_subdir)
        print(f"{target_subdir} created")
        if os.path.isdir(os.path.join(src, subdir)):
            for filename in os.listdir(os.path.join(src, subdir)):
                source_path = os.path.join(source_subdir, filename)
                dest_path = os.path.join(target_subdir, filename)
                encrypt_file(source_path, dest_path)
                print(f"Encrypting {filename}")


if __name__ == "__main__":
    main()
