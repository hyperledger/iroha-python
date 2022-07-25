from ..rust import Enum, make_struct, make_tuple, Dict
IdBox = Enum[("DomainId", "iroha_data_model.domain.Id"), ("AccountId", "iroha_data_model.account.Id"), ("AssetDefinitionId", "iroha_data_model.asset.DefinitionId"), ("AssetId", "iroha_data_model.asset.Id"), ("PeerId", "iroha_data_model.peer.Id"), ("TriggerId", "iroha_data_model.trigger.Id"), ("RoleId", "iroha_data_model.role.Id")] 
IdentifiableBox = Enum[("NewDomain", "iroha_data_model.domain.NewDomain"), ("NewAccount", "iroha_data_model.account.NewAccount"), ("NewAssetDefinition", "iroha_data_model.asset.NewAssetDefinition"), ("NewRole", "iroha_data_model.role.NewRole"), ("Peer", "iroha_data_model.peer.Peer"), ("Domain", "iroha_data_model.domain.Domain"), ("Account", "iroha_data_model.account.Account"), ("AssetDefinition", "iroha_data_model.asset.AssetDefinition"), ("Asset", "iroha_data_model.asset.Asset"), ("Trigger", "iroha_data_model.trigger.Trigger"), ("Role", "iroha_data_model.role.Role")] 
Parameter = Enum[("MaximumFaultyPeersAmount", int), ("BlockTime", int), ("CommitTime", int), ("TransactionReceiptTime", int)] 
RegistrableBox = Enum[("Peer", "iroha_data_model.peer.Peer"), ("Domain", "iroha_data_model.domain.NewDomain"), ("Account", "iroha_data_model.account.NewAccount"), ("AssetDefinition", "iroha_data_model.asset.NewAssetDefinition"), ("Asset", "iroha_data_model.asset.Asset"), ("Trigger", "iroha_data_model.trigger.Trigger"), ("Role", "iroha_data_model.role.NewRole")] 
Value = Enum[("U32", int), ("U128", int), ("Bool", bool), ("String", str), ("Name", "iroha_data_model.name.Name"), ("Fixed", "iroha_primitives.fixed.Fixed"), ("Vec", list), ("LimitedMetadata", "iroha_data_model.metadata.Metadata"), ("Id", "iroha_data_model.IdBox"), ("Identifiable", "iroha_data_model.IdentifiableBox"), ("PublicKey", "iroha_crypto.PublicKey"), ("Parameter", "iroha_data_model.Parameter"), ("SignatureCheckCondition", "iroha_data_model.account.SignatureCheckCondition"), ("TransactionValue", "iroha_data_model.transaction.TransactionValue"), ("TransactionQueryResult", "iroha_data_model.transaction.TransactionQueryResult"), ("PermissionToken", "iroha_data_model.permissions.PermissionToken"), ("Hash", "iroha_crypto.hash.Hash"), ("Block", "iroha_data_model.block_value.BlockValue"), ("BlockHeader", "iroha_data_model.block_value.BlockHeaderValue")] 
