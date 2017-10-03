# coding=utf-8
from iroha.helper import ed25519
import sha3
import base64
import time

from collections import namedtuple

KeyPair = namedtuple('KeyPair', ['private_key', 'public_key'])

def create_key_pair():
    # Mind the private/public key order!
    public_key, private_key = ed25519.generate()
    return KeyPair(private_key=private_key,
                   public_key=public_key)

def sign(key_pair, message):
    return ed25519.sign(message,key_pair.public_key,key_pair.private_key)

def verify(public_key, signature, message):
    return ed25519.verify(message,signature,public_key)

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

