from ...rust import Enum, make_struct, make_tuple, Dict
Event = Enum[("Pipeline", "iroha_data_model.events.pipeline.Event"), ("Data", "iroha_data_model.events.data.events.Event"), ("Time", "iroha_data_model.events.time.Event"), ("ExecuteTrigger", "iroha_data_model.events.execute_trigger.Event")] 
EventPublisherMessage = Enum[("SubscriptionAccepted", type(None)), ("Event", "iroha_data_model.events.Event")] 
EventSubscriberMessage = Enum[("SubscriptionRequest", "iroha_data_model.events.FilterBox"), ("EventReceived", type(None))] 
FilterBox = Enum[("Pipeline", "iroha_data_model.events.pipeline.EventFilter"), ("Data", "iroha_data_model.events.data.filters.FilterOpt"), ("Time", "iroha_data_model.events.time.EventFilter"), ("ExecuteTrigger", "iroha_data_model.events.execute_trigger.EventFilter")] 
VersionedEventPublisherMessage = Enum[("V1", "iroha_data_model.events.EventPublisherMessage")] 
VersionedEventSubscriberMessage = Enum[("V1", "iroha_data_model.events.EventSubscriberMessage")] 
