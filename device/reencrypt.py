import time
import argparse
import hashlib
import os
from cryptography.fernet import Fernet

HYBRID_KEY_LEN = 10
i = 0 #time
Ri = 123

def reencrypt_file(file_path):
    """
    Re-encrypt a file
    """
    print(f"Re-encrypting f{file_path}")
    f = open(source_path, "rb")
    key = f.read(HYBRID_KEY_LEN)
    # TODO generate the new key
    new_key = key * Ri % p
    f.seek(0)
    f.write(new_key)
    f.close()

def gen_new_ri():
    """
    Generate the R_i as H(R_{i-1})
    """
    pass

def main():
    parser = argparse.ArgumentParser(description='Encrypt a data repository')
    parser.add_argument('target', type=str, 
                        help='target folder to re-encrypt')
    args = parser.parse_args()
    target = args.target
    while True:
        print(f"Doing the {i}-th reencryption")
        # for all the file in the repository, do a re-encryption of the symkeys
        for subdir in os.listdir(target):
            target_subdir = os.path.join(target, subdir)
            if os.path.isdir(os.path.join(target, subdir)):
                for filename in os.listdir(os.path.join(target, subdir)):
                    dest_path = os.path.join(target_subdir, filename)
                    reencrypt_file(dest_path)
        Ri = gen_new_ri()
        time.sleep(10)
        i += 1

if __name__ == "__main__":
    main()
