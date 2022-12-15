
from ......rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
PermissionRemoved = make_struct("PermissionRemoved", [("role_id", "iroha_data_model.role.Id"), ("permission_definition_id", "iroha_data_model.permission.token.Id")])

RoleEvent = make_enum("RoleEvent", [("Created", get_class("iroha_data_model.role.Id")), ("Deleted", get_class("iroha_data_model.role.Id")), ("PermissionRemoved", get_class("iroha_data_model.events.data.events.role.PermissionRemoved"))], typing.Union[get_class("iroha_data_model.role.Id"), get_class("iroha_data_model.role.Id"), get_class("iroha_data_model.events.data.events.role.PermissionRemoved")])

RoleEventFilter = make_enum("RoleEventFilter", [("ByCreated", get_class(type(None))), ("ByDeleted", get_class(type(None))), ("ByPermissionRemoved", get_class(type(None)))], typing.Union[get_class(type(None)), get_class(type(None)), get_class(type(None))])

RoleFilter = make_struct("RoleFilter", [("origin_filter", "iroha_data_model.events.data.filters.FilterOpt"), ("event_filter", "iroha_data_model.events.data.filters.FilterOpt")])

SelfResolvingTypeVar.resolve_all()
