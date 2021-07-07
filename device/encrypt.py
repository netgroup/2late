"""
Perform encryption or re-encryption of data in DATA with inplace substitution.
"""
import argparse
import hashlib
import os
import tempfile
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import padding
from utils import int_to_bytes, int_from_bytes, read_in_chunks
from settings import SYM_KEY_LEN, TOO_LATE_SIGNATURE_LEN, TOO_LATE_HEADER_LEN, CONFIG_FILE, R0, g, p, q


def encrypt_file(source_path, tag, ri):
    """
    Read source file from source path.
    Apply hybrid encryption on source file.
    Encrypt the sym key with 2Late.
    Write the encrypted content on dest_path, prepending the encrypted key.
    """
    # Understand if the file is already encrypted or not
    is_encrypted = False
    sf = open(source_path, "r+b")
    header = sf.read(TOO_LATE_SIGNATURE_LEN)
    is_encrypted = header == b"2l8"
    sf.seek(0)

    if not is_encrypted:
        # File is not encrypted yet.
        # Do hybrid encryption and encrypt the sym key
        print("Do encryption for the first time")

        # get a random sym key
        key = Fernet.generate_key()
        f = Fernet(key)

        hmsg = hashlib.sha256()
        hmsg.update(int_to_bytes(ri) + tag.encode("utf8"))
        ri_tag_digest = int_from_bytes(hmsg.digest())  #  H(Ri|tag)

        assert(len(int_to_bytes(p)) > len(hmsg.digest()))  #  key < p

        # encrypt the symmetric key as key * g^{H(Ri|tag)}
        encrypted_key = int_from_bytes(key) * pow(g, ri_tag_digest, p) % p
        print(f"Key is {key}")
        print(f"Encrypted key is {encrypted_key}")
        # encrypt all the pieces of the original file

        assert(len(int_to_bytes(encrypted_key)) == SYM_KEY_LEN)

        # encrypt and write the file content
        encrypted = f.encrypt(sf.read())
        sf.seek(0)
        sf.write(b'2l8')
        sf.write(int_to_bytes(encrypted_key))
        sf.write(encrypted)
    else:
        # file is already encrypted with symkey, do a re-encryption
        print("Do re-encryption")

        # read the sym encryption key
        sf.seek(TOO_LATE_SIGNATURE_LEN)
        enc_key = sf.read(SYM_KEY_LEN)

        # generate H(Ri |tag)
        hmsg = hashlib.sha256()
        hmsg.update(int_to_bytes(ri) + tag.encode("utf8"))
        ri_tag_digest = int_from_bytes(hmsg.digest())  # this is H(Ri |tag)

        # create the new reencrypted key
        reencrypted_key = int_from_bytes(
            enc_key) * pow(g, ri_tag_digest, p) % p

        # write back the result into the file
        sf.seek(0)
        sf.write(int_to_bytes(reencrypted_key))
        assert(len(int_to_bytes(reencrypted_key)) == SYM_KEY_LEN)
    sf.close()


def get_ri():
    """
    Return the current Ri by reading in the configuration file
    """
    if os.path.isfile(CONFIG_FILE):
        f = open(CONFIG_FILE, "rb")
        ri = int_from_bytes(f.read())
        f.close()
    else:
        f = open(CONFIG_FILE, "wb")
        ri = R0
        f.write(int_to_bytes(ri))
        f.close()
    return ri


def save_next_ri(ri):
    """
    Compute the next value for ri and write it on the config file
    """
    f = open(CONFIG_FILE, "wb")
    hmsg = hashlib.sha256()
    hmsg.update(int_to_bytes(ri))
    next_ri = int_from_bytes(hmsg.digest())
    print("Computing next Ri")
    print(f"Old: {ri}\tNew: {next_ri}")
    f.write(int_to_bytes(next_ri))
    f.close()


def main():
    parser = argparse.ArgumentParser(description='Encrypt a data repository')
    parser.add_argument('data_path', type=str,
                        help='folder containing data to encrypt')

    args = parser.parse_args()
    data_path = args.data_path
    ri = get_ri()
    for subdir in os.listdir(data_path):
        target_subdir = os.path.join(data_path, subdir)
        if os.path.isdir(os.path.join(data_path, subdir)):
            for filename in os.listdir(os.path.join(data_path, subdir)):
                source_path = os.path.join(target_subdir, filename)
                print(
                    f"Encrypting {source_path} in subdir {subdir}")
                encrypt_file(source_path, subdir, ri)
    save_next_ri(ri)


if __name__ == "__main__":
    main()
