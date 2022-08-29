from ...sys.rust import query
from ...sys.iroha_data_model.query.asset import (
    FindAllAssets,
    FindAllAssetsDefinitions,
    FindAssetById as _FindAssetById,
    FindAssetDefinitionKeyValueByIdAndKey,
    FindAssetKeyValueByIdAndKey,
    FindAssetQuantityById,
    FindAssetsByAccountId,
    FindAssetsByAssetDefinitionId,
    FindAssetsByName,
)

from ..expression import Expression
from .. import Value, Identifiable, Id
from .. import wrapper


@wrapper(_FindAssetById)
class FindAssetById(_FindAssetById, query("Identifiable", "Asset")):

    @classmethod
    def id(cls, asset_id):
        return cls(Expression(Value(Id(asset_id))))
