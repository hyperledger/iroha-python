from ....rust import Enum, Struct, Tuple, Dict

FindAllAssets = Struct[()]

FindAllAssetsDefinitions = Struct[()]

FindAssetById = Struct[("id", "iroha_data_model.expression.EvaluatesTo")]

FindAssetKeyValueByIdAndKey = Struct[(
    "id", "iroha_data_model.expression.EvaluatesTo"), (
        "key", "iroha_data_model.expression.EvaluatesTo")]

FindAssetQuantityById = Struct[("id",
                                "iroha_data_model.expression.EvaluatesTo")]

FindAssetsByAccountId = Struct[("account_id",
                                "iroha_data_model.expression.EvaluatesTo")]

FindAssetsByAccountIdAndAssetDefinitionId = Struct[(
    "account_id", "iroha_data_model.expression.EvaluatesTo"), (
        "asset_definition_id", "iroha_data_model.expression.EvaluatesTo")]

FindAssetsByAssetDefinitionId = Struct[(
    "asset_definition_id", "iroha_data_model.expression.EvaluatesTo")]

FindAssetsByDomainName = Struct[("domain_name",
                                 "iroha_data_model.expression.EvaluatesTo")]

FindAssetsByDomainNameAndAssetDefinitionId = Struct[(
    "domain_name", "iroha_data_model.expression.EvaluatesTo"), (
        "asset_definition_id", "iroha_data_model.expression.EvaluatesTo")]

FindAssetsByName = Struct[("name", "iroha_data_model.expression.EvaluatesTo")]
