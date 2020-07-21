"""Test to check cryptographic functions"""

import pytest
import binascii
from collections import namedtuple
from iroha import Iroha, IrohaCrypto, ed25519_sha2

user_private_key = IrohaCrypto.private_key()
iroha = Iroha('ADMIN_ACCOUNT_ID')
Test_data = namedtuple('Test_data', ['message', 'private_key', 'public_key', 'seed'])
command = [Iroha.command('CreateDomain', domain_id='domain', default_role='user')]
transaction = Iroha.transaction(iroha, command)
Test_data.__new__.__defaults__ = (transaction, None, None, None)

data_scope = ([Test_data(private_key="f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70",
                         public_key=b'313a07e6384776ed95447710d15e59148473ccfc052a681317a72a69f2a49910'),
               Test_data(private_key=b'f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70',
                         public_key=b'313a07e6384776ed95447710d15e59148473ccfc052a681317a72a69f2a49910'),
               Test_data(
                   private_key=b'\x99\xfe\x89i\xac\xda\xfb\t\xbf\xdd\x00F7\x0e/\xa2X\x0b\x0c%\x91\xa266%%\r\xa1Mw\x1bc'
                               b'\xca\r7,\x15\xb7\x12\xb4o\xa1\xc6\xe4\xaf\xc4\xfd~#\xe9\x1d\xbf\x86\x9d\xa4\x97\xdb'
                               b'\x89\x8d\x88OE\xac@',
                   public_key='ed0120ca0d372c15b712b46fa1c6e4afc4fd7e23e91dbf869da497db898d884f45ac40',
                   seed=b'\x99\xfe\x89i\xac\xda\xfb\t\xbf\xdd\x00F7\x0e/\xa2X\x0b\x0c%\x91\xa266%%\r\xa1Mw\x1bc')
               ])
data_ids = ['priv_key, pub_key({},{})'.format(t.private_key, t.public_key)
            for t in data_scope]


@pytest.mark.parametrize('test_data', data_scope, ids=data_ids)
def test_derive_public_key(test_data):
    """Checking call with different data types of the derive_public_key method"""
    if test_data.seed is not None:  # if seed is present in the data, then we create a key_pair out of it.
        key_pair = ed25519_sha2.SigningKey(seed=test_data.seed)
        public_key = IrohaCrypto.derive_public_key(key_pair)
    else:
        public_key = IrohaCrypto.derive_public_key(test_data.private_key)
    print(public_key)
    assert public_key == test_data.public_key


@pytest.mark.parametrize('test_data', data_scope, ids=data_ids)
def test_create_signature(test_data):
    if test_data.seed is not None:
        key_pair = ed25519_sha2.SigningKey(seed=test_data.seed)
        signature = IrohaCrypto._signature(test_data.message, key_pair)
        vk = getattr(key_pair, "verify_key")
        print(binascii.unhexlify(vk))
        message_hash = IrohaCrypto.hash(test_data.message, sha2=True)
        sign_byte = binascii.unhexlify(signature.signature)
        validate = ed25519_sha2.VerifyKey.verify(key_pair.verify_key, message_hash, sign_byte)
        assert validate == message_hash
    else:
        signature = IrohaCrypto._signature(test_data.message, test_data.private_key)
        validate = IrohaCrypto.is_signature_valid(test_data.message, signature)
        assert validate
