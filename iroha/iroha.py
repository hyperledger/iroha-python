#!/usr/bin/env python3
#
# Copyright Soramitsu Co., Ltd. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
#

from . import ed25519 as ed25519_sha3
import nacl.signing as ed25519_sha2
import hashlib
import binascii
import grpc
import time
import re
import os

from . import commands_pb2
from . import endpoint_pb2
from . import endpoint_pb2_grpc
from . import primitive_pb2
from . import queries_pb2
from . import transaction_pb2


class IrohaCrypto(object):
    """
    Collection of general crypto-related functions
    """

    @staticmethod
    def derive_public_key(private_key):
        """
        Calculate public key from private key
        :param private_key: hex encoded private key
        :return: hex encoded public key
        """
        if isinstance(private_key, (str, bytes)):  # default, legacy
            secret = binascii.unhexlify(private_key)
            public_key = ed25519_sha3.publickey_unsafe(secret)
            hex_public_key = binascii.hexlify(public_key)
            return hex_public_key
        elif isinstance(private_key, ed25519_sha2.SigningKey):
            return 'ed0120' + binascii.hexlify(private_key.verify_key._key).decode("utf-8")

    @staticmethod
    def get_payload_to_be_signed(proto):
        """
        :proto: proto transaction or query
        :return: bytes representation of what has to be signed
        """
        if hasattr(proto, 'payload'):
            return proto.payload.SerializeToString()
        # signing of meta is implemented for block streaming queries,
        # because they do not have a payload in their schema
        elif hasattr(proto, 'meta'):
            return proto.meta.SerializeToString()
        raise RuntimeError('Unknown message type.')

    @staticmethod
    def hash(proto_with_payload):
        """
        Calculates hash of payload of proto message
        :proto_with_payload: proto transaction or query
        :return: bytes representation of hash
        """
        obj = IrohaCrypto.get_payload_to_be_signed(proto_with_payload)
        hash = hashlib.sha3_256(obj).digest()
        return hash

    @staticmethod
    def _signature(message, private_key):
        """
        Calculate signature for given message and private key
        :param message: proto that has payload message inside
        :param private_key: hex string with private key
        :return: a proto Signature message
        """
        public_key = IrohaCrypto.derive_public_key(private_key)
        if isinstance(private_key, (str, bytes)):  # default, legacy
            message_hash = IrohaCrypto.hash(message)
            sk = binascii.unhexlify(private_key)
            pk = binascii.unhexlify(public_key)
            signature_bytes = ed25519_sha3.signature_unsafe(
                message_hash, sk, pk)
        elif isinstance(private_key, ed25519_sha2.SigningKey):
            signature_bytes = private_key.sign(
                IrohaCrypto.get_payload_to_be_signed(message)).signature
        else:
            raise RuntimeError('Unsupported private key type.')
        signature = primitive_pb2.Signature()
        signature.public_key = public_key
        signature.signature = binascii.hexlify(signature_bytes)
        return signature

    @staticmethod
    def sign_transaction(transaction, *private_keys):
        """
        Add specified signatures to a transaction. Source transaction will be modified
        :param transaction: the transaction to be signed
        :param private_keys: hex strings of private keys to sign the transaction
        :return: the modified transaction
        """
        assert len(private_keys), 'At least one private key has to be passed'
        signatures = []
        for private_key in private_keys:
            signature = IrohaCrypto._signature(transaction, private_key)
            signatures.append(signature)
        transaction.signatures.extend(signatures)
        return transaction

    @staticmethod
    def sign_query(query, private_key):
        """
        Add a signature to a query. Source query will be modified
        :param query: the query to be signed
        :param private_key: hex string of private key to sign the query
        :return: the modified query
        """
        signature = IrohaCrypto._signature(query, private_key)
        query.signature.CopyFrom(signature)
        return query

    @staticmethod
    def is_sha2_signature_valid(message, signature):
        """
        Verify sha2 signature validity.
        :param signature: the signature to be checked
        :param message: message to check the signature against
        :return: bool, whether the signature is valid for the message
        """
        parse_message = IrohaCrypto.get_payload_to_be_signed(message)
        signature_bytes = binascii.unhexlify(signature.signature)
        public_key = ed25519_sha2.VerifyKey(binascii.unhexlify(signature.public_key)[3:])
        valid_message = ed25519_sha2.VerifyKey.verify(public_key, parse_message, signature_bytes)
        if valid_message == parse_message:
            return True
        return False

    @staticmethod
    def is_signature_valid(message, signature):
        """
        Verify sha3 signature validity. To check sha2 signature need use the "is_sha2_signature_valid" method
        :param signature: the signature to be checked
        :param message: message to check the signature against
        :return: bool, whether the signature is valid for the message
        """
        message_hash = IrohaCrypto.hash(message)
        try:
            signature_bytes = binascii.unhexlify(signature.signature)
            public_key = binascii.unhexlify(signature.public_key)
            ed25519_sha3.checkvalid(signature_bytes, message_hash, public_key)
            return True
        except (ed25519_sha3.SignatureMismatch, ValueError):
            return False

    @staticmethod
    def reduced_hash(transaction):
        """
        Calculates hash of reduced payload of a transaction
        :param transaction: transaction to be processed
        :return: hex representation of hash
        """
        bytes = transaction.payload.reduced_payload.SerializeToString()
        hash = hashlib.sha3_256(bytes).digest()
        hex_hash = binascii.hexlify(hash)
        return hex_hash

    @staticmethod
    def private_key():
        """
        Generates new random ed25519/sha3 private key
        :return: hex representation of private key
        """
        return binascii.b2a_hex(os.urandom(32))


class Iroha(object):
    """
    Collection of factory methods for transactions and queries creation
    """

    def __init__(self, creator_account=None):
        self.creator_account = creator_account

    @staticmethod
    def _camel_case_to_snake_case(camel_case_string):
        """Transforms"""
        tmp = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camel_case_string)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', tmp).lower()

    @staticmethod
    def now():
        """Current timestamp in milliseconds"""
        return int(round(time.time() * 1000))

    def transaction(self, commands, quorum=1,
                    creator_account=None, created_time=None):
        """
        Creates a protobuf transaction with specified set of entities
        :param commands: list of commands generated via command factory method
        :param quorum: required number of signatures, 1 is default
        :param creator_account: id of transaction creator account
        :param created_time: transaction creation timestamp in milliseconds
        :return: a proto transaction
        """
        assert creator_account or self.creator_account, \
            "No account name specified as transaction creator id"
        if not created_time:
            created_time = self.now()
        if not creator_account:
            creator_account = self.creator_account
        tx = transaction_pb2.Transaction()
        core_payload = tx.payload.reduced_payload
        # setting transaction contents
        core_payload.quorum = quorum
        core_payload.created_time = created_time
        core_payload.creator_account_id = creator_account
        core_payload.commands.extend(commands)
        return tx

    @staticmethod
    def command(name, **kwargs):
        """
        Creates a protobuf command to be inserted into a transaction
        :param name: CamelCased name of command
        :param kwargs: command arguments as they defined in schema
        :return: a proto command

        Usage example:
        cmd = Iroha.command('CreateDomain', domain_id='test', default_role='user')
        """
        command_wrapper = commands_pb2.Command()
        field_name = Iroha._camel_case_to_snake_case(name)
        internal_command = getattr(command_wrapper, field_name)
        for key, value in kwargs.items():
            if 'permissions' == key:
                permissions_attr = getattr(internal_command, key)
                permissions_attr.extend(value)
                continue
            if 'peer' == key:
                peer_attr = getattr(internal_command, key)
                peer_attr.CopyFrom(value)
                continue
            setattr(internal_command, key, value)
        return command_wrapper

    def query(self, name, counter=1, creator_account=None,
              created_time=None, page_size=None, first_tx_hash=None,
              **kwargs):
        """
        Creates a protobuf query with specified set of entities
        :param name: CamelCased name of query to be executed
        :param counter: query counter, should be incremented for each new query
        :param creator_account: account id of query creator
        :param created_time: query creation timestamp in milliseconds
        :param page_size: a non-zero positive number, size of result rowset for queries with pagination
        :param first_tx_hash: optional hash of a transaction that will be the beginning of the next page
        :param kwargs: query arguments as they defined in schema
        :return: a proto query
        """
        assert creator_account or self.creator_account, \
            "No account name specified as query creator id"
        pagination_meta = None
        if not created_time:
            created_time = self.now()
        if not creator_account:
            creator_account = self.creator_account
        if page_size or first_tx_hash:
            pagination_meta = queries_pb2.TxPaginationMeta()
            pagination_meta.page_size = page_size
            if first_tx_hash:
                pagination_meta.first_tx_hash = first_tx_hash

        meta = queries_pb2.QueryPayloadMeta()
        meta.created_time = created_time
        meta.creator_account_id = creator_account
        meta.query_counter = counter

        query_wrapper = queries_pb2.Query()
        query_wrapper.payload.meta.CopyFrom(meta)
        field_name = Iroha._camel_case_to_snake_case(name)
        internal_query = getattr(query_wrapper.payload, field_name)
        for key, value in kwargs.items():
            if 'tx_hashes' == key:
                hashes_attr = getattr(internal_query, key)
                hashes_attr.extend(value)
                continue
            setattr(internal_query, key, value)
        if pagination_meta:
            pagination_meta_attr = getattr(internal_query, 'pagination_meta')
            pagination_meta_attr.CopyFrom(pagination_meta)
        if not len(kwargs):
            message = getattr(queries_pb2, name)()
            internal_query.CopyFrom(message)
        return query_wrapper

    def blocks_query(self, counter=1, creator_account=None, created_time=None):
        """
        Creates a protobuf query for a blocks stream
        :param counter: query counter, should be incremented for each new query
        :param creator_account: account id of query creator
        :param created_time: query creation timestamp in milliseconds
        :return: a proto blocks query
        """
        if not created_time:
            created_time = self.now()
        if not creator_account:
            creator_account = self.creator_account

        meta = queries_pb2.QueryPayloadMeta()
        meta.created_time = created_time
        meta.creator_account_id = creator_account
        meta.query_counter = counter

        query_wrapper = queries_pb2.BlocksQuery()
        query_wrapper.meta.CopyFrom(meta)
        return query_wrapper

    @staticmethod
    def batch(transactions, atomic=True):
        """
        Tie transactions to be a single batch. All of them will have a common batch meta.
        :param transactions: list of transactions to be tied into a batch
        :param atomic: boolean - prescribes type of batch: ATOMIC if true, otherwise - ORDERED
        :return: nothing, source transactions will be modified
        """
        meta_ref = transaction_pb2.Transaction.Payload.BatchMeta
        batch_type = meta_ref.ATOMIC if atomic else meta_ref.ORDERED
        reduced_hashes = []
        for transaction in transactions:
            reduced_hash = IrohaCrypto.reduced_hash(transaction)
            reduced_hashes.append(reduced_hash)
        meta = meta_ref()
        meta.type = batch_type
        meta.reduced_hashes.extend(reduced_hashes)
        for transaction in transactions:
            transaction.payload.batch.CopyFrom(meta)


class IrohaGrpc(object):
    """
    Possible implementation of gRPC transport to Iroha
    """

    def __init__(self, address=None, timeout=None, secure=False, *, max_message_length=None):
        """
        Create Iroha gRPC client
        :param address: Iroha Torii address with port, example "127.0.0.1:50051"
        :param timeout: timeout for network I/O operations in seconds
        :param secure: enable grpc ssl channel
        :param max_message_length: it is max message length in bytes for grpc
        """
        self._address = address if address else '127.0.0.1:50051'

        channel_kwargs = {}
        if max_message_length is not None:
            channel_kwargs['options'] = [
                ('grpc.max_send_message_length', max_message_length),
                ('grpc.max_receive_message_length', max_message_length)]

        if secure:
            self._channel = grpc.secure_channel(self._address, grpc.ssl_channel_credentials(), **channel_kwargs)
        else:
            self._channel = grpc.insecure_channel(self._address, **channel_kwargs)

        self._timeout = timeout
        self._command_service_stub = endpoint_pb2_grpc.CommandService_v1Stub(
            self._channel)
        self._query_service_stub = endpoint_pb2_grpc.QueryService_v1Stub(
            self._channel)

    def send_tx(self, transaction, timeout=None):
        """
        Send a transaction to Iroha
        :param transaction: protobuf Transaction
        :param timeout: timeout for network I/O operations in seconds
        :return: None
        :raise: grpc.RpcError with .code() available in case of any error
        """
        if not timeout:
            timeout = self._timeout
        self._command_service_stub.Torii(transaction, timeout=timeout)

    def send_txs(self, transactions, timeout=None):
        """
        Send a series of transactions to Iroha at once.
        Useful for submitting batches of transactions.
        :param transactions: list of protobuf transactions to be sent
        :param timeout: timeout for network I/O operations in seconds
        :return: None
        :raise: grpc.RpcError with .code() available in case of any error
        """
        if not timeout:
            timeout = self._timeout
        tx_list = endpoint_pb2.TxList()
        tx_list.transactions.extend(transactions)
        self._command_service_stub.ListTorii(tx_list, timeout=timeout)

    def send_query(self, query, timeout=None):
        """
        Send a query to Iroha
        :param query: protobuf Query
        :param timeout: timeout for network I/O operations in seconds
        :return: a protobuf response to the query
        :raise: grpc.RpcError with .code() available in case of any error
        """
        if not timeout:
            timeout = self._timeout
        response = self._query_service_stub.Find(query, timeout=timeout)
        return response

    def send_blocks_stream_query(self, query, timeout=None):
        """
        Send a query for blocks stream to Iroha
        :param query: protobuf BlocksQuery
        :param timeout: timeout for network I/O operations in seconds
        :return: an iterable over a stream of blocks
        :raise: grpc.RpcError with .code() available in case of any error
        """
        if not timeout:
            timeout = self._timeout
        response = self._query_service_stub.FetchCommits(
            query, timeout=timeout)
        for block in response:
            yield block

    def tx_status(self, transaction, timeout=None):
        """
        Request a status of a transaction
        :param transaction: the transaction, which status is about to be known
        :param timeout: timeout for network I/O operations in seconds
        :return: a tuple with the symbolic status description,
        integral status code, and error code (will be 0 if no error occurred)
        :raise: grpc.RpcError with .code() available in case of any error
        """
        if not timeout:
            timeout = self._timeout
        request = endpoint_pb2.TxStatusRequest()
        request.tx_hash = binascii.hexlify(IrohaCrypto.hash(transaction))
        response = self._command_service_stub.Status(request, timeout=timeout)
        return self._parse_tx_status(response)

    def tx_status_stream(self, transaction, timeout=None):
        """
        Generator of transaction statuses from status stream
        :param transaction: the transaction, which status is about to be known
        :param timeout: timeout for network I/O operations in seconds
        :return: an iterable over a series of tuples with symbolic status description,
        integral status code, and error code (will be 0 if no error occurred)
        :raise: grpc.RpcError with .code() available in case of any error
        """
        tx_hash = IrohaCrypto.hash(transaction)
        yield from self.tx_hash_status_stream(tx_hash, timeout)

    def tx_hash_status_stream(self, transaction_hash: "str or bytes", timeout=None):
        """
        Generator of transaction statuses from status stream
        :param transaction_hash: the hash of transaction, which status is about to be known
        :param timeout: timeout for network I/O operations in seconds
        :return: an iterable over a series of tuples with symbolic status description,
        integral status code, and error code (will be 0 if no error occurred)
        :raise: grpc.RpcError with .code() available in case of any error
        """
        if not timeout:
            timeout = self._timeout
        request = endpoint_pb2.TxStatusRequest()
        if isinstance(transaction_hash, bytes):
            request.tx_hash = binascii.hexlify(transaction_hash)
        else:
            request.tx_hash = transaction_hash.encode('utf-8')
        response = self._command_service_stub.StatusStream(
            request, timeout=timeout)
        for status in response:
            status_name, status_code, error_code = self._parse_tx_status(
                status)
            yield status_name, status_code, error_code

    @staticmethod
    def _parse_tx_status(response):
        """
        Parse protocol.ToriiResponse into a tuple
        :param response: response to be parsed
        :return: a tuple with the symbolic status description,
        integral status code, and error code (will be 0 if no error occurred)
        """
        status_name = endpoint_pb2.TxStatus.Name(response.tx_status)
        status_code = response.tx_status
        error_code = response.error_code
        return status_name, status_code, error_code
