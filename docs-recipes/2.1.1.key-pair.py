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

key_pair2 = iroha.KeyPair.generate()

print("kp1 =", key_pair1)
print("kp2 =", key_pair2)

key_pair3 = iroha.KeyGenConfiguration.default().use_seed_hex("001122").generate()

key_pair4 = iroha.KeyGenConfiguration.default().use_private_key(key_pair2.private_key).generate()

# kp4 and kp4 should have the same value

print("kp3 =", key_pair3)
print("kp4 =", key_pair4)