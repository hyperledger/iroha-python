from .....rust import Enum, Struct, Tuple, Dict
EntityFilter = Enum[("ByPeer", "iroha_data_model.events.data.filters.FilterOpt"), ("ByDomain", "iroha_data_model.events.data.filters.FilterOpt"), ("ByAccount", "iroha_data_model.events.data.filters.FilterOpt"), ("ByAssetDefinition", "iroha_data_model.events.data.filters.FilterOpt"), ("ByAsset", "iroha_data_model.events.data.filters.FilterOpt"), ("ByTrigger", "iroha_data_model.events.data.filters.FilterOpt"), ("ByRole", "iroha_data_model.events.data.filters.FilterOpt")] 
FilterOpt = Enum[("AcceptAll", type(None)), ("BySome", "iroha_data_model.events.data.events.account.AccountEventFilter")] 
IdFilter = Tuple["iroha_data_model.account.Id"]
