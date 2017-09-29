"""Python library for Hyperledger Iroha."""


from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from src.helper import crypto
from src.creator import Creator
from src.network.connection import Connection

from schema.commands_pb2 import Command

# typedef CommandName for access to iroha.XX
CreateAccount = Command.CreateAccount
AddSignatory = Command.AddSignatory
RemoveSignatory = Command.RemoveSignatory

CreateDomain = Command.CreateDomain
CreateAsset = Command.CreateAsset

AddAssetQuantity = Command.AddAssetQuantity
SetAccountQuorum = Command.SetAccountQuorum
TransferAsset = Command.TransferAsset

def keygen():
    return crypto.create_key_pair()


def genCreator(creator_account_id,keys):
    creator = Creator()
    creator.set_account_id(creator_account_id)
    creator.set_keys(keys)
    return creator


def connection(ip,port):
    connect = Connection()
    connect.setUp(ip,port)
    return connect
