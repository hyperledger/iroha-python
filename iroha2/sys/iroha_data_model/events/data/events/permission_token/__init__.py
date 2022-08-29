from ......rust import Enum, make_struct, make_tuple, Dict
PermissionTokenEvent = Enum[("DefinitionCreated", "iroha_data_model.permissions.PermissionTokenDefinition"), ("DefinitionDeleted", "iroha_data_model.permissions.PermissionTokenDefinition")] 
