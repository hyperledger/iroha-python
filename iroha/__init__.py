"""Python library for Hyperledger Iroha."""


from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from iroha.helper import crypto, logger
from iroha.creator import Creator
from iroha.network.connection import Connection

from schema.commands_pb2 import Command
from schema.endpoint_pb2 import ToriiResponse, TxStatus
from schema.response_pb2 import GetAccountAssets,GetTransactions,GetAccount,GetAccountAssetTransactions,GetAccountTransactions,GetSignatories

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
    """
    Generate keypair ( public key and private key )

    Returns:
        `KeyPair`: base64 encoded ed25519 with sha3_256 keypair [ public_key, private_key ].
    """
    return crypto.create_key_pair()


def gen_creator(creator_account_id,keys,connection):
    """
    Generate creator. ( reference: `Creator` )

    Args:
        creator_account_id ( str ): creator account id
        keys ( []`KeyPair` ) : array of keypair. this means signatories of creator.
        connection ( `Connection` ) : connection used to connect iroha.
            `Conncect` can be got by iroha.connection(ip,port).

    Returns:
        `Creator`: Generated creator with account_id, signatories(keys) and connection

    """
    creator = Creator(creator_account_id,keys,connection)
    return creator


def gen_connection(ip,port):
    """
    Generate Connection used to connect iroha.

    Args:
        ip: ip address string of iroha.
        port: port number string of iroha.

    Returns:
        `Connection`: connector used to connect iroha.
    """
    connect = Connection(ip=ip,port=port)
    return connect

def setDebugLog():
    """
    Set Debug Output Level : Debug ( means many debug message )
    """
    logger.setDebug()
def setInfoLog():
    """
    Set Debug Output Level : Info
    """
    logger.setInfo()
def setWarningLog():
    """
    Set Debug Output Level : Warning ( means few debug message )
    """
    logger.setWarning()
