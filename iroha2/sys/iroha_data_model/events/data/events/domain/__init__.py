
from ......rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
DomainEvent = make_enum("DomainEvent", [("Account", get_class("iroha_data_model.events.data.events.account.AccountEvent")), ("AssetDefinition", get_class("iroha_data_model.events.data.events.asset.AssetDefinitionEvent")), ("Created", get_class("iroha_data_model.domain.Id")), ("Deleted", get_class("iroha_data_model.domain.Id")), ("MetadataInserted", get_class("iroha_data_model.events.data.events.MetadataChanged")), ("MetadataRemoved", get_class("iroha_data_model.events.data.events.MetadataChanged"))], typing.Union[get_class("iroha_data_model.events.data.events.account.AccountEvent"), get_class("iroha_data_model.events.data.events.asset.AssetDefinitionEvent"), get_class("iroha_data_model.domain.Id"), get_class("iroha_data_model.domain.Id"), get_class("iroha_data_model.events.data.events.MetadataChanged"), get_class("iroha_data_model.events.data.events.MetadataChanged")])

DomainEventFilter = make_enum("DomainEventFilter", [("ByCreated", get_class(type(None))), ("ByDeleted", get_class(type(None))), ("ByMetadataInserted", get_class(type(None))), ("ByMetadataRemoved", get_class(type(None))), ("ByAccount", get_class("iroha_data_model.events.data.filters.FilterOpt")), ("ByAssetDefinition", get_class("iroha_data_model.events.data.filters.FilterOpt"))], typing.Union[get_class(type(None)), get_class(type(None)), get_class(type(None)), get_class(type(None)), get_class("iroha_data_model.events.data.filters.FilterOpt"), get_class("iroha_data_model.events.data.filters.FilterOpt")])

DomainFilter = make_struct("DomainFilter", [("origin_filter", "iroha_data_model.events.data.filters.FilterOpt"), ("event_filter", "iroha_data_model.events.data.filters.FilterOpt")])

SelfResolvingTypeVar.resolve_all()
