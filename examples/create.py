#!/usr/bin/env python3
#
# Copyright Soramitsu Co., Ltd. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
#

import os
import binascii
from iroha import IrohaCrypto
from iroha import Iroha, IrohaGrpc, ed25519_sha2
import sys

if sys.version_info[0] < 3:
    raise Exception('Python 3 or a more recent version is required.')


IROHA_HOST_ADDR = os.getenv('IROHA_HOST_ADDR', '127.0.0.1')
IROHA_PORT = os.getenv('IROHA_PORT', '50051')
ADMIN_ACCOUNT_ID = os.getenv('ADMIN_ACCOUNT_ID', 'ursama@test')
seed = b'\x99\xfe\x89i\xac\xda\xfb\t\xbf\xdd\x00F7\x0e/\xa2X\x0b\x0c%\x91\xa266%%\r\xa1Mw\x1bc'
ADMIN_PRIVATE_KEY = ed25519_sha2.SigningKey(seed)
iroha = Iroha(ADMIN_ACCOUNT_ID)
net = IrohaGrpc('{}:{}'.format(IROHA_HOST_ADDR, IROHA_PORT))


def trace(func):
    """
    A decorator for tracing methods' begin/end execution points
    """

    def tracer(*args, **kwargs):
        name = func.__name__
        print('\tEntering "{}"'.format(name))
        result = func(*args, **kwargs)
        print('\tLeaving "{}"'.format(name))
        return result

    return tracer


@trace
def send_transaction_and_print_status(transaction):
    hex_hash = binascii.hexlify(IrohaCrypto.hash(transaction))
    print('Transaction hash = {}, creator = {}'.format(
        hex_hash, transaction.payload.reduced_payload.creator_account_id))
    net.send_tx(transaction)
    for status in net.tx_status_stream(transaction):
        print(status)


@trace
def create_domain_and_asset():
    """
    Creates domain 'domain' and asset 'coin#domain' with precision 2
    """
    commands = [
        iroha.command('CreateAccount', account_name='ursa',
                      domain_id='test', public_key='ed0120ca0d372c15b712b46fa1c6e4afc4fd7e23e91dbf869da497db898d884f45ac40')
    ]
    tx = IrohaCrypto.sign_transaction(
        iroha.transaction(commands), ADMIN_PRIVATE_KEY)
    send_transaction_and_print_status(tx)


create_domain_and_asset()

print('done')
