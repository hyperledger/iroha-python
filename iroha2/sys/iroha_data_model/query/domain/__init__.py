
from ....rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
FindAllDomains = make_tuple("FindAllDomains")
FindDomainById = make_struct("FindDomainById", [("id", "iroha_data_model.expression.EvaluatesTo")])

FindDomainKeyValueByIdAndKey = make_struct("FindDomainKeyValueByIdAndKey", [("id", "iroha_data_model.expression.EvaluatesTo"), ("key", "iroha_data_model.expression.EvaluatesTo")])

SelfResolvingTypeVar.resolve_all()
