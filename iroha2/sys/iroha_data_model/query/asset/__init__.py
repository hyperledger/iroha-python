from ....rust import Enum, make_struct, make_tuple, Dict
FindAllAssets = make_tuple("FindAllAssets")
FindAllAssetsDefinitions = make_tuple("FindAllAssetsDefinitions")
FindAssetById = make_struct("FindAssetById", [("id", "iroha_data_model.expression.EvaluatesTo")])

FindAssetDefinitionById = make_struct("FindAssetDefinitionById", [("id", "iroha_data_model.expression.EvaluatesTo")])

FindAssetDefinitionKeyValueByIdAndKey = make_struct("FindAssetDefinitionKeyValueByIdAndKey", [("id", "iroha_data_model.expression.EvaluatesTo"), ("key", "iroha_data_model.expression.EvaluatesTo")])

FindAssetKeyValueByIdAndKey = make_struct("FindAssetKeyValueByIdAndKey", [("id", "iroha_data_model.expression.EvaluatesTo"), ("key", "iroha_data_model.expression.EvaluatesTo")])

FindAssetQuantityById = make_struct("FindAssetQuantityById", [("id", "iroha_data_model.expression.EvaluatesTo")])

FindAssetsByAccountId = make_struct("FindAssetsByAccountId", [("account_id", "iroha_data_model.expression.EvaluatesTo")])

FindAssetsByAssetDefinitionId = make_struct("FindAssetsByAssetDefinitionId", [("asset_definition_id", "iroha_data_model.expression.EvaluatesTo")])

FindAssetsByDomainId = make_struct("FindAssetsByDomainId", [("domain_id", "iroha_data_model.expression.EvaluatesTo")])

FindAssetsByDomainIdAndAssetDefinitionId = make_struct("FindAssetsByDomainIdAndAssetDefinitionId", [("domain_id", "iroha_data_model.expression.EvaluatesTo"), ("asset_definition_id", "iroha_data_model.expression.EvaluatesTo")])

FindAssetsByName = make_struct("FindAssetsByName", [("name", "iroha_data_model.expression.EvaluatesTo")])

