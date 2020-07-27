from collections import namedtuple

import pytest

from iroha import Iroha

iroha = Iroha('ADMIN_ACCOUNT_ID')
command = [Iroha.command('CreateDomain', domain_id='domain', default_role='user')]
transaction = Iroha.transaction(iroha, command)
Test_data = namedtuple('Test_data', ['message', 'private_key', 'public_key', 'seed'])
Test_data.__new__.__defaults__ = (transaction, None, None, None)

data_scope = ([Test_data(private_key="f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70",
                         public_key=b'313a07e6384776ed95447710d15e59148473ccfc052a681317a72a69f2a49910'),
               Test_data(private_key=b'f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70',
                         public_key=b'313a07e6384776ed95447710d15e59148473ccfc052a681317a72a69f2a49910'),
               Test_data(public_key='ed0120ca0d372c15b712b46fa1c6e4afc4fd7e23e91dbf869da497db898d884f45ac40',
                         seed=b'\x99\xfe\x89i\xac\xda\xfb\t\xbf\xdd\x00F7\x0e/\xa2X\x0b\x0c%\x91\xa266%%\r\xa1Mw\x1bc')
               ])
data_ids = ['priv_key, pub_key({},{})'.format(t.private_key, t.public_key)
            for t in data_scope]


@pytest.fixture(scope='session', params=data_scope, ids=data_ids)
def data_for_crypto_test(request):
    return request.param

