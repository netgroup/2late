import time
import argparse
import hashlib
import os
from cryptography.fernet import Fernet
from utils import int_to_bytes, int_from_bytes, read_in_chunks
from settings import HYBRID_HEADER_LEN, R0, g, p, q

i = 0 #number of re-encryption perfomed on files
Ri = 123

def reencrypt_file(file_path):
    """
    Re-encrypt a file
    """
    print(f"Re-encrypting {file_path}")
    subdir_name = file_path.split('/')[-2]
    print(f"subdir name is {subdir_name}")
    # read the encrypted key
    f = open(file_path, "r+b")
    enc_key = f.read(HYBRID_HEADER_LEN)

    # generate H(Ri |dirname)
    hmsg =  hashlib.sha256()
    hmsg.update(int_to_bytes(Ri) + subdir_name.encode("utf8"))
    Ri_msg = int_from_bytes(hmsg.digest()) # this is H(Ri |dirname)
    
    # create the new reencrypted key
    reencrypted_key = int_from_bytes(enc_key) * pow(g, Ri_msg, p) % p

    # write back the result into the file
    f.seek(0)
    f.write(int_to_bytes(reencrypted_key))
    assert(len(int_to_bytes(reencrypted_key)) == HYBRID_HEADER_LEN)
    f.close()

def gen_next_ri():
    """
    Generate R_i as H(R_{i-1})
    """
    global Ri
    hmsg =  hashlib.sha256()
    hmsg.update(int_to_bytes(Ri))
    Ri = int_from_bytes(hmsg.digest())

def main():
    global i
    parser = argparse.ArgumentParser(description='Encrypt a data repository')
    parser.add_argument('target', type=str, 
                        help='target folder to re-encrypt')
    args = parser.parse_args()
    target = args.target
    while True:
        i += 1
        gen_next_ri()
        print(f"Doing the {i}-th reencryption")
        # for all the file in the repository, do a re-encryption of the symkeys
        for subdir in os.listdir(target):
            target_subdir = os.path.join(target, subdir)
            if os.path.isdir(os.path.join(target, subdir)):
                for filename in os.listdir(os.path.join(target, subdir)):
                    dest_path = os.path.join(target_subdir, filename)
                    reencrypt_file(dest_path)
        time.sleep(10)

if __name__ == "__main__":
    main()
