from protos.api_pb2 import Transaction, Asset
from enum import Enum
from datetime import datetime


class TransactionBuilder:
    class AssetType(Enum):
        ASSET = 1
        DOMAIN = 2
        ACCOUNT = 3
        PEER = 4
        SIMPLE_ASSET = 5
        NONE = 6

    def __init__(self, type, senderPublicKey):
        self.tx = Transaction()
        self.type = type
        self.senderPublicKey = senderPublicKey
        self.receiverPublicKey = ""
        self.txSignatures = []

        self.object = {}
        self.object_type = TransactionBuilder.AssetType.NONE

    # for Transfer
    def __init__(self, type, senderPublicKey, receiverPublicKey):
        self.tx = Transaction()
        self.type = type
        self.senderPublicKey = senderPublicKey
        self.receiverPublicKey = receiverPublicKey
        self.txSignatures = []

        self.object = {}
        self.object_type = TransactionBuilder.AssetType.NONE


    def add_txSignature(self, sig, hash_):
        self.txSignatures.append([sig, hash_])
        return self

    def set_asset(self, asset_):
        self.object_type = TransactionBuilder.AssetType.ASSET
        self.object[self.object_type] = asset_
        return self

    def set_domain(self, domain_):
        self.object_type = TransactionBuilder.AssetType.DOMAIN
        self.object[self.object_type] = domain_
        return self

    def set_account(self, account_):
        self.object_type = TransactionBuilder.AssetType.ACCOUNT
        self.object[self.object_type] = account_
        return self

    def set_peer(self, peer_):
        self.object_type = TransactionBuilder.AssetType.PEER
        self.object[self.object_type] = peer_
        return self

    def set_simple_asset(self, simple_asset_):
        self.object_type = TransactionBuilder.AssetType.SIMPLE_ASSET
        self.object[self.object_type] = simple_asset_
        return self

    def set_receive_public_key(self, receiver_publicKey_):
        self.receiverPublicKey = receiver_publicKey_
        return self


    # WIP
    def build(self):
        if self.object_type == TransactionBuilder.AssetType.ASSET:
            return Transaction(
                type=self.type,
                senderPubkey=self.senderPublicKey,
                receivePubkey=self.receiverPublicKey,
                hash="",  # This is WIP!! dangerous
                timestamp=int(datetime.now().timestamp()),
                asset=self.object[self.object_type]
            )
        elif self.object_type == TransactionBuilder.AssetType.ACCOUNT:
            return Transaction(
                type=self.type,
                senderPubkey=self.senderPublicKey,
                receivePubkey=self.receiverPublicKey,
                hash="",  # This is WIP!! dangerous
                timestamp=int(datetime.now().timestamp()),
                account=self.object[self.object_type]
            )
        elif self.object_type == TransactionBuilder.AssetType.DOMAIN:
            return Transaction(
                type=self.type,
                senderPubkey=self.senderPublicKey,
                receivePubkey=self.receiverPublicKey,
                hash="",  # This is WIP!! dangerous
                timestamp=int(datetime.now().timestamp()),
                domain=self.object[self.object_type]
            )
        elif self.object_type == TransactionBuilder.AssetType.SIMPLE_ASSET:
            return Transaction(
                type=self.type,
                senderPubkey=self.senderPublicKey,
                receivePubkey=self.receiverPublicKey,
                hash="",  # This is WIP!! dangerous
                timestamp=int(datetime.now().timestamp()),
                simpleAsset=self.object[self.object_type]
            )
