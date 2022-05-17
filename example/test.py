#!/usr/bin/env python3
import iroha2
import json

from iroha2 import Client

from iroha2.data_model import domain
from iroha2.data_model.isi import *
from iroha2.data_model.domain import *
from iroha2.data_model.expression import *
from iroha2.data_model.events import FilterBox, pipeline
from iroha2.data_model import *

cfg = json.loads(open("./config.json").read())
cl = Client(cfg)

domain = NewDomain("iroha_python")
register = Register.identifiable(domain)

hash = cl.submit_isi(register)

filter = FilterBox.Pipeline(
    pipeline.EventFilter(
        entity_kind=pipeline.EntityKind.Transaction(),
        status_kind=pipeline.StatusKind.Committed(),
        hash=None,
    ))
listener = cl.listen(filter)

for event in listener:
    print(event)

    if event["Pipeline"]["status"] == "Committed" \
        and event["Pipeline"]["hash"] == hash:

        break
