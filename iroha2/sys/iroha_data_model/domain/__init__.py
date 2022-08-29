from ...rust import Enum, make_struct, make_tuple, Dict
Domain = make_struct("Domain", [("id", "iroha_data_model.domain.Id"), ("accounts", Dict), ("asset_definitions", Dict), ("logo", "iroha_data_model.domain.IpfsPath"), ("metadata", "iroha_data_model.metadata.Metadata")])

Id = make_struct("Id", [("name", "iroha_data_model.name.Name")])

IpfsPath = make_tuple("IpfsPath", [str])
NewDomain = make_struct("NewDomain", [("id", "iroha_data_model.domain.Id"), ("logo", "iroha_data_model.domain.IpfsPath"), ("metadata", "iroha_data_model.metadata.Metadata")])

