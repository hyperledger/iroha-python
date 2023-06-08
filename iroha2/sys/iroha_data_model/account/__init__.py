
from ...rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
Account = make_struct("Account", [("id", "iroha_data_model.account.Id"), ("assets", Dict), ("signatories", list), ("signature_check_condition", "iroha_data_model.account.SignatureCheckCondition"), ("metadata", "iroha_data_model.metadata.Metadata"), ("roles", list)])

Id = make_struct("Id", [("name", "iroha_data_model.name.Name"), ("domain_id", "iroha_data_model.domain.Id")])

NewAccount = make_struct("NewAccount", [("id", "iroha_data_model.account.Id"), ("signatories", list), ("metadata", "iroha_data_model.metadata.Metadata")])

SignatureCheckCondition = make_tuple("SignatureCheckCondition", ["iroha_data_model.expression.EvaluatesTo"])
SelfResolvingTypeVar.resolve_all()
