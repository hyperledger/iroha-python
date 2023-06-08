from ...sys.iroha_data_model.expression import *
from ...sys.iroha_data_model.expression import (Expression as _Expression,
                                                EvaluatesTo as _EvaluatesTo)

from .. import wrapper, patch


@wrapper(_Expression)
class Expression(_Expression):

    @patch(_Expression, "to_rust")
    def to_rust(self):
        return self._value.to_rust()


@wrapper(_EvaluatesTo, flattened=True)
class EvaluatesTo(_EvaluatesTo):
    pass
