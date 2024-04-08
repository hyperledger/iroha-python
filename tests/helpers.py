import iroha

def generate_public_key(seed="abcd1122"):

    """
    Generate a public key using Ed25519PrivateKey.
    """
    return iroha.KeyGenConfiguration.default().use_seed_hex(seed).generate().public_key