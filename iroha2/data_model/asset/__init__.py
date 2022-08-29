from typing import Union, Optional

from ...sys.iroha_data_model.asset import (
    Asset,
    AssetDefinition as _Definition,
    NewAssetDefinition as NewDefinition,
    AssetDefinitionEntry as DefinitionEntry,
    AssetValue as Value,
    AssetValueType as ValueType,
    DefinitionId as _DefinitionId,
    Id,
    Mintable,
)
from ..domain import Id as DomainId
from ..isi import Registrable
from .. import wrapper


@wrapper(_DefinitionId)
class DefinitionId(_DefinitionId, Registrable):

    @classmethod
    def parse(cls, addr):
        "Parses the definition id from address in form of name#domain"
        name, domain_id = addr.split('#')
        return cls(name=name, domain_id=DomainId(domain_id))


@wrapper(_Definition)
class Definition(_Definition, Registrable):

    def __init__(self,
                 id: Union[str, DefinitionId],
                 value_type: ValueType,
                 mintable: Mintable,
                 metadata: Optional[dict] = None):

        if metadata is None:
            metadata = {}

        if isinstance(id, str):
            id = DefinitionId.parse(id)

        return super().__init__(id=id,
                                value_type=value_type,
                                mintable=mintable,
                                metadata=metadata)

    def registrable(self):
        return NewDefinition(self.id, self.value_type, self.mintable,
                             self.metadata)
