from ...rust import Enum, Struct, Tuple, Dict
Asset = Struct[("id", "iroha_data_model.asset.Id"), ("value", "iroha_data_model.asset.AssetValue")]

AssetDefinition = Struct[("id", "iroha_data_model.asset.DefinitionId"), ("value_type", "iroha_data_model.asset.AssetValueType"), ("mintable", "iroha_data_model.asset.Mintable"), ("metadata", "iroha_data_model.metadata.Metadata")]

AssetDefinitionEntry = Struct[("definition", "iroha_data_model.asset.AssetDefinition"), ("registered_by", "iroha_data_model.account.Id")]

AssetValue = Enum[("Quantity", int), ("BigQuantity", int), ("Fixed", "iroha_data_primitives.fixed.Fixed"), ("Store", "iroha_data_model.metadata.Metadata")] 
AssetValueType = Enum[("Quantity", type(None)), ("BigQuantity", type(None)), ("Fixed", type(None)), ("Store", type(None))] 
DefinitionId = Struct[("name", "iroha_data_model.Name"), ("domain_id", "iroha_data_model.domain.Id")]

Id = Struct[("definition_id", "iroha_data_model.asset.DefinitionId"), ("account_id", "iroha_data_model.account.Id")]

Mintable = Enum[("Infinitely", type(None)), ("Once", type(None)), ("Not", type(None))] 
