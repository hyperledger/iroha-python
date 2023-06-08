
from ......rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
PermissionTokenEvent = make_enum("PermissionTokenEvent", [("DefinitionCreated", get_class("iroha_data_model.permission.token.Definition")), ("DefinitionDeleted", get_class("iroha_data_model.permission.token.Definition"))], typing.Union[get_class("iroha_data_model.permission.token.Definition"), get_class("iroha_data_model.permission.token.Definition")])

PermissionValidatorEvent = make_enum("PermissionValidatorEvent", [("Added", get_class("iroha_data_model.permission.validator.Id")), ("Removed", get_class("iroha_data_model.permission.validator.Id"))], typing.Union[get_class("iroha_data_model.permission.validator.Id"), get_class("iroha_data_model.permission.validator.Id")])

SelfResolvingTypeVar.resolve_all()
