
from ...rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
Asset = make_struct("Asset", [("id", "iroha_data_model.asset.Id"), ("value", "iroha_data_model.asset.AssetValue")])

AssetDefinition = make_struct("AssetDefinition", [("id", "iroha_data_model.asset.DefinitionId"), ("value_type", "iroha_data_model.asset.AssetValueType"), ("mintable", "iroha_data_model.asset.Mintable"), ("metadata", "iroha_data_model.metadata.Metadata")])

AssetDefinitionEntry = make_struct("AssetDefinitionEntry", [("definition", "iroha_data_model.asset.AssetDefinition"), ("registered_by", "iroha_data_model.account.Id")])

AssetValue = make_enum("AssetValue", [("Quantity", get_class(int)), ("BigQuantity", get_class(int)), ("Fixed", get_class("iroha_primitives.fixed.Fixed")), ("Store", get_class("iroha_data_model.metadata.Metadata"))], typing.Union[get_class(int), get_class(int), get_class("iroha_primitives.fixed.Fixed"), get_class("iroha_data_model.metadata.Metadata")])

AssetValueType = make_enum("AssetValueType", [("Quantity", get_class(type(None))), ("BigQuantity", get_class(type(None))), ("Fixed", get_class(type(None))), ("Store", get_class(type(None)))], typing.Union[get_class(type(None)), get_class(type(None)), get_class(type(None)), get_class(type(None))])

DefinitionId = make_struct("DefinitionId", [("name", "iroha_data_model.name.Name"), ("domain_id", "iroha_data_model.domain.Id")])

Id = make_struct("Id", [("definition_id", "iroha_data_model.asset.DefinitionId"), ("account_id", "iroha_data_model.account.Id")])

Mintable = make_enum("Mintable", [("Infinitely", get_class(type(None))), ("Once", get_class(type(None))), ("Not", get_class(type(None)))], typing.Union[get_class(type(None)), get_class(type(None)), get_class(type(None))])

NewAssetDefinition = make_struct("NewAssetDefinition", [("id", "iroha_data_model.asset.DefinitionId"), ("value_type", "iroha_data_model.asset.AssetValueType"), ("mintable", "iroha_data_model.asset.Mintable"), ("metadata", "iroha_data_model.metadata.Metadata")])

SelfResolvingTypeVar.resolve_all()
