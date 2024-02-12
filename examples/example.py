import iroha

config = open("example_config.json").read()
cl = iroha.Client(config)

for asset in cl.find_all_assets_definitions():
    print(f"Asset {asset.id}:")
    print(repr(asset))

pyasset_id = iroha.AssetDefinitionId("pyasset", "wonderland")
alice = iroha.AccountId("alice", "wonderland")
bob = iroha.AccountId("bob", "wonderland")

register = iroha.Instruction.register(iroha.NewAssetDefinition(pyasset_id, iroha.AssetValueType.QUANTITY))
mint = iroha.Instruction.mint(1024, iroha.AssetId(pyasset_id, alice))
transfer = iroha.Instruction.transfer(512, iroha.AssetId(pyasset_id, alice), bob)
cl.submit([register, mint, transfer])
