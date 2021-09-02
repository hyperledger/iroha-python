#!/usr/bin/env python3
import iroha2
import json

from iroha2 import Client
from iroha2.data_model.isi import *
from iroha2.data_model.domain import *
from iroha2.data_model.expression import *
from iroha2.data_model.events import EventFilter, pipeline
from iroha2.data_model import *

cfg = json.loads(open("./config.json").read())
cl = Client(cfg)

domain = Domain("xor")
register = Register(Expression(Value(Identifiable(domain))))

hash = cl.submit_isi(register)

filter = EventFilter.Pipeline(
    pipeline.EventFilter(
        entity=pipeline.EntityType.Transaction(),
        hash=None,
    ))
listener = cl.listen(filter)

for event in listener:
    print(event)

    if event["Pipeline"]["status"] == "Committed" \
        and event["Pipeline"]["hash"] == hash:

        break
