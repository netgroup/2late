import argparse
import hashlib

R0 = 123
g = 7 # group generator
p = 14387 # modulus - safe prime
q = (p - 1) /2 

def int_to_bytes(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')

def int_from_bytes(xbytes: bytes) -> int:
    return int.from_bytes(xbytes, 'big')

def main():
    parser = argparse.ArgumentParser(description='Create a key')
    parser.add_argument('time', type=int, 
                        help='time t (integer)')
    parser.add_argument('message', type=str, 
                        help='message m (string)')
    args = parser.parse_args()
    t = args.time
    m = args.message
    R = R0
    for i in range(t):
        hmsg =  hashlib.sha256()
        hmsg.update(int_to_bytes(R) + m.encode("utf8"))
        R = int_from_bytes(hmsg.digest())
        print(f"Iteration {i}: R={R}")
    inverseG = pow(g, p-2, p) 
    key = pow(inverseG, R, p)
    print(f"Key: {key}")

if __name__ == "__main__":
    main()
