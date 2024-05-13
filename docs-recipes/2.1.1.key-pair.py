import iroha

key_pair1 = iroha.KeyPair.from_json("""
{
  "public_key": "ed01207233BFC89DCBD68C19FDE6CE6158225298EC1131B6A130D1AEB454C1AB5183C0",
  "private_key": {
    "algorithm": "ed25519",
    "payload": "9ac47abf59b356e0bd7dcbbbb4dec080e302156a48ca907e47cb6aea1d32719e7233bfc89dcbd68c19fde6ce6158225298ec1131b6a130d1aeb454c1ab5183c0"
  }
}
""")

key_pair2 = iroha.KeyPair.random()

print("kp1 =", key_pair1)
print("kp2 =", key_pair2)

key_pair3 = iroha.KeyPair.from_hex_seed("001122")

key_pair4 = iroha.KeyPair.from_private_key(key_pair2.private_key)

# kp2 and kp4 should have the same value

print("kp3 =", key_pair3)
print("kp4 =", key_pair4)


# Different algorithms are supported

print("kp using Ed25519 =", iroha.KeyPair.random_with_algorithm("Ed25519"))
print("kp using Secp256k1 =", iroha.KeyPair.random_with_algorithm("Secp256k1"))
print("kp using BlsNormal =", iroha.KeyPair.random_with_algorithm("BlsNormal"))
print("kp using BlsSmall =", iroha.KeyPair.random_with_algorithm("BlsSmall"))