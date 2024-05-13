import iroha

def generate_public_key(seed="abcd1122"):

    """
    Generate a public key using Ed25519PrivateKey.
    """
    return iroha.KeyPair.from_hex_seed(seed).public_key