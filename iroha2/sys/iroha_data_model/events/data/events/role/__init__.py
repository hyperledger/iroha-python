from ......rust import Enum, make_struct, make_tuple, Dict
PermissionRemoved = make_struct("PermissionRemoved", [("role_id", "iroha_data_model.role.Id"), ("permission_definition_id", "iroha_data_model.permissions.Id")])

RoleEvent = Enum[("Created", "iroha_data_model.role.Id"), ("Deleted", "iroha_data_model.role.Id"), ("PermissionRemoved", "iroha_data_model.events.data.events.role.PermissionRemoved")] 
RoleEventFilter = Enum[("ByCreated", type(None)), ("ByDeleted", type(None)), ("ByPermissionRemoved", type(None))] 
RoleFilter = make_struct("RoleFilter", [("origin_filter", "iroha_data_model.events.data.filters.FilterOpt"), ("event_filter", "iroha_data_model.events.data.filters.FilterOpt")])

