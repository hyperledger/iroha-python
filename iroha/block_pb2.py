# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: block.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import primitive_pb2 as primitive__pb2
from . import transaction_pb2 as transaction__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='block.proto',
  package='iroha.protocol',
  syntax='proto3',
  serialized_options=b'Z\030iroha.generated/protocol',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0b\x62lock.proto\x12\x0eiroha.protocol\x1a\x0fprimitive.proto\x1a\x11transaction.proto\"\xa3\x02\n\x08\x42lock_v1\x12\x31\n\x07payload\x18\x01 \x01(\x0b\x32 .iroha.protocol.Block_v1.Payload\x12-\n\nsignatures\x18\x02 \x03(\x0b\x32\x19.iroha.protocol.Signature\x1a\xb4\x01\n\x07Payload\x12\x31\n\x0ctransactions\x18\x01 \x03(\x0b\x32\x1b.iroha.protocol.Transaction\x12\x11\n\ttx_number\x18\x02 \x01(\r\x12\x0e\n\x06height\x18\x03 \x01(\x04\x12\x17\n\x0fprev_block_hash\x18\x04 \x01(\t\x12\x14\n\x0c\x63reated_time\x18\x05 \x01(\x04\x12$\n\x1crejected_transactions_hashes\x18\x06 \x03(\t\"F\n\x05\x42lock\x12,\n\x08\x62lock_v1\x18\x01 \x01(\x0b\x32\x18.iroha.protocol.Block_v1H\x00\x42\x0f\n\rblock_versionB\x1aZ\x18iroha.generated/protocolb\x06proto3'
  ,
  dependencies=[primitive__pb2.DESCRIPTOR,transaction__pb2.DESCRIPTOR,])




_BLOCK_V1_PAYLOAD = _descriptor.Descriptor(
  name='Payload',
  full_name='iroha.protocol.Block_v1.Payload',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='transactions', full_name='iroha.protocol.Block_v1.Payload.transactions', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='tx_number', full_name='iroha.protocol.Block_v1.Payload.tx_number', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='height', full_name='iroha.protocol.Block_v1.Payload.height', index=2,
      number=3, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='prev_block_hash', full_name='iroha.protocol.Block_v1.Payload.prev_block_hash', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='created_time', full_name='iroha.protocol.Block_v1.Payload.created_time', index=4,
      number=5, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='rejected_transactions_hashes', full_name='iroha.protocol.Block_v1.Payload.rejected_transactions_hashes', index=5,
      number=6, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=179,
  serialized_end=359,
)

_BLOCK_V1 = _descriptor.Descriptor(
  name='Block_v1',
  full_name='iroha.protocol.Block_v1',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='payload', full_name='iroha.protocol.Block_v1.payload', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='signatures', full_name='iroha.protocol.Block_v1.signatures', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_BLOCK_V1_PAYLOAD, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=68,
  serialized_end=359,
)


_BLOCK = _descriptor.Descriptor(
  name='Block',
  full_name='iroha.protocol.Block',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='block_v1', full_name='iroha.protocol.Block.block_v1', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='block_version', full_name='iroha.protocol.Block.block_version',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=361,
  serialized_end=431,
)

_BLOCK_V1_PAYLOAD.fields_by_name['transactions'].message_type = transaction__pb2._TRANSACTION
_BLOCK_V1_PAYLOAD.containing_type = _BLOCK_V1
_BLOCK_V1.fields_by_name['payload'].message_type = _BLOCK_V1_PAYLOAD
_BLOCK_V1.fields_by_name['signatures'].message_type = primitive__pb2._SIGNATURE
_BLOCK.fields_by_name['block_v1'].message_type = _BLOCK_V1
_BLOCK.oneofs_by_name['block_version'].fields.append(
  _BLOCK.fields_by_name['block_v1'])
_BLOCK.fields_by_name['block_v1'].containing_oneof = _BLOCK.oneofs_by_name['block_version']
DESCRIPTOR.message_types_by_name['Block_v1'] = _BLOCK_V1
DESCRIPTOR.message_types_by_name['Block'] = _BLOCK
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Block_v1 = _reflection.GeneratedProtocolMessageType('Block_v1', (_message.Message,), {

  'Payload' : _reflection.GeneratedProtocolMessageType('Payload', (_message.Message,), {
    'DESCRIPTOR' : _BLOCK_V1_PAYLOAD,
    '__module__' : 'block_pb2'
    # @@protoc_insertion_point(class_scope:iroha.protocol.Block_v1.Payload)
    })
  ,
  'DESCRIPTOR' : _BLOCK_V1,
  '__module__' : 'block_pb2'
  # @@protoc_insertion_point(class_scope:iroha.protocol.Block_v1)
  })
_sym_db.RegisterMessage(Block_v1)
_sym_db.RegisterMessage(Block_v1.Payload)

Block = _reflection.GeneratedProtocolMessageType('Block', (_message.Message,), {
  'DESCRIPTOR' : _BLOCK,
  '__module__' : 'block_pb2'
  # @@protoc_insertion_point(class_scope:iroha.protocol.Block)
  })
_sym_db.RegisterMessage(Block)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
