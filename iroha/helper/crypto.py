# coding=utf-8
import ed25519_sha3
import sha3
import base64
import time

from collections import namedtuple

class KeyPair(namedtuple('KeyPair', ['raw_private_key', 'raw_public_key'])):

    def encode(self, value):
        return base64.b64encode(value)

    @property
    def private_key(self):
        return self.encode(self.raw_private_key)

    @property
    def public_key(self):
        return self.encode(self.raw_public_key)

def create_key_pair():
    # Mind the private/public key order!
    public_key, private_key = ed25519_sha3.create_keypair()
    return KeyPair(raw_private_key=private_key, raw_public_key=public_key)

def sign(key_pair, message):
    raw_signature = ed25519_sha3.sign(message, key_pair.raw_public_key, key_pair.raw_private_key)
    return base64.b64encode(raw_signature)

def verify(public_key, signature, message):
    public_key = base64.b64decode(public_key)
    signature = base64.b64decode(signature)
    return bool(ed25519_sha3.verify(message,signature,public_key))

def sha3_256(message):
    digest_bytes = sha3.sha3_256(message).digest()
    return base64.standard_b64encode(digest_bytes)


def b64encode(message):
    return base64.standard_b64encode(message)

def b64decode(message):
    return base64.standard_b64decode(message)


def sign_hash(proto):
    return sha3.sha3_256(proto.SerializeToString()).digest()


def db_encode(message):
    return b64encode(message).decode()

def db_decode(message):
    return b64decode(message.encode())

def now():
    return int(time.time()*1000.0)

