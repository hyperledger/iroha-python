#!/usr/bin/env python3
#
# Copyright Soramitsu Co., Ltd. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
#

# Here are Iroha dependencies.
# Python library generally consists of 3 parts:
# Iroha, IrohaCrypto and IrohaGrpc which we need to import:
"""
This example is similar to tx-example.py but it consist transaction queries
with optional params to return transactions in specific time range.
"""

import os
import sys
import binascii
from iroha import Iroha, IrohaGrpc, IrohaCrypto
from google.protobuf.timestamp_pb2 import Timestamp
from iroha.primitive_pb2 import can_set_my_account_detail
from functools import wraps
from grpc import RpcError, StatusCode
import inspect  # inspect.stack(0)

from utilities.errorCodes2Hr import get_proper_functions_for_commands


if sys.version_info[0] < 3:
    raise Exception('Python 3 or a more recent version is required.')


# Here is the information about the environment and admin account information:
IROHA_HOST_ADDR = os.getenv('IROHA_HOST_ADDR', '127.0.0.1')
IROHA_PORT = os.getenv('IROHA_PORT', '50051')
ADMIN_ACCOUNT_ID = os.getenv('ADMIN_ACCOUNT_ID', 'admin@test')
ADMIN_PRIVATE_KEY = os.getenv(
    'ADMIN_PRIVATE_KEY', 'f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70')

# Here we will create user keys
user_private_key = IrohaCrypto.private_key()
user_public_key = IrohaCrypto.derive_public_key(user_private_key)
iroha = Iroha(ADMIN_ACCOUNT_ID)
net = IrohaGrpc(f'{IROHA_HOST_ADDR}:{IROHA_PORT}')


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


# For example, below we define a transaction made of 2 commands:
# CreateDomain and CreateAsset.
# Each of Iroha commands has its own set of parameters and there are many commands.
# You can check out all of them here:
# https://iroha.readthedocs.io/en/main/develop/api/commands.html
@trace
def create_domain_and_asset(domain: str, asset_short_id: str, precision=2, default_role='user'):
    """
    Creates domain and asset with specific precision provided by arguments
    """
    commands = [
        iroha.command('CreateDomain', domain_id=domain, default_role=default_role),
        iroha.command('CreateAsset', asset_name=asset_short_id,
                      domain_id=domain, precision=precision)
    ]
# And sign the transaction using the keys from earlier:
    tx = IrohaCrypto.sign_transaction(
        iroha.transaction(commands), ADMIN_PRIVATE_KEY)
    send_transaction_and_print_status(tx)
# You can define queries 
# (https://iroha.readthedocs.io/en/main/develop/api/queries.html) 
# the same way.


@trace
def add_coin_to_admin(asset: str, amount='1000.00'):
    """
    Add provided amount of specific units to admin account
    """
    tx = iroha.transaction([
        iroha.command('AddAssetQuantity',
                      asset_id=asset, amount=amount)
    ])
    IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)
    send_transaction_and_print_status(tx)
    tx_tms = tx.payload.reduced_payload.created_time
    print(tx_tms)
    first_time, last_time = tx_tms - 1, tx_tms + 1
    return first_time, last_time


@trace
def create_account(account_id: str, domain: str):
    """
    Create account
    """
    tx = iroha.transaction([
        iroha.command('CreateAccount', account_name=account_id, domain_id=domain,
                      public_key=user_public_key)
    ])
    IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)
    send_transaction_and_print_status(tx)


@trace
def transfer_coin(source_account, destination_account, asset_id, amount='2.00'):
    """
    Transfer assets between accounts
    """
    tx = iroha.transaction([
        iroha.command('TransferAsset', src_account_id=source_account,
                      dest_account_id=destination_account, asset_id=asset_id,
                      description='init top up', amount=amount)
    ])
    IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)
    send_transaction_and_print_status(tx)


@trace
def user_grants_to_admin_set_account_detail_permission(account_id: str):
    """
    Make admin account able to set detail of account
    """
    tx = iroha.transaction([
        iroha.command('GrantPermission', account_id=ADMIN_ACCOUNT_ID,
                      permission=can_set_my_account_detail)
    ], creator_account=account_id)
    IrohaCrypto.sign_transaction(tx, user_private_key)
    send_transaction_and_print_status(tx)


@trace
def set_age_to_user(account_id: str):
    """
    Set age to user by admin account
    """
    tx = iroha.transaction([
        iroha.command('SetAccountDetail',
                      account_id=account_id, key='age', value='18')
    ])
    IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)
    send_transaction_and_print_status(tx)


@trace
def get_coin_info(asset: str):
    """
    Get asset info for provided asset
    """
    query = iroha.query('GetAssetInfo', asset_id=asset)
    IrohaCrypto.sign_query(query, ADMIN_PRIVATE_KEY)

    response = net.send_query(query)
    data = response.asset_response.asset
    print(f'Asset id = {data.asset_id}, precision = {data.precision}')


@trace
def get_account_assets(account_id: str):
    """
    List all the assets of provided user account
    """
    query = iroha.query('GetAccountAssets', account_id=account_id)
    IrohaCrypto.sign_query(query, ADMIN_PRIVATE_KEY)

    response = net.send_query(query)
    data = response.account_assets_response.account_assets
    for asset in data:
        print(f'Asset id = {asset.asset_id}, balance = {asset.balance}')


@trace
def query_transactions_simple():
    query = iroha.query('GetAccountTransactions', account_id=ADMIN_ACCOUNT_ID, page_size=3)
    IrohaCrypto.sign_query(query, ADMIN_PRIVATE_KEY)
    response = net.send_query(query)
    data = response
    print(data)


@trace 
def query_transactions(first_time=None, last_time=None,
                       first_height=None, last_height=None):
    query = iroha.query('GetAccountTransactions', account_id=ADMIN_ACCOUNT_ID,
                        first_tx_time=first_time,
                        last_tx_time=last_time,
                        first_tx_height=first_height,
                        last_tx_height=last_height,
                        page_size=3)
    IrohaCrypto.sign_query(query, ADMIN_PRIVATE_KEY)
    response = net.send_query(query)
    data = response
    print(data)


@trace
def get_user_details(account_id: str):
    """
    Get all the kv-storage entries for userone@domain
    """
    query = iroha.query('GetAccountDetail', account_id=account_id)
    IrohaCrypto.sign_query(query, ADMIN_PRIVATE_KEY)

    response = net.send_query(query)
    data = response.account_detail_response
    print(f'Account id = {account_id}, details = {data.detail}')


def iroha_timestamp_to_protobuf_timestamp(timestamp_to_convert):
    # set timestamp to correct value
    # for more protobuf timestamp api info see:
    # https://googleapis.dev/python/protobuf/latest/google/protobuf/timestamp_pb2.html
    tx_time = Timestamp()
    tx_time.FromMilliseconds(timestamp_to_convert)
    return tx_time


if __name__ == '__main__':
    try:
        # Let's run the commands defined previously:
        create_domain_and_asset(domain='domain', asset_short_id='coin')
        first_time, last_time = add_coin_to_admin(asset='coin#domain')
        create_account(account_id='userone', domain='domain')
        transfer_coin('admin@test', 'userone@domain', 'coin#domain')
        user_grants_to_admin_set_account_detail_permission(account_id='userone@domain')
        set_age_to_user(account_id='userone@domain')
        get_coin_info(asset='coin#domain')
        get_account_assets(account_id='userone@domain')
        get_user_details(account_id='userone@domain')
        query_transactions_simple()

        # query for txs in measured time
        print('transactions from time interval query: ')
        query_transactions(iroha_timestamp_to_protobuf_timestamp(first_time),
                           iroha_timestamp_to_protobuf_timestamp(last_time))
        # query for txs in given height range
        print('transactions from height range query: ')
        query_transactions(first_height=2, last_height=3)
        print('done')
    except RpcError as rpc_error:
        if rpc_error.code() == StatusCode.UNAVAILABLE:
            print(f'[E] Iroha is not running in address:'
                  f'{IROHA_HOST_ADDR}:{IROHA_PORT}!')
        else:
            print(e)
    except RuntimeError as e:
        print(e)
