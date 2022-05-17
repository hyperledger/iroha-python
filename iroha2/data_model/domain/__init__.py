from ...sys.iroha_data_model.domain import Domain as _Domain
from ...sys.iroha_data_model.domain import NewDomain as _NewDomain
from ...sys.iroha_data_model.domain import Id as _DomainId
from ...sys.iroha_data_model.domain import IpfsPath
from ...sys.iroha_data_model import Name

class NewDomain(_NewDomain):
    def __init__(self, id, logo="QmQqzMTavQgT4f4T5v6PWBp7XNKtoPmC9jvn12WPT3gkSE"):
        id = _DomainId(name=id)
        super().__init__(self,
                         id=id,
                         logo=logo,
                         metadata={})

class Domain(_Domain):
    def __init__(self, id, logo="QmQqzMTavQgT4f4T5v6PWBp7XNKtoPmC9jvn12WPT3gkSE"):
        id = _DomainId(name=id)
        super().__init__(self,
                         id=id,
                         logo=logo,
                         accounts={},
                         asset_definitions={},
                         metadata={})
