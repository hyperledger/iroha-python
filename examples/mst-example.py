#!/usr/bin/env python3
# this code was originally coded by user: Leo (@iptelephony)

"""
The example demonstrates how to use multi-signature transactions.
MST are transactions which must be signed by multiple keys.
MST can contain multiple transactions, to be signed by multiple accounts.
"""

import os
import sys
import binascii
import time
from grpc import RpcError, StatusCode
import inspect  # inspect.stack(0)
from iroha import Iroha, IrohaGrpc, IrohaCrypto
from functools import wraps
from iroha.primitive_pb2 import can_set_my_account_detail, can_set_my_quorum
from utilities.errorCodes2Hr import get_proper_functions_for_commands


if sys.version_info[0] < 3:
    raise Exception('Python 3 or a more recent version is required.')

IROHA_HOST_ADDR = os.getenv('IROHA_HOST_ADDR', '127.0.0.1')
IROHA_PORT = os.getenv('IROHA_PORT', '50051')
ADMIN_ACCOUNT_ID = os.getenv('ADMIN_ACCOUNT_ID', 'admin@test')

ADMIN_PRIVATE_KEY = os.getenv(
    'ADMIN_PRIVATE_KEY', 'f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70')
ADMIN_PUBLIC_KEY = IrohaCrypto.derive_public_key(ADMIN_PRIVATE_KEY)

iroha = Iroha(ADMIN_ACCOUNT_ID)
net = IrohaGrpc(f'{IROHA_HOST_ADDR}:{IROHA_PORT}')

group = {
    'account': "group@test",
    'private_key': 'f101537e319568c765b2cc89698325604991dca57b9716b58016b253506caba1'
}
group['public_key'] = IrohaCrypto.derive_public_key(group['private_key'])

alice = {
    'account': "alice@test",
    'private_key': 'f101537e319568c765b2cc89698325604991dca57b9716b58016b253506caba2',
}
alice['public_key'] = IrohaCrypto.derive_public_key(alice['private_key'])

bob = {
    'account': "bob@test",
    'private_key': 'f101537e319568c765b2cc89698325604991dca57b9716b58016b253506caba3',
}
bob['public_key'] = IrohaCrypto.derive_public_key(bob['private_key'])

receiver = {
    'account': "receiver@test",
    'private_key': 'f101537e319568c765b2cc89698325604991dca57b9716b58016b253506caba4',
}
receiver['public_key'] = IrohaCrypto.derive_public_key(receiver['private_key'])


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
def create_user_accounts():
    tx = iroha.transaction([
        create_account(alice['account'], alice['public_key']),
        create_account(bob['account'], bob['public_key']),
        create_account(group['account'], group['public_key']),
        create_account(receiver['account'], receiver['public_key'])
    ])
    """
    Create users
    """
    IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)
    send_transaction_and_print_status(tx)


@trace
def create_account(account_id, public_key):
    account_short_id, domain = account_id.split("@")
    return iroha.command('CreateAccount', account_name=account_short_id, domain_id=domain,
                         public_key=public_key)


@trace
def transfer_coin_from_admin(dest_id, asset_id, amount):
    """
    Transfer asset from admin to another account
    """
    tx = iroha.transaction([
        iroha.command('TransferAsset', src_account_id=ADMIN_ACCOUNT_ID, dest_account_id=dest_id,
                      asset_id=asset_id, description='init top up', amount=amount)
    ])
    IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)
    send_transaction_and_print_status(tx)


@trace
def transfer_coin_from_group(dest_id, asset_id, amount, creator_id, creator_private_key):
    """
    Transfer from the group account to another account.
    This transaction requires 2 sigs to proceed. After the creator has signed, it will be pending.
    """
    src_account_id = group['account']
    iroha2 = Iroha(creator_id)
    tx = iroha2.transaction([
        iroha2.command('TransferAsset', src_account_id=src_account_id, dest_account_id=dest_id,
                       asset_id=asset_id, description='transfer', amount=amount)
    ], creator_account=src_account_id, quorum=2)
    IrohaCrypto.sign_transaction(tx, creator_private_key)
    send_transaction_and_print_status(tx)


@trace
def get_account_assets(account_id):
    """
    List all the assets of userone@domain
    """
    query = iroha.query('GetAccountAssets', account_id=account_id)
    IrohaCrypto.sign_query(query, ADMIN_PRIVATE_KEY)

    response = net.send_query(query)
    data = response.account_assets_response.account_assets
    print(f'Account = {account_id}')
    for asset in data:
        print(f'Asset id = {asset.asset_id}, balance = {asset.balance}')


@trace
def get_pending_transactions():
    query = IrohaCrypto.sign_query(Iroha(group['account']).query('GetPendingTransactions'), ADMIN_PRIVATE_KEY)
    pending_transactions = net.send_query(query)
    print(len(pending_transactions.transactions_response.transactions))
    for tx in pending_transactions.transactions_response.transactions:
        print(f'creator: {tx.payload.reduced_payload.creator_account_id}')


@trace
def setup_group_account():
    iroha = Iroha(group['account'])
    cmds = [
        iroha.command('AddSignatory', account_id=group['account'], public_key=ADMIN_PUBLIC_KEY),
        iroha.command('AddSignatory', account_id=group['account'], public_key=alice['public_key']),
        iroha.command('AddSignatory', account_id=group['account'], public_key=bob['public_key']),
        iroha.command('GrantPermission', account_id='admin@test', permission=can_set_my_quorum),
    ]
    tx = iroha.transaction(cmds)
    IrohaCrypto.sign_transaction(tx, group['private_key'])
    send_transaction_and_print_status(tx)


@trace
def mint_asset(asset_id, amount):
    """
    Add provided number of assets
    """
    tx = iroha.transaction([
        iroha.command('AddAssetQuantity', asset_id=asset_id, amount=amount)
    ])
    IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)
    send_transaction_and_print_status(tx)


@trace
def sign_pending_transactions(account_id, private_key):
    global net
    query = IrohaCrypto.sign_query(Iroha(account_id).query('GetPendingTransactions'), private_key)
    pending_transactions = net.send_query(query)
    print(len(pending_transactions.transactions_response.transactions))
    for tx in pending_transactions.transactions_response.transactions:
        print('creator: {}'.format(tx.payload.reduced_payload.creator_account_id))
        if tx.payload.reduced_payload.creator_account_id == account_id:
            # we need do this temporarily, otherwise accept will not reach MST engine
            print(f'tx: {tx}')
            del tx.signatures[:]
            print(f'tx: {tx}')
            IrohaCrypto.sign_transaction(tx, private_key)
            send_transaction_and_print_status(tx)


@trace
def change_quorum(account_id):
    tx = iroha.transaction([
        iroha.command('SetAccountQuorum', account_id=account_id, quorum=2)
    ])
    IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)
    send_transaction_and_print_status(tx)


if __name__ == '__main__':
    try:
        print('1. creating accounts')
        create_user_accounts()
        setup_group_account()

        print('2. mint coins and give to group#test account')
        mint_asset('coin#test', '1000.00')
        transfer_coin_from_admin(group['account'], 'coin#test', '42.00')

        print('3. alice@test initiates transfer 14.0 from group@test to receiver@test')
        transfer_coin_from_group(receiver['account'], 'coin#test', '14.00', alice['account'], alice['private_key'])

        print('4. bob@test countersigns transfer')
        sign_pending_transactions(group['account'], bob['private_key'])

        time.sleep(5)
        get_account_assets(receiver['account'])
        get_account_assets(group['account'])

        print('5. bob@test initiates transfer 7.0 from group@test to receiver@test')
        transfer_coin_from_group(receiver['account'], 'coin#test', '7.00', bob['account'], bob['private_key'])

        print('6. alice@test countersigns transfer')
        sign_pending_transactions(group['account'], alice['private_key'])

        time.sleep(5)
        get_account_assets(receiver['account'])
        get_account_assets(group['account'])
    except RpcError as rpc_error:
        if rpc_error.code() == StatusCode.UNAVAILABLE:
            print(f'[E] Iroha is not running in address:'
                  f'{IROHA_HOST_ADDR}:{IROHA_PORT}!')
        else:
            print(e)
    except RuntimeError as e:
        print(e)
