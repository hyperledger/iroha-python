"""Test to check cryptographic functions"""

from iroha import IrohaCrypto, ed25519_sha2


def test_derive_public_key(data_for_crypto_test):
    """Checking call with different data types"""
    if data_for_crypto_test.seed is not None:  # if seed is present in the data, then we create a key_pair out of it.
        key_pair = ed25519_sha2.SigningKey(seed=data_for_crypto_test.seed)
        public_key = IrohaCrypto.derive_public_key(key_pair)
    else:
        public_key = IrohaCrypto.derive_public_key(data_for_crypto_test.private_key)
    assert public_key == data_for_crypto_test.public_key


def test_create_signature(data_for_crypto_test):
    """Checking call with different data types"""
    if data_for_crypto_test.seed is not None:
        key_pair = ed25519_sha2.SigningKey(seed=data_for_crypto_test.seed)
        signature = IrohaCrypto._signature(data_for_crypto_test.message, key_pair)
        validate = IrohaCrypto.is_sha2_signature_valid(data_for_crypto_test.message, signature)
        assert validate
    else:
        signature = IrohaCrypto._signature(data_for_crypto_test.message, data_for_crypto_test.private_key)
        validate = IrohaCrypto.is_signature_valid(data_for_crypto_test.message, signature)
        assert validate
