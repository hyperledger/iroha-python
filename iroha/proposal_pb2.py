# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proposal.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import transaction_pb2 as transaction__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0eproposal.proto\x12\x0eiroha.protocol\x1a\x11transaction.proto\"c\n\x08Proposal\x12\x0e\n\x06height\x18\x01 \x01(\x04\x12\x31\n\x0ctransactions\x18\x02 \x03(\x0b\x32\x1b.iroha.protocol.Transaction\x12\x14\n\x0c\x63reated_time\x18\x03 \x01(\x04\x42\x1aZ\x18iroha.generated/protocolb\x06proto3')



_PROPOSAL = DESCRIPTOR.message_types_by_name['Proposal']
Proposal = _reflection.GeneratedProtocolMessageType('Proposal', (_message.Message,), {
  'DESCRIPTOR' : _PROPOSAL,
  '__module__' : 'proposal_pb2'
  # @@protoc_insertion_point(class_scope:iroha.protocol.Proposal)
  })
_sym_db.RegisterMessage(Proposal)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
