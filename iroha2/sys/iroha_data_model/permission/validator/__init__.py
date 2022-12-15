
from ....rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
Id = make_struct("Id", [("name", "iroha_data_model.name.Name"), ("account_id", "iroha_data_model.account.Id")])

Type = make_enum("Type", [("Transaction", get_class(type(None))), ("Instruction", get_class(type(None))), ("Query", get_class(type(None))), ("Expression", get_class(type(None)))], typing.Union[get_class(type(None)), get_class(type(None)), get_class(type(None)), get_class(type(None))])

Validator = make_struct("Validator", [("id", "iroha_data_model.permission.validator.Id"), ("validator_type", "iroha_data_model.permission.validator.Type"), ("wasm", "iroha_data_model.transaction.WasmSmartContract")])

SelfResolvingTypeVar.resolve_all()
