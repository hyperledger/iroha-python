#!/usr/bin/env python3
"""
This example demonstrates how to use pagination:
https://iroha.readthedocs.io/en/develop/develop/api/queries.html#result-pagination
to change ordering of results into descending order.
"""
import os
import sys
import binascii
import datetime
import inspect  # inspect.stack(0)
from iroha import IrohaCrypto, Iroha, IrohaGrpc, queries_pb2
from functools import wraps
from time import sleep
from grpc import RpcError, StatusCode
from utilities.errorCodes2Hr import get_proper_functions_for_commands


if sys.version_info[0] < 3:
    raise Exception('Python 3 or a more recent version is required.')


IROHA_HOST_ADDR = os.getenv('IROHA_HOST_ADDR', '127.0.0.1')
IROHA_PORT = os.getenv('IROHA_PORT', '50051')
ADMIN_ACCOUNT_ID = os.getenv('ADMIN_ACCOUNT_ID', 'admin@test')
ADMIN_PRIVATE_KEY = os.getenv(
    'ADMIN_PRIVATE_KEY', 'f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70')


user_account = 'aa@test'
user_private_key = '1234567890123456789012345678901234567890123456789012345678901234'
user_public_key = IrohaCrypto.derive_public_key(user_private_key)

iroha = Iroha(ADMIN_ACCOUNT_ID)
net = IrohaGrpc(f'{IROHA_HOST_ADDR}:{IROHA_PORT}')

ASSET_ID = 'lemurcoin#test'


def trace(func):
    """
    A decorator for tracing methods' begin/end execution points
    """
    @wraps(func)
    def tracer(*args, **kwargs):
        name = func.__name__
        stack_size = int(len(inspect.stack(0)) / 2)  # @wraps(func) is also increasing the size
        indent = stack_size*'\t'
        print(f'{indent} > Entering "{name}"')
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
def create_account(user_account: str, user_public_key: str):
    account, domain = user_account.split('@')
    tx = iroha.transaction([
        iroha.command('CreateAccount', account_name=account, domain_id=domain,
                      public_key=user_public_key)
    ])
    IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)
    send_transaction_and_print_status(tx)


@trace
def create_asset(asset_id: str):
    asset, domain = asset_id.split('#')
    tx = iroha.transaction([
        iroha.command('CreateAsset', asset_name=asset, domain_id=domain, precision=2)
    ])
    IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)
    send_transaction_and_print_status(tx)


@trace
def add_coin_to_admin(asset_id: str, amount: int):
    tx = iroha.transaction([
        iroha.command('AddAssetQuantity', asset_id=asset_id, amount=str(amount))
    ])
    IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)
    send_transaction_and_print_status(tx)


@trace
def perform_few_transfer_transactions(destination_account: str, how_many: int):
    for i in range(1, how_many + 1):
        perform_transfer_transaction(destination_account, description=f'tx {i}', amount=i)


@trace
def perform_transfer_transaction(destination_account: str, description: str, amount: int):
    tx = iroha.transaction([
        iroha.command('TransferAsset', src_account_id=ADMIN_ACCOUNT_ID,
                      dest_account_id=destination_account,
                      asset_id=ASSET_ID, description=description, amount=str(amount))
    ])

    IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)
    print(f'------------> Transaction: "{description}" ------------>')
    send_transaction_and_print_status(tx)


@trace
def get_account_transactions(user_account: str, user_private_key: str,
                             asset_name: str, transactions_limit: int,
                             field=queries_pb2.kCreatedTime,
                             direction=queries_pb2.kAscending):
    ordering_sequence = [[field, direction]]

    iroha2 = Iroha(user_account)
    query = iroha2.query('GetAccountAssetTransactions', account_id=user_account,
                         asset_id=asset_name, page_size=transactions_limit,
                         ordering_sequence=ordering_sequence)

    IrohaCrypto.sign_query(query, user_private_key)
    response = net.send_query(query)

    transactions = response.transactions_page_response.transactions
    for tx in transactions:
        transfer_tx = tx.payload.reduced_payload.commands[0].transfer_asset
        created_time = tx.payload.reduced_payload.created_time
        created_time_hr = iroha_timestamp_to_human_readable(created_time)
        print(f'Transaction: {transfer_tx.src_account_id} -> {transfer_tx.dest_account_id},'
              f'{transfer_tx.asset_id}*{transfer_tx.amount}: "{transfer_tx.description}". '
              f'Created: {created_time_hr} ({created_time})')


def get_iroha_version():
    try:
        from importlib.metadata import version
        return version('iroha')
    except ModuleNotFoundError:
        return 'unknown'


def iroha_timestamp_to_human_readable(timestamp_to_convert):
    milliseconds_per_second = 10.**3
    dt = datetime.datetime.fromtimestamp(timestamp_to_convert / milliseconds_per_second)
    return dt.isoformat()


def print_paragraph(text: str):
    print(10 * '-', f'{text}:', 10 * '-')


if __name__ == '__main__':
    try:
        print('Your current iroha version:', get_iroha_version())
        print_paragraph('Preparing')
        create_account(user_account, user_public_key)
        create_asset(ASSET_ID)
        add_coin_to_admin(ASSET_ID, 10000)

        print_paragraph('Creating transactions')
        perform_few_transfer_transactions(user_account, how_many=10)
        sleep(5)

        print_paragraph('Querying as usual')
        get_account_transactions(user_account, user_private_key, ASSET_ID, transactions_limit=3,
                                 direction=queries_pb2.kAscending)

        print_paragraph('Quering as with reversed order')
        get_account_transactions(user_account, user_private_key, ASSET_ID, transactions_limit=3,
                                 direction=queries_pb2.kDescending)
    except RpcError as rpc_error:
        if rpc_error.code() == StatusCode.UNAVAILABLE:
            print(f'[E] Iroha is not running in address:'
                  f'{IROHA_HOST_ADDR}:{IROHA_PORT}!')
        else:
            print(e)
    except RuntimeError as e:
        print(e)
