from ...rust import Enum, Struct, Tuple, Dict
Domain = Struct[("id", "iroha_data_model.domain.Id"), ("accounts", Dict), ("asset_definitions", Dict), ("logo", "iroha_data_model.domain.IpfsPath"), ("metadata", "iroha_data_model.metadata.Metadata")]

Id = Struct[("name", "iroha_data_model.Name")]

IpfsPath = Tuple[str]
NewDomain = Struct[("id", "iroha_data_model.domain.Id"), ("logo", "iroha_data_model.domain.IpfsPath"), ("metadata", "iroha_data_model.metadata.Metadata")]

