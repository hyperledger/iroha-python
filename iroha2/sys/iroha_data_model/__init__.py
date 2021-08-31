from ..rust import Enum, Struct, Tuple, Dict

IdBox = Enum[("AccountId", "iroha_data_model.account.Id"),
             ("AssetId", "iroha_data_model.asset.Id"),
             ("AssetDefinitionId", "iroha_data_model.asset.DefinitionId"),
             ("DomainName", str), ("PeerId", "iroha_data_model.peer.Id"),
             ("WorldId", type(None))]
IdentifiableBox = Enum[("Account", "iroha_data_model.account.Account"),
                       ("NewAccount", "iroha_data_model.account.NewAccount"),
                       ("Asset", "iroha_data_model.asset.Asset"),
                       ("AssetDefinition",
                        "iroha_data_model.asset.AssetDefinition"),
                       ("Domain", "iroha_data_model.domain.Domain"),
                       ("Peer", "iroha_data_model.peer.Peer"), ("World",
                                                                type(None))]
Parameter = Enum[("MaximumFaultyPeersAmount", int), ("BlockTime", int),
                 ("CommitTime", int), ("TransactionReceiptTime", int)]
Value = Enum[("U32", int), ("Bool", bool), ("String", str), ("Vec", list),
             ("Id", "iroha_data_model.IdBox"),
             ("Identifiable", "iroha_data_model.IdentifiableBox"),
             ("PublicKey", "iroha_crypto.PublicKey"),
             ("Parameter", "iroha_data_model.Parameter"),
             ("SignatureCheckCondition",
              "iroha_data_model.account.SignatureCheckCondition"),
             ("TransactionValue",
              "iroha_data_model.transaction.TransactionValue"),
             ("PermissionToken",
              "iroha_data_model.permissions.PermissionToken")]
