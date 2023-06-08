from typing import Union, Optional

from ...sys.iroha_data_model.asset import (
    Asset,
    AssetDefinition as _Definition,
    NewAssetDefinition as NewDefinition,
    AssetDefinitionEntry as DefinitionEntry,
    AssetValue as Value,
    AssetValueType as ValueType,
    DefinitionId as _DefinitionId,
    Id as _Id,
    Mintable,
)
from ..domain import Id as DomainId
from ..account import Id as AccountId
from ..isi import Registrable
from .. import wrapper, patch


@wrapper(_Id)
class Id(_Id, Registrable):

    @patch(_Id, "to_rust")
    def __repr__(self):
        return f"{self.definition_id}#{self.account_id}"

    @patch(_Id, "from_rust")
    @classmethod
    def parse(cls, asset_id):
        definition_name, domain_name, account_id = asset_id.rsplit("#")
        account_id = AccountId.parse(account_id)

        if domain_name == "":
            domain_id = account_id.domain_id
        else:
            domain_id = DomainId(domain_name)

        return Id(DefinitionId(definition_name, domain_id), account_id)


@wrapper(_DefinitionId)
class DefinitionId(_DefinitionId, Registrable):

    @patch(_DefinitionId, "to_rust")
    def __repr__(self):
        return f"{self.name}#{self.domain_id}"

    @patch(_DefinitionId, "from_rust")
    @classmethod
    def parse(cls, addr):
        "Parses the definition id from address in form of name#domain"
        name, domain_id = addr.split('#')
        return DefinitionId(name=name, domain_id=DomainId(domain_id))


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
