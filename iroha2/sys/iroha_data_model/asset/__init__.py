from ...rust import Enum, make_struct, make_tuple, Dict
Asset = make_struct("Asset", [("id", "iroha_data_model.asset.Id"), ("value", "iroha_data_model.asset.AssetValue")])

AssetDefinition = make_struct("AssetDefinition", [("id", "iroha_data_model.asset.DefinitionId"), ("value_type", "iroha_data_model.asset.AssetValueType"), ("mintable", "iroha_data_model.asset.Mintable"), ("metadata", "iroha_data_model.metadata.Metadata")])

AssetDefinitionEntry = make_struct("AssetDefinitionEntry", [("definition", "iroha_data_model.asset.AssetDefinition"), ("registered_by", "iroha_data_model.account.Id")])

AssetValue = Enum[("Quantity", int), ("BigQuantity", int), ("Fixed", "iroha_primitives.fixed.Fixed"), ("Store", "iroha_data_model.metadata.Metadata")] 
AssetValueType = Enum[("Quantity", type(None)), ("BigQuantity", type(None)), ("Fixed", type(None)), ("Store", type(None))] 
DefinitionId = make_struct("DefinitionId", [("name", "iroha_data_model.name.Name"), ("domain_id", "iroha_data_model.domain.Id")])

Id = make_struct("Id", [("definition_id", "iroha_data_model.asset.DefinitionId"), ("account_id", "iroha_data_model.account.Id")])

Mintable = Enum[("Infinitely", type(None)), ("Once", type(None)), ("Not", type(None))] 
NewAssetDefinition = make_struct("NewAssetDefinition", [("id", "iroha_data_model.asset.DefinitionId"), ("value_type", "iroha_data_model.asset.AssetValueType"), ("mintable", "iroha_data_model.asset.Mintable"), ("metadata", "iroha_data_model.metadata.Metadata")])

