import argparse
import hashlib
from settings import p, q, R0, g


def int_to_bytes(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')


def int_from_bytes(xbytes: bytes) -> int:
    return int.from_bytes(xbytes, 'big')


def get_key(t_start, t_end, tag):
    """
    Return the decoding key given the index (time) and a tag
    """
    Ri = R0
    Rsum = 0
    for i in range(t_end+1):
        
        if i >= t_start:
            hmsg = hashlib.sha256()
            hmsg.update(int_to_bytes(Ri) + tag.encode("utf8"))
            ri_tag_digest = int_from_bytes(hmsg.digest())
            print(f"Iteration {i}: ri_tag_digest={ri_tag_digest}")

            # sum all ri_tag_digest
            Rsum = (Rsum + ri_tag_digest) % q

        # prepare next Ri
        hmsg = hashlib.sha256()
        hmsg.update(int_to_bytes(Ri))
        Ri = int_from_bytes(hmsg.digest())

    inverseG = pow(g, p-2, p)
    key = pow(inverseG, Rsum, p)
    return key


def main():
    parser = argparse.ArgumentParser(description='Create a key')
    parser.add_argument('start_time', type=int,
                        help='starting time (integer)')
    parser.add_argument('end_time', type=int , help='ending time (integer)')
    parser.add_argument('tag', type=str,
                        help='tag m (string)')
    args = parser.parse_args()
    t_start = args.start_time
    t_end = args.end_time
    tag = args.tag

    key = get_key(t_start, t_end, tag)

    print(f"Key: {key}")


if __name__ == "__main__":
    main()
