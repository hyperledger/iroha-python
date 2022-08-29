#!/usr/bin/env python3
import json

from iroha2 import Client

from iroha2.data_model.isi import Register
from iroha2.data_model.domain import Domain
from iroha2.data_model.account import Account
from iroha2.data_model import asset, account
from iroha2.data_model.events import FilterBox, pipeline
from iroha2.crypto import KeyPair


def wait_for_tx(cl: Client, hash: str):
    filter = FilterBox.Pipeline(
        pipeline.EventFilter(
            entity_kind=pipeline.EntityKind.Transaction(),
            status_kind=None,
            hash=None,
        ))

    listener = cl.listen(filter)

    for event in listener:
        if event.variant is event.Type.Pipeline:
            if event.value.hash == hash:
                if event.value.status.variant is pipeline.Status.Type.Committed:
                    return
                elif event.value.status.variant is pipeline.Status.Type.Validating:
                    pass
                else:
                    raise RuntimeError(f"Tx rejected: {event.value.status}")


cfg = json.loads(open("./config.json").read())
cl = Client(cfg)

domain = Domain("python")
register = Register.identifiable(domain)
hash = cl.submit_isi(register)
wait_for_tx(cl, hash)

asset_definition = asset.Definition(
    "pyasset#python",
    asset.ValueType.Quantity(),
    asset.Mintable.Infinitely(),
)
register = Register.identifiable(asset_definition)
hash = cl.submit_isi(register)
wait_for_tx(cl, hash)

keypair = KeyPair()
acct = account.Account("monty@python", signatories=[keypair.public])
register = Register.identifiable(acct)
hash = cl.submit_isi(register)
wait_for_tx(cl, hash)
