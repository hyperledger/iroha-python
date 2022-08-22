#!/usr/bin/env python3
#
# Copyright Soramitsu Co., Ltd. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""
This example demonstrates how to use atomic batch of multiple transactions.
The batch is atomic - so it means that it would be committed only and only if all transactions
would be committed, otherwise entire batch (all transactions) would be rejected.
Transactions in batch can be authored by multiple accounts - each account signs
his transactions.

Note that to create batch to be signed by multiple accounts extra params need to be used:
`creator_account` and `quorum`.
"""

import binascii
from iroha import Iroha, IrohaGrpc, IrohaCrypto
import os
import sys
from grpc import RpcError, StatusCode
import inspect  # inspect.stack(0)
from functools import wraps
from utilities.errorCodes2Hr import get_proper_functions_for_commands


IROHA_HOST_ADDR = os.getenv('IROHA_HOST_ADDR', '127.0.0.1')
IROHA_PORT = os.getenv('IROHA_PORT', '50051')
ADMIN_ACCOUNT_ID = os.getenv('ADMIN_ACCOUNT_ID', 'admin@test')
ADMIN_PRIVATE_KEY = os.getenv(
    'ADMIN_PRIVATE_KEY', 'f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70')

print("""

PLEASE ENSURE THAT MST IS ENABLED IN IROHA CONFIG

""")

if sys.version_info[0] < 3:
    raise Exception('Python 3 or a more recent version is required.')

iroha = Iroha(ADMIN_ACCOUNT_ID)
net = IrohaGrpc(f'{IROHA_HOST_ADDR}:{IROHA_PORT}')

alice_private_keys = [
    'f101537e319568c765b2cc89698325604991dca57b9716b58016b253506caba1',
    'f101537e319568c765b2cc89698325604991dca57b9716b58016b253506caba2'
]

bob_private_keys = [
    'f101537e319568c765b2cc89698325604991dca57b9716b58016b253506caba3',
    'f101537e319568c765b2cc89698325604991dca57b9716b58016b253506caba4'
]


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
    print(f'Transaction "{get_commands_from_tx(transaction)}",'
          f' hash = {hex_hash}, creator = {creator_id}')
    net.send_tx(transaction)
    print_transaction_status(transaction)


def print_transaction_status(transaction):
    commands = get_commands_from_tx(transaction)
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
def send_batch_and_print_status(transactions):
    global net
    net.send_txs(transactions)
    for tx in transactions:
        hex_hash = binascii.hexlify(IrohaCrypto.hash(tx))
        print('\t' + '-' * 20)
        creator = tx.payload.reduced_payload.creator_account_id
        print(f'Transaction hash = {hex_hash}, creator = {creator}')
        print_transaction_status(tx)


@trace
def prepare_users():
    global iroha
    init_cmds = [
        iroha.command('CreateAsset', asset_name='bitcoin',
                      domain_id='test', precision=2),
        iroha.command('CreateAsset', asset_name='dogecoin',
                      domain_id='test', precision=2),
        iroha.command('AddAssetQuantity',
                      asset_id='bitcoin#test', amount='100000'),
        iroha.command('AddAssetQuantity',
                      asset_id='dogecoin#test', amount='20000'),
        iroha.command('CreateAccount', account_name='alice', domain_id='test',
                      public_key=public_key_from_private(alice_private_keys[0])),
        iroha.command('CreateAccount', account_name='bob', domain_id='test',
                      public_key=public_key_from_private(bob_private_keys[0])),
        iroha.command('TransferAsset', src_account_id='admin@test', dest_account_id='alice@test',
                      asset_id='bitcoin#test', description='init top up', amount='100000'),
        iroha.command('TransferAsset', src_account_id='admin@test', dest_account_id='bob@test',
                      asset_id='dogecoin#test', description='init doge', amount='20000')
    ]
    init_tx = iroha.transaction(init_cmds)
    IrohaCrypto.sign_transaction(init_tx, ADMIN_PRIVATE_KEY)
    send_transaction_and_print_status(init_tx)


@trace
def add_keys_and_set_quorum():
    add_key_and_set_quorum(account_id='alice@test', account_private_key=alice_private_keys[0],
                           account_private_key_to_add=alice_private_keys[1])

    add_key_and_set_quorum(account_id='bob@test', account_private_key=bob_private_keys[0],
                           account_private_key_to_add=bob_private_keys[1])


@trace
def add_key_and_set_quorum(account_id, account_private_key, account_private_key_to_add):
    public_key_to_add_signatory = public_key_from_private(account_private_key_to_add)
    iroha_local = Iroha(account_id)
    cmds = [
        iroha_local.command('AddSignatory', account_id=account_id,
                            public_key=public_key_to_add_signatory),
        iroha_local.command('SetAccountQuorum',
                            account_id=account_id, quorum=2)
    ]
    tx = iroha_local.transaction(cmds)
    IrohaCrypto.sign_transaction(tx, account_private_key)
    send_transaction_and_print_status(tx)


def public_key_from_private(private_key: "str or bytes"):
    return IrohaCrypto.derive_public_key(private_key).decode('utf-8')


@trace
def alice_creates_exchange_batch():
    alice_tx = iroha.transaction(
        [iroha.command(
            'TransferAsset', src_account_id='alice@test', dest_account_id='bob@test',
            asset_id='bitcoin#test', amount='1'
        )],
        creator_account='alice@test',
        quorum=2
    )
    bob_tx = iroha.transaction(
        [iroha.command(
            'TransferAsset', src_account_id='bob@test', dest_account_id='alice@test',
            asset_id='dogecoin#test', amount='2'
        )],
        creator_account='bob@test'
        # we intentionally omit here bob's quorum, since alice is the originator of the exchange and in general case
        # alice does not know bob's quorum.
        # bob knowing own quorum in case of accept should sign the tx using all the number of missing keys at once
    )
    iroha.batch([alice_tx, bob_tx], atomic=True)
    # sign transactions only after batch meta creation
    IrohaCrypto.sign_transaction(alice_tx, *alice_private_keys)
    send_batch_and_print_status([alice_tx, bob_tx])


@trace
def bob_accepts_exchange_request():
    global net
    q = IrohaCrypto.sign_query(
        Iroha('bob@test').query('GetPendingTransactions'),
        bob_private_keys[0]
    )
    pending_transactions = net.send_query(q)
    for tx in pending_transactions.transactions_response.transactions:
        if tx.payload.reduced_payload.creator_account_id == 'alice@test':
            # we need do this temporarily, otherwise accept will not reach MST engine
            del tx.signatures[:]
        else:
            IrohaCrypto.sign_transaction(tx, *bob_private_keys)
    send_batch_and_print_status(
        pending_transactions.transactions_response.transactions)


@trace
def check_no_pending_txs(account_id: str, account_private_key):
    print(' ~~~ No pending txs expected:')
    print(
        net.send_query(
            IrohaCrypto.sign_query(
                iroha.query('GetPendingTransactions',
                            creator_account=account_id),
                account_private_key
            )
        )
    )
    print(' ~~~')


@trace
def bob_declines_exchange_request():
    print("""
    
    IT IS EXPECTED HERE THAT THE BATCH WILL FAIL STATEFUL VALIDATION
    
    """)
    global net
    q = IrohaCrypto.sign_query(
        Iroha('bob@test').query('GetPendingTransactions'),
        bob_private_keys[0]
    )
    pending_transactions = net.send_query(q)
    for tx in pending_transactions.transactions_response.transactions:
        if tx.payload.reduced_payload.creator_account_id == 'alice@test':
            # we need do this temporarily, otherwise accept will not reach MST engine
            del tx.signatures[:]
        else:
            # intentionally alice keys were used to fail bob's txs
            IrohaCrypto.sign_transaction(tx, *alice_private_keys)
            # zeroes as private keys are also acceptable
    send_batch_and_print_status(
        pending_transactions.transactions_response.transactions)


if __name__ == '__main__':
    try:
        prepare_users()
        add_keys_and_set_quorum()

        alice_creates_exchange_batch()
        bob_accepts_exchange_request()
        check_no_pending_txs(account_id='bob@test', account_private_key=bob_private_keys[0])

        alice_creates_exchange_batch()
        try:
            bob_declines_exchange_request()  # the bath is expected to fail
        except RuntimeError:
            pass
        check_no_pending_txs(account_id='bob@test', account_private_key=bob_private_keys[0])
    except RpcError as rpc_error:
        if rpc_error.code() == StatusCode.UNAVAILABLE:
            print(f'[E] Iroha is not running in address:'
                  f'{IROHA_HOST_ADDR}:{IROHA_PORT}!')
        else:
            print(e)
    except RuntimeError as e:
        print(e)
