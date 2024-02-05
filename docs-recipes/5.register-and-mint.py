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

assets = client.query_all_assets_owned_by_account("alice@wonderland")

print("Listing all assets owned by alice@wonderland...")
for a in assets:
    print(" - ", a,)


asset_definition_id = "time#wonderland"
asset_id = "time##alice@wonderland"

if "time##alice@wonderland" in assets:
    print("'alice@wonderland' already has asset 'time'.")

register_definition = iroha.Instruction.register_asset_definition(asset_definition_id, "Quantity")

mint = iroha.Instruction.mint_asset(5, asset_id, "Quantity")

client.submit_executable([register_definition, mint])

while True:
    assets = client.query_all_assets_owned_by_account("alice@wonderland")
    
    if asset_id in assets:
        break

print("Listing all assets owned by alice@wonderland...")
for a in assets:
    print(" - ", a,)