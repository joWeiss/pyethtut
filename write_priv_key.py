#!/usr/bin/env python3.6
from secp256k1 import PrivateKey

if __name__ == '__main__':
    k = PrivateKey(None)
    with open('priv_key', 'w') as f:
        f.write(k.serialize())
