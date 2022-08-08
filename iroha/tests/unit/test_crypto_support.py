"""Test to check cryptographic functions"""

from iroha import IrohaCrypto, ed25519_sha2


def test_derive_public_key(crypto_data):
    """Checking call with different data types"""
    public_key = IrohaCrypto.derive_public_key(crypto_data.private_key)
    assert public_key == crypto_data.public_key


def test_create_signature(crypto_data):
    """Checking call with different data types"""
    signature = IrohaCrypto._signature(crypto_data.message, crypto_data.private_key)
    if isinstance(crypto_data.private_key, ed25519_sha2.SigningKey):  # Use different validation method
        validate = IrohaCrypto.is_sha2_signature_valid(crypto_data.message, signature)
        assert validate
    else:
        validate = IrohaCrypto.is_signature_valid(crypto_data.message, signature)
        assert validate
