from ...rust import Enum, Struct, Tuple, Dict

Account = Struct[("id", "iroha_data_model.account.Id"), ("assets", Dict),
                 ("signatories", list), ("permission_tokens", "BTreeSet"),
                 ("signature_check_condition",
                  "iroha_data_model.account.SignatureCheckCondition"),
                 ("metadata", "iroha_data_model.metadata.Metadata")]

Id = Struct[("name", str), ("domain_name", str)]

NewAccount = Struct[("id", "iroha_data_model.account.Id"),
                    ("signatories", list),
                    ("metadata", "iroha_data_model.metadata.Metadata")]

SignatureCheckCondition = Tuple["iroha_data_model.expression.EvaluatesTo"]
