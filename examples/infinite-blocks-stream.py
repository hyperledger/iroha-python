#!/usr/bin/env python3
#
# Copyright Soramitsu Co., Ltd. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""
The script will wait for new blocks.
You need to send some commands to the node to see any blocks coming
"""

import sys
import os
from grpc import RpcError, StatusCode
import inspect  # inspect.stack(0)
from iroha import Iroha, IrohaGrpc, IrohaCrypto
from functools import wraps


if sys.version_info[0] < 3:
    raise Exception('Python 3 or a more recent version is required.')

IROHA_HOST_ADDR = os.getenv('IROHA_HOST_ADDR', '127.0.0.1')
IROHA_PORT = os.getenv('IROHA_PORT', '50051')
ADMIN_ACCOUNT_ID = os.getenv('ADMIN_ACCOUNT_ID', 'admin@test')
ADMIN_PRIVATE_KEY = os.getenv(
    'ADMIN_PRIVATE_KEY', 'f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70')

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
def get_blocks():
    """
    Subscribe to blocks stream from the network
    :return:
    """
    query = iroha.blocks_query()
    IrohaCrypto.sign_query(query, ADMIN_PRIVATE_KEY)
    for block in net.send_blocks_stream_query(query):
        print('\nThe next block arrived:', block)


if __name__ == '__main__':
    try:
        print('The script will wait for new blocks. '
              'You need to send some commands to the node to see any blocks coming')
        get_blocks()
    except RpcError as rpc_error:
        if rpc_error.code() == StatusCode.UNAVAILABLE:
            print(f'[E] Iroha is not running in address:'
                  f'{IROHA_HOST_ADDR}:{IROHA_PORT}!')
        else:
            print(e)
    except RuntimeError as e:
        print(e)
