from ...rust import Enum, Struct, Tuple, Dict

EventFilter = Enum[("Pipeline",
                    "iroha_data_model.events.pipeline.EventFilter"),
                   ("Data", "iroha_data_model.events.data.EventFilter")]
