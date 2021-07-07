#!/usr/bin/env python3
#
# Copyright Soramitsu Co., Ltd. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
#

import os
import binascii
from iroha import IrohaCrypto
from iroha import Iroha, IrohaGrpc
import sys

if sys.version_info[0] < 3:
    raise Exception('Python 3 or a more recent version is required.')

print("""
This example works only through a TLS connection, you must first configure torii_tls_params
https://iroha.readthedocs.io/en/main/configure/torii-tls.html
""")

IROHA_HOST_ADDR = os.getenv('IROHA_HOST_ADDR', 'localhost')
IROHA_TLS_PORT = os.getenv('IROHA_PORT', '55552')
ADMIN_ACCOUNT_ID = os.getenv('ADMIN_ACCOUNT_ID', 'admin@test')
ADMIN_PRIVATE_KEY = os.getenv(
    'ADMIN_PRIVATE_KEY', 'f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70')
iroha = Iroha(ADMIN_ACCOUNT_ID)
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
net = IrohaGrpc('{}:{}'.format(IROHA_HOST_ADDR, IROHA_TLS_PORT), secure=True, root_certificates=byte_certificate)


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
def add_coin_to_admin():
    """
    Add 1000.00 units of 'coin#domain' to 'admin@test'
    """
    tx = iroha.transaction([
        iroha.command('AddAssetQuantity',
                      asset_id='coin#domain', amount='1000.00')
    ])
    IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)
    send_transaction_and_print_status(tx)


add_coin_to_admin()