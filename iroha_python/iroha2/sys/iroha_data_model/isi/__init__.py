from ...rust import Enum, Struct, Tuple, Dict

BurnBox = Struct[("object", "iroha_data_model.expression.EvaluatesTo"),
                 ("destination_id", "iroha_data_model.expression.EvaluatesTo")]

FailBox = Struct[("message", str)]

GrantBox = Struct[("object", "iroha_data_model.expression.EvaluatesTo"),
                  ("destination_id",
                   "iroha_data_model.expression.EvaluatesTo")]

If = Struct[("condition", "iroha_data_model.expression.EvaluatesTo"),
            ("then", "iroha_data_model.isi.Instruction"),
            ("otherwise", "iroha_data_model.isi.Instruction")]

Instruction = Enum[("Register", "iroha_data_model.isi.RegisterBox"),
                   ("Unregister", "iroha_data_model.isi.UnregisterBox"),
                   ("Mint", "iroha_data_model.isi.MintBox"),
                   ("Burn", "iroha_data_model.isi.BurnBox"),
                   ("Transfer", "iroha_data_model.isi.TransferBox"),
                   ("If",
                    "iroha_data_model.isi.If"), ("Pair",
                                                 "iroha_data_model.isi.Pair"),
                   ("Sequence", "iroha_data_model.isi.SequenceBox"),
                   ("Fail", "iroha_data_model.isi.FailBox"),
                   ("SetKeyValue", "iroha_data_model.isi.SetKeyValueBox"),
                   ("RemoveKeyValue",
                    "iroha_data_model.isi.RemoveKeyValueBox"),
                   ("Grant", "iroha_data_model.isi.GrantBox")]
MintBox = Struct[("object", "iroha_data_model.expression.EvaluatesTo"),
                 ("destination_id", "iroha_data_model.expression.EvaluatesTo")]

Pair = Struct[("left_instruction", "iroha_data_model.isi.Instruction"),
              ("right_instruction", "iroha_data_model.isi.Instruction")]

RegisterBox = Struct[("object", "iroha_data_model.expression.EvaluatesTo")]

RemoveKeyValueBox = Struct[("object_id",
                            "iroha_data_model.expression.EvaluatesTo"),
                           ("key", "iroha_data_model.expression.EvaluatesTo")]

SequenceBox = Struct[("instructions", list)]

SetKeyValueBox = Struct[("object_id",
                         "iroha_data_model.expression.EvaluatesTo"),
                        ("key", "iroha_data_model.expression.EvaluatesTo"),
                        ("value", "iroha_data_model.expression.EvaluatesTo")]

TransferBox = Struct[("source_id", "iroha_data_model.expression.EvaluatesTo"),
                     ("object", "iroha_data_model.expression.EvaluatesTo"),
                     ("destination_id",
                      "iroha_data_model.expression.EvaluatesTo")]

UnregisterBox = Struct[("object_id",
                        "iroha_data_model.expression.EvaluatesTo")]
