from ...rust import Enum, Struct, Tuple, Dict

Add = Struct[("left", "iroha_data_model.expression.EvaluatesTo"),
             ("right", "iroha_data_model.expression.EvaluatesTo")]

And = Struct[("left", "iroha_data_model.expression.EvaluatesTo"),
             ("right", "iroha_data_model.expression.EvaluatesTo")]

Contains = Struct[("collection", "iroha_data_model.expression.EvaluatesTo"),
                  ("element", "iroha_data_model.expression.EvaluatesTo")]

ContainsAll = Struct[("collection", "iroha_data_model.expression.EvaluatesTo"),
                     ("elements", "iroha_data_model.expression.EvaluatesTo")]

ContainsAny = Struct[("collection", "iroha_data_model.expression.EvaluatesTo"),
                     ("elements", "iroha_data_model.expression.EvaluatesTo")]

ContextValue = Struct[("value_name", str)]

Divide = Struct[("left", "iroha_data_model.expression.EvaluatesTo"),
                ("right", "iroha_data_model.expression.EvaluatesTo")]

Equal = Struct[("left", "iroha_data_model.expression.EvaluatesTo"),
               ("right", "iroha_data_model.expression.EvaluatesTo")]

EvaluatesTo = Struct[("expression", "iroha_data_model.expression.Expression")]

Expression = Enum[("Add", "iroha_data_model.expression.Add"),
                  ("Subtract", "iroha_data_model.expression.Subtract"),
                  ("Multiply", "iroha_data_model.expression.Multiply"),
                  ("Divide", "iroha_data_model.expression.Divide"),
                  ("Mod", "iroha_data_model.expression.Mod"),
                  ("RaiseTo", "iroha_data_model.expression.RaiseTo"),
                  ("Greater", "iroha_data_model.expression.Greater"),
                  ("Less", "iroha_data_model.expression.Less"),
                  ("Equal", "iroha_data_model.expression.Equal"),
                  ("Not", "iroha_data_model.expression.Not"),
                  ("And", "iroha_data_model.expression.And"),
                  ("Or", "iroha_data_model.expression.Or"),
                  ("If", "iroha_data_model.expression.If"),
                  ("Raw", "iroha_data_model.Value"),
                  ("Query", "iroha_data_model.query.QueryBox"),
                  ("Contains", "iroha_data_model.expression.Contains"),
                  ("ContainsAll", "iroha_data_model.expression.ContainsAll"),
                  ("ContainsAny", "iroha_data_model.expression.ContainsAny"),
                  ("Where", "iroha_data_model.expression.Where"),
                  ("ContextValue", "iroha_data_model.expression.ContextValue")]
Greater = Struct[("left", "iroha_data_model.expression.EvaluatesTo"),
                 ("right", "iroha_data_model.expression.EvaluatesTo")]

If = Struct[("condition", "iroha_data_model.expression.EvaluatesTo"),
            ("then_expression", "iroha_data_model.expression.EvaluatesTo"),
            ("else_expression", "iroha_data_model.expression.EvaluatesTo")]

Less = Struct[("left", "iroha_data_model.expression.EvaluatesTo"),
              ("right", "iroha_data_model.expression.EvaluatesTo")]

Mod = Struct[("left", "iroha_data_model.expression.EvaluatesTo"),
             ("right", "iroha_data_model.expression.EvaluatesTo")]

Multiply = Struct[("left", "iroha_data_model.expression.EvaluatesTo"),
                  ("right", "iroha_data_model.expression.EvaluatesTo")]

Not = Struct[("expression", "iroha_data_model.expression.EvaluatesTo")]

Or = Struct[("left", "iroha_data_model.expression.EvaluatesTo"),
            ("right", "iroha_data_model.expression.EvaluatesTo")]

RaiseTo = Struct[("left", "iroha_data_model.expression.EvaluatesTo"),
                 ("right", "iroha_data_model.expression.EvaluatesTo")]

Subtract = Struct[("left", "iroha_data_model.expression.EvaluatesTo"),
                  ("right", "iroha_data_model.expression.EvaluatesTo")]

Where = Struct[("expression", "iroha_data_model.expression.EvaluatesTo"),
               ("values", Dict)]
