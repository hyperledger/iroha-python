from ...rust import Enum, make_struct, make_tuple, Dict
Add = make_struct("Add", [("left", "iroha_data_model.expression.EvaluatesTo"), ("right", "iroha_data_model.expression.EvaluatesTo")])

And = make_struct("And", [("left", "iroha_data_model.expression.EvaluatesTo"), ("right", "iroha_data_model.expression.EvaluatesTo")])

Contains = make_struct("Contains", [("collection", "iroha_data_model.expression.EvaluatesTo"), ("element", "iroha_data_model.expression.EvaluatesTo")])

ContainsAll = make_struct("ContainsAll", [("collection", "iroha_data_model.expression.EvaluatesTo"), ("elements", "iroha_data_model.expression.EvaluatesTo")])

ContainsAny = make_struct("ContainsAny", [("collection", "iroha_data_model.expression.EvaluatesTo"), ("elements", "iroha_data_model.expression.EvaluatesTo")])

ContextValue = make_struct("ContextValue", [("value_name", str)])

Divide = make_struct("Divide", [("left", "iroha_data_model.expression.EvaluatesTo"), ("right", "iroha_data_model.expression.EvaluatesTo")])

Equal = make_struct("Equal", [("left", "iroha_data_model.expression.EvaluatesTo"), ("right", "iroha_data_model.expression.EvaluatesTo")])

EvaluatesTo = make_struct("EvaluatesTo", [("expression", "iroha_data_model.expression.Expression")])

Expression = Enum[("Add", "iroha_data_model.expression.Add"), ("Subtract", "iroha_data_model.expression.Subtract"), ("Multiply", "iroha_data_model.expression.Multiply"), ("Divide", "iroha_data_model.expression.Divide"), ("Mod", "iroha_data_model.expression.Mod"), ("RaiseTo", "iroha_data_model.expression.RaiseTo"), ("Greater", "iroha_data_model.expression.Greater"), ("Less", "iroha_data_model.expression.Less"), ("Equal", "iroha_data_model.expression.Equal"), ("Not", "iroha_data_model.expression.Not"), ("And", "iroha_data_model.expression.And"), ("Or", "iroha_data_model.expression.Or"), ("If", "iroha_data_model.expression.If"), ("Raw", "iroha_data_model.Value"), ("Query", "iroha_data_model.query.QueryBox"), ("Contains", "iroha_data_model.expression.Contains"), ("ContainsAll", "iroha_data_model.expression.ContainsAll"), ("ContainsAny", "iroha_data_model.expression.ContainsAny"), ("Where", "iroha_data_model.expression.Where"), ("ContextValue", "iroha_data_model.expression.ContextValue")] 
Greater = make_struct("Greater", [("left", "iroha_data_model.expression.EvaluatesTo"), ("right", "iroha_data_model.expression.EvaluatesTo")])

If = make_struct("If", [("condition", "iroha_data_model.expression.EvaluatesTo"), ("then_expression", "iroha_data_model.expression.EvaluatesTo"), ("else_expression", "iroha_data_model.expression.EvaluatesTo")])

Less = make_struct("Less", [("left", "iroha_data_model.expression.EvaluatesTo"), ("right", "iroha_data_model.expression.EvaluatesTo")])

Mod = make_struct("Mod", [("left", "iroha_data_model.expression.EvaluatesTo"), ("right", "iroha_data_model.expression.EvaluatesTo")])

Multiply = make_struct("Multiply", [("left", "iroha_data_model.expression.EvaluatesTo"), ("right", "iroha_data_model.expression.EvaluatesTo")])

Not = make_struct("Not", [("expression", "iroha_data_model.expression.EvaluatesTo")])

Or = make_struct("Or", [("left", "iroha_data_model.expression.EvaluatesTo"), ("right", "iroha_data_model.expression.EvaluatesTo")])

RaiseTo = make_struct("RaiseTo", [("left", "iroha_data_model.expression.EvaluatesTo"), ("right", "iroha_data_model.expression.EvaluatesTo")])

Subtract = make_struct("Subtract", [("left", "iroha_data_model.expression.EvaluatesTo"), ("right", "iroha_data_model.expression.EvaluatesTo")])

Where = make_struct("Where", [("expression", "iroha_data_model.expression.EvaluatesTo"), ("values", Dict)])

