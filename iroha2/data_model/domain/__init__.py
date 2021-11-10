from ...sys.iroha_data_model.domain import Domain as _Domain


class Domain(_Domain):
    def __init__(self, name):
        super().__init__(self,
                         name=name,
                         accounts={},
                         asset_definitions={},
                         metadata={})
