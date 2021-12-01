from ...sys.iroha_data_model.asset import (
    Asset,
    AssetDefinition as Definition,
    AssetDefinitionEntry as DefinitionEntry,
    AssetValue as Value,
    AssetValueType as ValueType,
    DefinitionId as _DefinitionId,
    Id,
)


class DefinitionId(_DefinitionId):
    @classmethod
    def parse(cls, addr):
        "Parses the definition id from address in form of name#domain"
        name, domain_name = addr.split('#')
        return cls(name=name, domain_name=domain_name)
