from typing import Union, Optional

from ...sys.iroha_data_model.account import (
    Account as _Account,
    NewAccount as _NewAccount,
    Id,
)
from ..domain import Id as DomainId
from ..isi import Registrable
from ...crypto import PublicKey
from .. import wrapper


@wrapper(_Account)
class Account(_Account, Registrable):

    def __init__(self,
                 id: Union[Id, str],
                 assets: Optional[dict] = None,
                 signatories: Optional[list[PublicKey]] = None,
                 metadata: Optional[dict] = None,
                 roles: Optional[list] = None):

        if assets is None:
            assets = []

        if metadata is None:
            metadata = {}

        if roles is None:
            roles = []

        if signatories is None:
            signatories = []

        if isinstance(id, str):
            acct_id, domain_id = id.split("@")
            id = Id(name=acct_id, domain_id=DomainId(domain_id))

        return super().__init__(
            id=id,
            metadata=metadata,
            assets=assets,
            signatories=signatories,
            signature_check_condition=True,  # TODO:
            roles=roles)

    def registrable(self):
        return _NewAccount(id=self.id,
                           signatories=self.signatories,
                           metadata=self.metadata)
