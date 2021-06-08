import argparse
import hashlib
from settings import p, q, R0, g


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
    Ri = R0
    Rsum = 0
    for i in range(t+1):
        hmsg =  hashlib.sha256()
        hmsg.update(int_to_bytes(Ri) + m.encode("utf8"))
        Ri_msg = int_from_bytes(hmsg.digest())
        print(f"Iteration {i}: Ri_msg={Ri_msg}")

        #sum all Ri_msg
        Rsum = (Rsum + Ri_msg) % q

        # prepare next Ri
        hmsg =  hashlib.sha256()
        hmsg.update(int_to_bytes(Ri))
        Ri = int_from_bytes(hmsg.digest())

    inverseG = pow(g, p-2, p) 
    key = pow(inverseG, Rsum, p)
    print(f"Key: {key}")

if __name__ == "__main__":
    main()
