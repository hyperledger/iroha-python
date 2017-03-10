"""Python library for Hyperledger Iroha."""

# ed25519 library uses terms "signing key" for "private key",
# and "verifying key" for "public key".
# This library also strips '=' from base64-encoded byte strings,
# so all inputs/outputs are converted manually to/from binary representation.


from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import base64

from collections import namedtuple

import ed25519
import sha3

import api_pb2_grpc as api_pb2_grpc
import grpc

KeyPair = namedtuple('KeyPair', ['private_key', 'public_key'])


def create_key_pair():
    # Mind the private/public key order!
    private_key, public_key = ed25519.create_keypair()
    private_key_base64 = base64.standard_b64encode(private_key.to_bytes())
    public_key_base64 = base64.standard_b64encode(public_key.to_bytes())
    return KeyPair(private_key=private_key_base64,
                   public_key=public_key_base64)


def sign(key_pair, message):
    private_key_bytes = base64.standard_b64decode(key_pair.private_key)
    private_key = ed25519.SigningKey(private_key_bytes)
    signature_bytes = private_key.sign(message)
    return base64.standard_b64encode(signature_bytes)


def verify(public_key, signature, message):
    try:
        public_key_bytes = base64.standard_b64decode(public_key)
        public_key = ed25519.VerifyingKey(public_key_bytes)
        signature_bytes = base64.standard_b64decode(signature)
        public_key.verify(signature_bytes, message)
        return True
    except ed25519.BadSignatureError:
        return False


def sha3_256(message):
    digest_bytes = sha3.sha3_256(message).digest()
    return base64.standard_b64encode(digest_bytes)


def sha3_384(message):
    digest_bytes = sha3.sha3_384(message).digest()
    return base64.standard_b64encode(digest_bytes)


def sha3_512(message):
    digest_bytes = sha3.sha3_512(message).digest()
    return base64.standard_b64encode(digest_bytes)


class Kannagi:
    def __init__(self):
        # ToDo configurable
        channel = grpc.insecure_channel('localhost:50051')
        self.sumeragi_stub = api_pb2_grpc.SumeragiStub(channel)
        self.asset_repo_stub = api_pb2_grpc.AssetRepositoryStub(channel)
        self.tx_repo_stub = api_pb2_grpc.TransactionRepositoryStub(channel)

    def torii(self, tx):
        res = self.sumeragi_stub.Torii(
            tx
        )
        # ToDo  log class
        print("client received: " + res.message)
        return res

    def assetRepository(self, query):
        return self.asset_repo_stub.find(query)

    def transationRepository(self, query):
        return self.transationRepository(query)
