from typing import Union, Optional

from ...sys.iroha_data_model.account import (
    Account as _Account,
    NewAccount as _NewAccount,
    Id,
)
from ..domain import Id as DomainId
from ..isi import Registrable


class Account(_Account, Registrable):
    def __init__(self,
                 id: Union[Id, str],
                 assets: Optional[dict] = None,
                 permission_tokens: Optional[list] = None,
                 metadata: Optional[dict] = None,
                 roles: Optional[list] = None):

        if assets is None:
            assets = []

        if permission_tokens is None:
            permission_tokens = []

        if metadata is None:
            metadata = {}

        if roles is None:
            roles = []

        if isinstance(id, str):
            acct_id, domain_id = id.split("@")
            id = Id(name=acct_id, domain_id=DomainId(domain_id))

        return super().__init__(self, id=id,
                                metadata=metadata,
                                assets=assets,
                                signatories=[],
                                permission_tokens=permission_tokens,
                                signature_check_condition=True,
                                roles=roles)

    def registrable(self):
        return _NewAccount(id=self.id,
                           signatories=self.signatories,
                           metadata=self.metadata)
