
from ...rust import make_enum, make_struct, make_tuple, get_class, SelfResolvingTypeVar, Dict
import typing
            
Add = make_struct("Add", [("left", "iroha_data_model.expression.EvaluatesTo"), ("right", "iroha_data_model.expression.EvaluatesTo")])

And = make_struct("And", [("left", "iroha_data_model.expression.EvaluatesTo"), ("right", "iroha_data_model.expression.EvaluatesTo")])

Contains = make_struct("Contains", [("collection", "iroha_data_model.expression.EvaluatesTo"), ("element", "iroha_data_model.expression.EvaluatesTo")])

ContainsAll = make_struct("ContainsAll", [("collection", "iroha_data_model.expression.EvaluatesTo"), ("elements", "iroha_data_model.expression.EvaluatesTo")])

ContainsAny = make_struct("ContainsAny", [("collection", "iroha_data_model.expression.EvaluatesTo"), ("elements", "iroha_data_model.expression.EvaluatesTo")])

ContextValue = make_struct("ContextValue", [("value_name", "iroha_data_model.name.Name")])

Divide = make_struct("Divide", [("left", "iroha_data_model.expression.EvaluatesTo"), ("right", "iroha_data_model.expression.EvaluatesTo")])

Equal = make_struct("Equal", [("left", "iroha_data_model.expression.EvaluatesTo"), ("right", "iroha_data_model.expression.EvaluatesTo")])

EvaluatesTo = make_struct("EvaluatesTo", [("expression", "iroha_data_model.expression.Expression")])

Expression = make_enum("Expression", [("Add", get_class("iroha_data_model.expression.Add")), ("Subtract", get_class("iroha_data_model.expression.Subtract")), ("Multiply", get_class("iroha_data_model.expression.Multiply")), ("Divide", get_class("iroha_data_model.expression.Divide")), ("Mod", get_class("iroha_data_model.expression.Mod")), ("RaiseTo", get_class("iroha_data_model.expression.RaiseTo")), ("Greater", get_class("iroha_data_model.expression.Greater")), ("Less", get_class("iroha_data_model.expression.Less")), ("Equal", get_class("iroha_data_model.expression.Equal")), ("Not", get_class("iroha_data_model.expression.Not")), ("And", get_class("iroha_data_model.expression.And")), ("Or", get_class("iroha_data_model.expression.Or")), ("If", get_class("iroha_data_model.expression.If")), ("Raw", get_class("iroha_data_model.Value")), ("Query", get_class("iroha_data_model.query.QueryBox")), ("Contains", get_class("iroha_data_model.expression.Contains")), ("ContainsAll", get_class("iroha_data_model.expression.ContainsAll")), ("ContainsAny", get_class("iroha_data_model.expression.ContainsAny")), ("Where", get_class("iroha_data_model.expression.Where")), ("ContextValue", get_class("iroha_data_model.expression.ContextValue"))], typing.Union[get_class("iroha_data_model.expression.Add"), get_class("iroha_data_model.expression.Subtract"), get_class("iroha_data_model.expression.Multiply"), get_class("iroha_data_model.expression.Divide"), get_class("iroha_data_model.expression.Mod"), get_class("iroha_data_model.expression.RaiseTo"), get_class("iroha_data_model.expression.Greater"), get_class("iroha_data_model.expression.Less"), get_class("iroha_data_model.expression.Equal"), get_class("iroha_data_model.expression.Not"), get_class("iroha_data_model.expression.And"), get_class("iroha_data_model.expression.Or"), get_class("iroha_data_model.expression.If"), get_class("iroha_data_model.Value"), get_class("iroha_data_model.query.QueryBox"), get_class("iroha_data_model.expression.Contains"), get_class("iroha_data_model.expression.ContainsAll"), get_class("iroha_data_model.expression.ContainsAny"), get_class("iroha_data_model.expression.Where"), get_class("iroha_data_model.expression.ContextValue")])

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

SelfResolvingTypeVar.resolve_all()
