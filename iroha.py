"""Python library for Hyperledger Iroha."""

# ed25519 library uses terms "signing key" for "private key",
# and "verifying key" for "public key".


from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from collections import namedtuple

import ed25519
import sha3


KeyPair = namedtuple('KeyPair', ['private_key', 'public_key'])


def create_key_pair(seed=None):
    """Create a private/public key pair.

    Use a system randomness source or a 32-byte seed if supplied.
    """
    if seed is None:
        # Mind the private/public key order!
        private_key, public_key = ed25519.create_keypair()
    else:
        assert len(seed) == 32
        private_key = ed25519.SigningKey(seed)
        public_key = private_key.get_verifying_key()
    return KeyPair(private_key=private_key.to_bytes(),
                   public_key=public_key.to_bytes())


def sign(key_pair, message):
    lib_private_key = ed25519.SigningKey(key_pair.private_key)
    return lib_private_key.sign(message)


def verify(public_key, signature, message):
    try:
        lib_public_key = ed25519.VerifyingKey(public_key)
        lib_public_key.verify(signature, message)
        return True
    except ed25519.BadSignatureError:
        return False


def sha3_256(message):
    return sha3.sha3_256(message).digest()


def sha3_384(message):
    return sha3.sha3_384(message).digest()


def sha3_512(message):
    return sha3.sha3_512(message).digest()
