
from .....rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
EntityFilter = make_enum("EntityFilter", [("ByPeer", get_class("iroha_data_model.events.data.filters.FilterOpt")), ("ByDomain", get_class("iroha_data_model.events.data.filters.FilterOpt")), ("ByAccount", get_class("iroha_data_model.events.data.filters.FilterOpt")), ("ByAssetDefinition", get_class("iroha_data_model.events.data.filters.FilterOpt")), ("ByAsset", get_class("iroha_data_model.events.data.filters.FilterOpt")), ("ByTrigger", get_class("iroha_data_model.events.data.filters.FilterOpt")), ("ByRole", get_class("iroha_data_model.events.data.filters.FilterOpt"))], typing.Union[get_class("iroha_data_model.events.data.filters.FilterOpt"), get_class("iroha_data_model.events.data.filters.FilterOpt"), get_class("iroha_data_model.events.data.filters.FilterOpt"), get_class("iroha_data_model.events.data.filters.FilterOpt"), get_class("iroha_data_model.events.data.filters.FilterOpt"), get_class("iroha_data_model.events.data.filters.FilterOpt"), get_class("iroha_data_model.events.data.filters.FilterOpt")])

FilterOpt = make_enum("FilterOpt", [("AcceptAll", get_class(type(None))), ("BySome", get_class("iroha_data_model.events.data.events.account.AccountEventFilter"))], typing.Union[get_class(type(None)), get_class("iroha_data_model.events.data.events.account.AccountEventFilter")])

OriginFilter = make_tuple("OriginFilter", ["iroha_data_model.account.Id"])
SelfResolvingTypeVar.resolve_all()
