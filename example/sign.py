from iroha2.data_model.transaction import SignedTransaction
from iroha2.crypto import KeyPair

# Example signed transaction, encoded with SCALE codec and represented as hex string
encoded_transaction = "0114616c69636528776f6e6465726c616e640004000d09001468656c6c6f00002cde318c87010000a0860100000000000000041c65643235353139807233bfc89dcbd68c19fde6ce6158225298ec1131b6a130d1aeb454c1ab5183c00101bef276fc36ba638abd422e76fd0e6df319df1c3d336ab60d7276333b4010bb7d962d04b273d9caf91cb8509581c0b55e1cdee371c52863a8b4b62c67fbfc870f"

# Example ed25519 private key
private_key = "413b285d1819a6166b0daa762bb6bef2d082cffb9a13ce041cb0fda5e2f06dc37fbedb314a9b0c00caef967ac5cabb982ec45da828a0c58a9aafc854f32422ac"

# Recover keypair from private key
key_pair = KeyPair.from_private(private_key)
# ed25519 is the default, for e.g. secp256k1 key you would
# need to explicitly specify the algorithm:
#key_pair = KeyPair.from_private(private_key, "secp256k1")

# Decode transaction
transaction = SignedTransaction.decode(encoded_transaction)

# Sign transaction with provided private key
transaction.append_signature(key_pair)

# Re-encode the transaction
re_encoded_transaction = transaction.encode()

print(f"Signed and encoded transaction:\n{re_encoded_transaction}")