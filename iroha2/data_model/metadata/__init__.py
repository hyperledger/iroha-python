from ...sys.iroha_data_model.metadata import *
from ...sys.iroha_data_model.metadata import (
    Metadata as _Metadata, )
from .. import wrapper


@wrapper(_Metadata, flattened=True)
class Metadata(_Metadata):
    pass
