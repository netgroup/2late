"""
Perform initial encryption of data in DATA, placing encrypted data in ENCDATA
"""
import argparse
import hashlib
import os
from cryptography.fernet import Fernet

R0 = 123
g = 7 # group generator
p = 14387 # modulus - safe prime
q = (p - 1) /2 

def int_to_bytes(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')

def int_from_bytes(xbytes: bytes) -> int:
    return int.from_bytes(xbytes, 'big')

def encrypt_file(source_path, dest_path):
    """
    Read source file from source path.
    Apply hybrid encryption on source file.
    Encrypt the sym key with 2Late.
    Write the encrypted content on dest_path, prepending the encrypted key.
    """
    print(f"Encrypting {source_path} to {dest_path}")

    sf = open(source_path, "rb")
    df = open(dest_path, "wb")

    key = Fernet.generate_key()
    f = Fernet(key)

    # get the subdir name, to compute H(R|subdir)
    subdir_name = source_path.split('/')[-2]
    print(f"subdir name is {subdir_name}")
    hmsg =  hashlib.sha256()
    hmsg.update(int_to_bytes(R0) + subdir_name.encode("utf8"))
    Rmsg = int_from_bytes(hmsg.digest()) # this is H(R0|dirname)

    # encrypt the symmetric key as key * g^{H(R0|dirname)} 
    #TODO: qui abbiamo un problema perché la chiave è più piccola di p
    #TODO: la moltiplicazione la facciamo cosi?
    encrypted_key = int_from_bytes(key) * pow(g, Rmsg, p) % p
    print(f"Key is {key}")
    print(f"Encrypted key is {encrypted_key}")

    # encrypt all the piece of the original file
    def read_in_chunks(file_object, chunk_size=1024):
        """Lazy function (generator) to read a file piece by piece.
        Default chunk size: 1k."""
        while True:
            data = file_object.read(chunk_size)
            if not data:
                break
            yield data
    # prepend the encrypted key to the file
    #TODO: capire quanto è lunga la encrypted key  
    #fare lunghezza fissa e mettere padding?
    # https://cryptography.io/en/latest/hazmat/primitives/padding/
    df.write(int_to_bytes(encrypted_key))
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
