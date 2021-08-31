from ...rust import Enum, Struct, Tuple, Dict

Asset = Struct[("id", "iroha_data_model.asset.Id"),
               ("value", "iroha_data_model.asset.AssetValue")]

AssetDefinition = Struct[("value_type",
                          "iroha_data_model.asset.AssetValueType"),
                         ("id", "iroha_data_model.asset.DefinitionId")]

AssetDefinitionEntry = Struct[("definition",
                               "iroha_data_model.asset.AssetDefinition"),
                              ("registered_by", "iroha_data_model.account.Id")]

AssetValue = Enum[("Quantity", int), ("BigQuantity", int),
                  ("Store", "iroha_data_model.metadata.Metadata")]
AssetValueType = Enum[("Quantity", type(None)), ("BigQuantity", type(None)),
                      ("Store", type(None))]
DefinitionId = Struct[("name", str), ("domain_name", str)]

Id = Struct[("definition_id", "iroha_data_model.asset.DefinitionId"),
            ("account_id", "iroha_data_model.account.Id")]
