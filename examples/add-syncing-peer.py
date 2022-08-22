"""
This example demonstrates how to add new peer, when new peer is syncing node.
Details about how to add new peer to the network are here:
https://iroha.readthedocs.io/en/develop/maintenance/add_peer.html
"""

import os
import sys
from functools import wraps
from iroha import primitive_pb2, IrohaCrypto, binascii, IrohaGrpc, Iroha
from grpc import RpcError, StatusCode
import inspect  # inspect.stack(0)
from utilities.errorCodes2Hr import get_proper_functions_for_commands


if sys.version_info[0] < 3:
    raise Exception('Python 3 or a more recent version is required.')


ADMIN_ACCOUNT_ID = os.getenv('ADMIN_ACCOUNT_ID', 'admin@test')
ADMIN_PRIVATE_KEY = os.getenv(
    'ADMIN_PRIVATE_KEY', 'f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70')

iroha_admin = Iroha(ADMIN_ACCOUNT_ID)


IROHA_HOST_ADDR = os.getenv('IROHA_HOST_ADDR', 'localhost')
IROHA_PORT = os.getenv('IROHA_PORT', '50051')

NEW_PEER_PUBLIC_KEY = os.getenv(
    'NEW_PEER_PUBLIC_KEY', 'edfa0f05d019c0a0dd6ca491e0c2e78d1ef4148ffa10ffc72f48a0fd6af08e5b')
NEW_PEER_ADDRESS = os.getenv('NEW_PEER_ADDRESS', 'localhost')
NEW_PEER_IROHA_PORT = os.getenv('NEW_PEER_IROHA_PORT', '50050')
NEW_PEER_FULL_ADDRESS = f'{NEW_PEER_ADDRESS}:{NEW_PEER_IROHA_PORT}'

net = IrohaGrpc(f'{IROHA_HOST_ADDR}:{IROHA_PORT}')
net_new_peer = IrohaGrpc(NEW_PEER_FULL_ADDRESS)


def trace(func):
    """
    A decorator for tracing methods' begin/end execution points
    """
    @wraps(func)
    def tracer(*args, **kwargs):
        name = func.__name__
        stack_size = int(len(inspect.stack(0)) / 2)  # @wraps(func) is also increasing the size
        indent = stack_size*'\t'
        print(f'{indent} > Entering "{name}": args: {args}')
        result = func(*args, **kwargs)
        print(f'{indent} < Leaving "{name}"')
        return result

    return tracer


@trace
def add_peers(iroha_connection, peer_address: str, peer_public_key: str):
    peer = primitive_pb2.Peer(address=peer_address, peer_key=peer_public_key, syncing_peer=True)
    tx = iroha_connection.transaction([
        iroha_connection.command('AddPeer', peer=peer)
    ])
    IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)
    send_transaction_and_print_status(tx)


@trace
def send_transaction_and_print_status(transaction):
    hex_hash = binascii.hexlify(IrohaCrypto.hash(transaction))
    creator_id = transaction.payload.reduced_payload.creator_account_id
    commands = get_commands_from_tx(transaction)
    print(f'Transaction "{commands}",'
          f' hash = {hex_hash}, creator = {creator_id}')
    net.send_tx(transaction)
    for i, status in enumerate(net.tx_status_stream(transaction)):
        status_name, status_code, error_code = status
        print(f"{i}: status_name={status_name}, status_code={status_code}, "
              f"error_code={error_code}")
        if status_name in ('STATEFUL_VALIDATION_FAILED', 'STATELESS_VALIDATION_FAILED', 'REJECTED'):
            error_code_hr = get_proper_functions_for_commands(commands)(error_code)
            raise RuntimeError(f"{status_name} failed on tx: "
                               f"{transaction} due to reason {error_code}: "
                               f"{error_code_hr}")


def get_commands_from_tx(transaction):
    commands_from_tx = []
    for command in transaction.payload.reduced_payload.__getattribute__("commands"):
        listed_fields = command.ListFields()
        commands_from_tx.append(listed_fields[0][0].name)
    return commands_from_tx


@trace
def print_peers(text: str, net_to_query: IrohaGrpc):
    print('-------', text, '-------')
    query = iroha_admin.query('GetPeers')
    IrohaCrypto.sign_query(query, ADMIN_PRIVATE_KEY)
    response = net_to_query.send_query(query)
    peers_response = response.peers_response.peers
    for i, p in enumerate(peers_response):
        print(i, p)


if __name__ == '__main__':
    try:
        print(f'!!!New peer in address {NEW_PEER_FULL_ADDRESS} should work now! '
              f'It not the script {sys.argv[0]} would fail!!!')
        print_peers('Peers before adding new one', net)
        add_peers(iroha_connection=iroha_admin, peer_address=NEW_PEER_FULL_ADDRESS,
                  peer_public_key=NEW_PEER_PUBLIC_KEY)
        print_peers('Peers after adding the new one - query to old peer', net)
        print_peers('Peers after adding the new one - query to new peer', net_new_peer)
    except RpcError as rpc_error:
        if rpc_error.code() == StatusCode.UNAVAILABLE:
            print(f'[E] Iroha is not running in address: '
                  f'{IROHA_HOST_ADDR}:{IROHA_PORT}!')
        else:
            print(e)
    except RuntimeError as e:
        print(e)
