#!/usr/bin/env python3
#
# Copyright Soramitsu Co., Ltd. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""
This example demonstrates how to use TLS connection between Iroha peer and iroha-python.
Before running the example first configure torii_tls_params according to documentation:
https://iroha.readthedocs.io/en/main/configure/torii-tls.html
Note: You need certificate for your server (sample from Iroha will not work).
"""

import os
import binascii
import sys
from grpc import RpcError, StatusCode
import inspect  # inspect.stack(0)
from iroha import Iroha, IrohaGrpc, IrohaCrypto
from functools import wraps
from utilities.errorCodes2Hr import get_proper_functions_for_commands


if sys.version_info[0] < 3:
    raise Exception('Python 3 or a more recent version is required.')


IROHA_HOST_ADDR = os.getenv('IROHA_HOST_ADDR', 'localhost')
IROHA_TLS_PORT = os.getenv('IROHA_PORT', '55552')
ADMIN_ACCOUNT_ID = os.getenv('ADMIN_ACCOUNT_ID', 'admin@test')
ADMIN_PRIVATE_KEY = os.getenv(
    'ADMIN_PRIVATE_KEY', 'f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70')
iroha = Iroha(ADMIN_ACCOUNT_ID)
# NOTE: You have to generate certificates for your machine - sample below will not work:
certificate = """-----BEGIN CERTIFICATE-----
MIIDUDCCAjgCCQCsHEs/sUtihTANBgkqhkiG9w0BAQsFADBqMQswCQYDVQQGEwJy
dTELMAkGA1UECAwCZGYxCzAJBgNVBAcMAmRmMQswCQYDVQQKDAJkZjELMAkGA1UE
CwwCZGYxEjAQBgNVBAMMCWxvY2FsaG9zdDETMBEGCSqGSIb3DQEJARYEbWFpbDAe
Fw0yMDExMTkxOTM1MzVaFw0yMDEyMTkxOTM1MzVaMGoxCzAJBgNVBAYTAnJ1MQsw
CQYDVQQIDAJkZjELMAkGA1UEBwwCZGYxCzAJBgNVBAoMAmRmMQswCQYDVQQLDAJk
ZjESMBAGA1UEAwwJbG9jYWxob3N0MRMwEQYJKoZIhvcNAQkBFgRtYWlsMIIBIjAN
BgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAu/vS/zgCIJOfpP58OFX+4EDByDnQ
42MSQtgw1+nDQjc2thasHrNI5pFrWIRtVYUIIPhhPUEJJFW034awLWiggiZHWO9a
gocO95AxjaborxRVavOLUIX17HnEiU6lb3lyfwq9t2bpluT+ooRM2ymDCl/NCsdS
nvRomFvCcfpbVu0rc0hBVsLGrg+Hr/+mS88MIL6sU95Suawj8f8A0QoMN0zxQjto
EyXVWN46vurxXMYFDbdRejwg1ba+DFajm6Dcl1nIq/u7dpG6mmDMzFVrwmYh6wYf
XpT4eW9KNe9EEIh+loF7ohg+GE2YGXW/9f8UuQfsgyTHHj+uS0jdiD3PDwIDAQAB
MA0GCSqGSIb3DQEBCwUAA4IBAQBQxyCYOA47Uzxc3qdYwnmqQ6oug73heh5qMbjC
dJ9eY+BKZgd97kI+msX1ha9PKQaITONeZxE2907m2RQckCFXYFPxumQ/O8YiN3Vb
UXy3otCPKlF+RoPEFH2UJiiIakbgE796FB/TskO1pEvdrE9i1GiCV2503VUzP9IC
QRFMvWvZ4lk5Jw7rthL3xsdz3BDESULfN4mXQthZ98H+v7z7WaARzdOauFLwJ4rV
XNlyBGw14951Xm/MoKQZdZlsG80xDucBf/VJrKLkQW60CWmXhit0GiZu79LzYMuN
QAGWtoyyaJ7TmCOUR9MpH/2bna429WOhg9/hgMDGdJ9bG1Bm
-----END CERTIFICATE-----
"""
byte_certificate = bytes(certificate, 'utf-8')
net = IrohaGrpc(f'{IROHA_HOST_ADDR}:{IROHA_TLS_PORT}', secure=True,
                root_certificates=byte_certificate)


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
def add_coin_to_admin(asset_id: str, amount_to_add='1000.00'):
    """
    Add provided amount of specific units to admin account
    """
    tx = iroha.transaction([
        iroha.command('AddAssetQuantity', asset_id=asset_id, amount=amount_to_add)
    ])
    IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)
    send_transaction_and_print_status(tx)


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
        print(f'Asset of {account_id}: {asset.asset_id}, balance = {asset.balance}')


if __name__ == '__main__':
    print("""
    This example works only through a TLS connection, you must first configure torii_tls_params
    https://iroha.readthedocs.io/en/main/configure/torii-tls.html
    """)
    try:
        add_coin_to_admin(asset_id='coin#domain', amount_to_add='1000.00')
        get_account_assets(account_id=ADMIN_ACCOUNT_ID)
    except RpcError as rpc_error:
        if rpc_error.code() == StatusCode.UNAVAILABLE:
            print(f'[E] Iroha is not running in address:'
                  f'{IROHA_HOST_ADDR}:{IROHA_TLS_PORT}, '
                  f'or invalid certificate for TLS connection')
        else:
            print(e)
    except RuntimeError as e:
        print(e)
