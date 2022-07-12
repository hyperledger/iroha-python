from ......rust import Enum, Struct, Tuple, Dict
AccountEvent = Enum[("Asset", "iroha_data_model.events.data.events.asset.AssetEvent"), ("Created", "iroha_data_model.account.Id"), ("Deleted", "iroha_data_model.account.Id"), ("AuthenticationAdded", "iroha_data_model.account.Id"), ("AuthenticationRemoved", "iroha_data_model.account.Id"), ("PermissionAdded", "iroha_data_model.account.Id"), ("PermissionRemoved", "iroha_data_model.account.Id"), ("MetadataInserted", "iroha_data_model.account.Id"), ("MetadataRemoved", "iroha_data_model.account.Id")] 