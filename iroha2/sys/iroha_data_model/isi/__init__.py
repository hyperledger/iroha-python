
from ...rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
BurnBox = make_struct("BurnBox", [("object", "iroha_data_model.expression.EvaluatesTo"), ("destination_id", "iroha_data_model.expression.EvaluatesTo")])

ExecuteTriggerBox = make_struct("ExecuteTriggerBox", [("trigger_id", "iroha_data_model.trigger.Id")])

FailBox = make_struct("FailBox", [("message", str)])

GrantBox = make_struct("GrantBox", [("object", "iroha_data_model.expression.EvaluatesTo"), ("destination_id", "iroha_data_model.expression.EvaluatesTo")])

If = make_struct("If", [("condition", "iroha_data_model.expression.EvaluatesTo"), ("then", "iroha_data_model.isi.Instruction"), ("otherwise", "iroha_data_model.isi.Instruction")])

Instruction = make_enum("Instruction", [("Register", get_class("iroha_data_model.isi.RegisterBox")), ("Unregister", get_class("iroha_data_model.isi.UnregisterBox")), ("Mint", get_class("iroha_data_model.isi.MintBox")), ("Burn", get_class("iroha_data_model.isi.BurnBox")), ("Transfer", get_class("iroha_data_model.isi.TransferBox")), ("If", get_class("iroha_data_model.isi.If")), ("Pair", get_class("iroha_data_model.isi.Pair")), ("Sequence", get_class("iroha_data_model.isi.SequenceBox")), ("Fail", get_class("iroha_data_model.isi.FailBox")), ("SetKeyValue", get_class("iroha_data_model.isi.SetKeyValueBox")), ("RemoveKeyValue", get_class("iroha_data_model.isi.RemoveKeyValueBox")), ("Grant", get_class("iroha_data_model.isi.GrantBox")), ("Revoke", get_class("iroha_data_model.isi.RevokeBox")), ("ExecuteTrigger", get_class("iroha_data_model.isi.ExecuteTriggerBox"))], typing.Union[get_class("iroha_data_model.isi.RegisterBox"), get_class("iroha_data_model.isi.UnregisterBox"), get_class("iroha_data_model.isi.MintBox"), get_class("iroha_data_model.isi.BurnBox"), get_class("iroha_data_model.isi.TransferBox"), get_class("iroha_data_model.isi.If"), get_class("iroha_data_model.isi.Pair"), get_class("iroha_data_model.isi.SequenceBox"), get_class("iroha_data_model.isi.FailBox"), get_class("iroha_data_model.isi.SetKeyValueBox"), get_class("iroha_data_model.isi.RemoveKeyValueBox"), get_class("iroha_data_model.isi.GrantBox"), get_class("iroha_data_model.isi.RevokeBox"), get_class("iroha_data_model.isi.ExecuteTriggerBox")])

MintBox = make_struct("MintBox", [("object", "iroha_data_model.expression.EvaluatesTo"), ("destination_id", "iroha_data_model.expression.EvaluatesTo")])

Pair = make_struct("Pair", [("left_instruction", "iroha_data_model.isi.Instruction"), ("right_instruction", "iroha_data_model.isi.Instruction")])

RegisterBox = make_struct("RegisterBox", [("object", "iroha_data_model.expression.EvaluatesTo")])

RemoveKeyValueBox = make_struct("RemoveKeyValueBox", [("object_id", "iroha_data_model.expression.EvaluatesTo"), ("key", "iroha_data_model.expression.EvaluatesTo")])

RevokeBox = make_struct("RevokeBox", [("object", "iroha_data_model.expression.EvaluatesTo"), ("destination_id", "iroha_data_model.expression.EvaluatesTo")])

SequenceBox = make_struct("SequenceBox", [("instructions", list)])

SetKeyValueBox = make_struct("SetKeyValueBox", [("object_id", "iroha_data_model.expression.EvaluatesTo"), ("key", "iroha_data_model.expression.EvaluatesTo"), ("value", "iroha_data_model.expression.EvaluatesTo")])

TransferBox = make_struct("TransferBox", [("source_id", "iroha_data_model.expression.EvaluatesTo"), ("object", "iroha_data_model.expression.EvaluatesTo"), ("destination_id", "iroha_data_model.expression.EvaluatesTo")])

UnregisterBox = make_struct("UnregisterBox", [("object_id", "iroha_data_model.expression.EvaluatesTo")])

SelfResolvingTypeVar.resolve_all()
