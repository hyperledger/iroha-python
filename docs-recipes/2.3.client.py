import iroha

key_pair = iroha.KeyPair.from_json("""
{
  "public_key": "ed01207233BFC89DCBD68C19FDE6CE6158225298EC1131B6A130D1AEB454C1AB5183C0",
  "private_key": {
    "algorithm": "ed25519",
    "payload": "9ac47abf59b356e0bd7dcbbbb4dec080e302156a48ca907e47cb6aea1d32719e7233bfc89dcbd68c19fde6ce6158225298ec1131b6a130d1aeb454c1ab5183c0"
  }
}
""")

account_id = "alice@wonderland"
web_login = "mad_hatter"
password = "ilovetea"
api_url = "http://127.0.0.1:8080/"
telemetry_url = "http://127.0.0.1:8180/"
chain_id = "00000000-0000-0000-0000-000000000000"

client = iroha.Client.create(
            key_pair,
            account_id,
            web_login,
            password,
            api_url,
            chain_id)

domains = client.query_all_domains()

print("Listing all domains...")
for d in domains:
    print(" - ", d,)

