"""Python library for Hyperledger Iroha."""

# ed25519 library uses terms "signing key" for "private key",
# and "verifying key" for "public key".
# This library also strips '=' from base64-encoded byte strings,
# so all inputs/outputs are converted manually to/from binary representation.


from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from collections import namedtuple

import ed25519
import grpc
import sha3

from protos.api_pb2 import Asset,BaseObject,Query
import protos.api_pb2_grpc as api_pb2_grpc

from transaction import TransactionBuilder


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


def getAccountInfo(publicKey):
    query = Query(
        senderPubkey=publicKey,
        type="account"
    )


class Kannagi:
    def __init__(self):
        # ToDo configurable
        channel = grpc.insecure_channel('172.17.0.3:50051')
        self.sumeragi_stub = api_pb2_grpc.SumeragiStub(channel)
        self.asset_repo_stub = api_pb2_grpc.AssetRepositoryStub(channel)
        self.tx_repo_stub = api_pb2_grpc.TransactionRepositoryStub(channel)

    def send(self, sender, receiver, name, value):
        asset = Asset(
            publicKey=sender,
            name=name,
            value={
                "value":value
            }
        )
        tx = TransactionBuilder("transfer", sender, receiver).set_asset(asset).build()
        self.torii(tx)

    def torii(self, tx):
        res = self.sumeragi_stub.Torii(
            tx
        )
        # ToDo  log class
        print("client received: " + res.message)
        return res

    def get_account_info(self, publicKey):
        query = Query(
            senderPubkey=publicKey,
            type="account"
        )
        return self.asset_repo_stub.find(query)

    def get_asset_info(self, publicKey, assetName):
        query = Query(
            senderPubkey=publicKey,
            type="asset",
            value={
                "name": BaseObject(valueString=assetName)
            }
        )
        return self.asset_repo_stub.find(query)

    def assetRepository(self, query):
        return self.asset_repo_stub.find(query)

    def get_all_transation(self):
        # in now, don't use query
        query = Query()
        return self.tx_repo_stub.find(query)
