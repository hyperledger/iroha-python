#!/usr/bin/env python
# -*- coding: utf-8 -*-

from iroha import IrohaCrypto
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
            'code': 0x13,
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
        'hex': '7865fc8f9d4bbc1fdbfa891e67d8102bde30a7382587cd02a0756adfb1e26ad38a98ea710bc30ef47d1d32b5f05640781455ebd5ae6d7612c88c7b985f82dd08'
    }
)

INVALID_TABLE = (
    {
        'encoding': {
            'use_multihash': True,
            'code': 'unknown'
        },
        'hex': '7bab70e95cb585ea052c3aeb27de0afa9897ba5746276aa1c25310383216ceb860eb82baacbc940e710a40f21f962a3651013b90c23ece31606752f298c38d90'
    },
{
        'encoding': {
            'use_multihash': True,
            'code': ''
        },
        'hex': '7bab70e95cb585ea052c3aeb27de0afa9897ba5746276aa1c25310383216ceb860eb82baacbc940e710a40f21f962a3651013b90c23ece31606752f298c38d90'
    }
)


@pytest.mark.parametrize('value', VALID_TABLE)
def test_valid_cases_multihash(value):
    """ derive_public_key: test if it passes for all valid cases """
    use_multihash = value['encoding']['use_multihash']
    if use_multihash:
        hex = value['hex']
        private_key = IrohaCrypto.derive_public_key(hex,
                                                    use_multihash=use_multihash,
                                                    multihash_code=value['encoding']['code'])
        assert private_key.decode("utf-8").startswith('13')
    else:
        private_key = IrohaCrypto.derive_public_key(value['hex'])
        assert not private_key.decode("utf-8").startswith('13')


@pytest.mark.parametrize('value', INVALID_TABLE)
def test_invalid_cases_multihash(value):
    use_multihash = value['encoding']['use_multihash']
    if use_multihash:
        with pytest.raises(ValueError) as excinfo:
            IrohaCrypto.derive_public_key(value['hex'], use_multihash=use_multihash,
                                          multihash_code=value['encoding']['code'])
        assert 'Unsupported hash function' in str(excinfo.value)
