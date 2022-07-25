from ...rust import Enum, make_struct, make_tuple, Dict
BurnBox = make_struct("BurnBox", [("object", "iroha_data_model.expression.EvaluatesTo"), ("destination_id", "iroha_data_model.expression.EvaluatesTo")])

ExecuteTriggerBox = make_struct("ExecuteTriggerBox", [("trigger_id", "iroha_data_model.trigger.Id")])

FailBox = make_struct("FailBox", [("message", str)])

GrantBox = make_struct("GrantBox", [("object", "iroha_data_model.expression.EvaluatesTo"), ("destination_id", "iroha_data_model.expression.EvaluatesTo")])

If = make_struct("If", [("condition", "iroha_data_model.expression.EvaluatesTo"), ("then", "iroha_data_model.isi.Instruction"), ("otherwise", "iroha_data_model.isi.Instruction")])

Instruction = Enum[("Register", "iroha_data_model.isi.RegisterBox"), ("Unregister", "iroha_data_model.isi.UnregisterBox"), ("Mint", "iroha_data_model.isi.MintBox"), ("Burn", "iroha_data_model.isi.BurnBox"), ("Transfer", "iroha_data_model.isi.TransferBox"), ("If", "iroha_data_model.isi.If"), ("Pair", "iroha_data_model.isi.Pair"), ("Sequence", "iroha_data_model.isi.SequenceBox"), ("Fail", "iroha_data_model.isi.FailBox"), ("SetKeyValue", "iroha_data_model.isi.SetKeyValueBox"), ("RemoveKeyValue", "iroha_data_model.isi.RemoveKeyValueBox"), ("Grant", "iroha_data_model.isi.GrantBox"), ("Revoke", "iroha_data_model.isi.RevokeBox"), ("ExecuteTrigger", "iroha_data_model.isi.ExecuteTriggerBox")] 
MintBox = make_struct("MintBox", [("object", "iroha_data_model.expression.EvaluatesTo"), ("destination_id", "iroha_data_model.expression.EvaluatesTo")])

Pair = make_struct("Pair", [("left_instruction", "iroha_data_model.isi.Instruction"), ("right_instruction", "iroha_data_model.isi.Instruction")])

RegisterBox = make_struct("RegisterBox", [("object", "iroha_data_model.expression.EvaluatesTo")])

RemoveKeyValueBox = make_struct("RemoveKeyValueBox", [("object_id", "iroha_data_model.expression.EvaluatesTo"), ("key", "iroha_data_model.expression.EvaluatesTo")])

RevokeBox = make_struct("RevokeBox", [("object", "iroha_data_model.expression.EvaluatesTo"), ("destination_id", "iroha_data_model.expression.EvaluatesTo")])

SequenceBox = make_struct("SequenceBox", [("instructions", list)])

SetKeyValueBox = make_struct("SetKeyValueBox", [("object_id", "iroha_data_model.expression.EvaluatesTo"), ("key", "iroha_data_model.expression.EvaluatesTo"), ("value", "iroha_data_model.expression.EvaluatesTo")])

TransferBox = make_struct("TransferBox", [("source_id", "iroha_data_model.expression.EvaluatesTo"), ("object", "iroha_data_model.expression.EvaluatesTo"), ("destination_id", "iroha_data_model.expression.EvaluatesTo")])

UnregisterBox = make_struct("UnregisterBox", [("object_id", "iroha_data_model.expression.EvaluatesTo")])

