from ....rust import Enum, Struct, Tuple, Dict
FindAllAssets = Tuple[()]
FindAllAssetsDefinitions = Tuple[()]
FindAssetById = Struct[("id", "iroha_data_model.expression.EvaluatesTo")]

FindAssetDefinitionById = Struct[("id", "iroha_data_model.expression.EvaluatesTo")]

FindAssetDefinitionKeyValueByIdAndKey = Struct[("id", "iroha_data_model.expression.EvaluatesTo"), ("key", "iroha_data_model.expression.EvaluatesTo")]

FindAssetKeyValueByIdAndKey = Struct[("id", "iroha_data_model.expression.EvaluatesTo"), ("key", "iroha_data_model.expression.EvaluatesTo")]

FindAssetQuantityById = Struct[("id", "iroha_data_model.expression.EvaluatesTo")]

FindAssetsByAccountId = Struct[("account_id", "iroha_data_model.expression.EvaluatesTo")]

FindAssetsByAssetDefinitionId = Struct[("asset_definition_id", "iroha_data_model.expression.EvaluatesTo")]

FindAssetsByDomainId = Struct[("domain_id", "iroha_data_model.expression.EvaluatesTo")]

FindAssetsByDomainIdAndAssetDefinitionId = Struct[("domain_id", "iroha_data_model.expression.EvaluatesTo"), ("asset_definition_id", "iroha_data_model.expression.EvaluatesTo")]

FindAssetsByName = Struct[("name", "iroha_data_model.expression.EvaluatesTo")]

