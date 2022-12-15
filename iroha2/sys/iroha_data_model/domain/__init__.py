
from ...rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
Domain = make_struct("Domain", [("id", "iroha_data_model.domain.Id"), ("accounts", Dict), ("asset_definitions", Dict), ("asset_total_quantities", Dict), ("logo", "iroha_data_model.domain.IpfsPath"), ("metadata", "iroha_data_model.metadata.Metadata")])

Id = make_struct("Id", [("name", "iroha_data_model.name.Name")])

IpfsPath = make_tuple("IpfsPath", [str])
NewDomain = make_struct("NewDomain", [("id", "iroha_data_model.domain.Id"), ("logo", "iroha_data_model.domain.IpfsPath"), ("metadata", "iroha_data_model.metadata.Metadata")])

SelfResolvingTypeVar.resolve_all()
