from binascii import hexlify

import multihash
from iroha import ed25519_sha2
from iroha import IrohaCrypto
import binascii
import pytest

VALID_TABLE = (
    {
        'encoding': {
            'use_multihash': False
        },
        'hex': '7bab70e95cb585ea052c3aeb27de0afa9897ba5746276aa1c25310383216ceb860eb82baacbc940e710a40f21f962a3651013b90c23ece31606752f298c38d90'
    },
    {
        'encoding': {
            'use_multihash': True,
            'code': 0x12,
            'name': 'sha2-256'
        },
        'hex': '41dd7b6443542e75701aa98a0c235951a28a0d851b11564d20022ab11d2589a8'
    },
    {
        'encoding': {
            'use_multihash': True,
            'code': 0x13,
            'name': 'sha2-512'
        },
        'hex': ''
    }
)

sha2_code = 0x13
priv = ''

# unhex1 = binascii.unhexlify(priv)
# buffer = ed25519_sha2.publickey(unhex1)
# print(binascii.hexlify(buffer))

# print(IrohaCrypto.derive_public_key(priv, use_multihash=True))
# print(IrohaCrypto.hash('sdfsfsf'))


class MultihashUseageTestCase(object):
    @pytest.mark.parametrize('value', VALID_TABLE)
    def test_valid_cases(self, value):
        """ derive_public_key: test if it passes for all valid cases """
        use_multihash = value['encoding']['use_multihash']
        if use_multihash:
            pass
        else:
            pass
