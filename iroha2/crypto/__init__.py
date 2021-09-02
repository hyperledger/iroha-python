from ..sys.iroha_crypto import Hash, PublicKey, Signature
from ..sys import hash as _hash, sign as _sign, KeyPair


class Hash:
    def __init__(self, seq):
        self.hash = _hash(seq)

    def to_rust(self):
        return self.hash


class Signature:
    def __init__(self, keys, payload):
        self.sign = _sign(keys, payload)

    def to_rust(self):
        return self.sign
