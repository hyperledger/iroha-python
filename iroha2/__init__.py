#!/usr/bin/env python
from .sys import Client as _Client
from .data_model.query import Query as _Query
from .data_model.isi import Instruction as _Instruction


class Client:
    def __init__(self, cfg, headers=None):
        if headers is None:
            self.cl = _Client(cfg)
        else:
            self.cl = _Client.with_headers(cfg, headers)

    def tx_body(self, tx: list):
        return self.cl.tx_body(tx, {})

    def submit_tx(self, tx: list):
        tx = [i.to_rust() for i in tx]
        return self.cl.submit_all_with_metadata(tx, {})

    def submit_isi(self, isi):
        return self.submit_tx([_Instruction(isi)])

    def submit_tx_blocking(self, tx: list):
        tx = [i.to_rust() for i in tx]
        return self.cl.submit_all_blocking_with_metadata(tx, {})

    def submit_isi_blocking(self, isi):
        return self.submit_tx_blocking([_Instruction(isi)])

    def query(self, q):
        out = self.cl.request(_Query(q))
        return q.parse_output(out) if hasattr(q, "parse_output") else out

    def listen(self, events_kind):
        return self.cl.listen_for_events(events_kind)
