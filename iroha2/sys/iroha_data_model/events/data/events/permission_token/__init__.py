
from ......rust import make_enum, make_struct, make_tuple, Dict, get_class
import typing
            
PermissionTokenEvent = make_enum("PermissionTokenEvent", [("DefinitionCreated", get_class("iroha_data_model.permissions.PermissionTokenDefinition")), ("DefinitionDeleted", get_class("iroha_data_model.permissions.PermissionTokenDefinition"))], typing.Union[get_class("iroha_data_model.permissions.PermissionTokenDefinition"), get_class("iroha_data_model.permissions.PermissionTokenDefinition")])
