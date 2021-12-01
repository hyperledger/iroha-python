from ...sys.iroha_data_model.isi import (
    BurnBox as Burn,
    FailBox as Fail,
    GrantBox as Grant,
    MintBox as Mint,
    RegisterBox as _Register,
    RemoveKeyValueBox as RemoveKeyValue,
    SequenceBox as Sequence,
    SetKeyValueBox as SetKeyValue,
    TransferBox as Transfer,
    UnregisterBox as _Unregister,
    If,
    Instruction,
    Pair,
)
from iroha2.data_model.expression import Expression
from iroha2.data_model import Value, Identifiable, Id


class Register(_Register):
    @classmethod
    def identifiable(cls, identifiable):
        "Creates instruction with raw identifiable"
        return cls(Expression(Value(Identifiable(identifiable))))


class Unregister(_Unregister):
    @classmethod
    def id(cls, id):
        "Creates instruction with raw id"
        return cls(Expression(Value(Id(id))))
