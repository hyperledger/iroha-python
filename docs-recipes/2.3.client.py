import iroha

key_pair = iroha.KeyPair.from_json("""
{
  "public_key": "ed01207233BFC89DCBD68C19FDE6CE6158225298EC1131B6A130D1AEB454C1AB5183C0",
  "private_key": {
    "digest_function": "ed25519",
    "payload": "9ac47abf59b356e0bd7dcbbbb4dec080e302156a48ca907e47cb6aea1d32719e7233bfc89dcbd68c19fde6ce6158225298ec1131b6a130d1aeb454c1ab5183c0"
  }
}
""")

account_id = "alice@wonderland"
web_login = "mad_hatter"
password = "ilovetea"
api_url = "http://127.0.0.1:8080/"
telemetry_url = "http://127.0.0.1:8180/"

client = iroha.Client.create(
            key_pair,
            account_id,
            web_login,
            password,
            api_url)

pyasset_id = iroha.AssetDefinitionId("pyasset", "wonderland")
alice = iroha.AccountId("alice", "wonderland")
bob = iroha.AccountId("bob", "wonderland")


register = iroha.Instruction.register(iroha.NewAssetDefinition(pyasset_id, iroha.AssetValueType.QUANTITY))
mint = iroha.Instruction.mint(1024, iroha.AssetId(pyasset_id, alice))
transfer = iroha.Instruction.transfer(512, iroha.AssetId(pyasset_id, alice), bob)

client.submit_executable([register, mint, transfer])
