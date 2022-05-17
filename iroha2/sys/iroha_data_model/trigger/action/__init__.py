from ....rust import Enum, Struct, Tuple, Dict
Action = Struct[("executable", "iroha_data_model.transaction.Executable"), ("repeats", "iroha_data_model.trigger.action.Repeats"), ("technical_account", "iroha_data_model.account.Id"), ("filter", "iroha_data_model.events.FilterBox"), ("metadata", "iroha_data_model.metadata.Metadata")]

Repeats = Enum[("Indefinitely", type(None)), ("Exactly", "AtomicU32Wrapper")] 
