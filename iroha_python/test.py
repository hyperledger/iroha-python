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
register = Instruction(Register(Expression(Value(Identifiable(domain)))))

hash = cl.submit_isi(register)

filter = EventFilter.Pipeline(pipeline.EventFilter(
    entity=pipeline.EntityType.Transaction(),
    hash=None,
))
listener = cl.listen(filter)

# Strange thing -- ws doesnt work as an iterator
while True:
    ev = listener.__next__()
    if ev["Ok"]["Pipeline"]["status"] != "Committed":
        continue
    if ev["Ok"]["Pipeline"]["hash"] != hash:
        continue
    break
