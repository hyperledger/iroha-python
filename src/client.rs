use paste::paste;

use pyo3::{
    exceptions::{PyRuntimeError, PyValueError},
    prelude::*,
};

use iroha_client::client::Client as IrohaClient;
use iroha_config::client::*;
use std::num::NonZeroU64;
use std::str::FromStr;

use crate::data_model::asset::{PyAsset, PyAssetDefinition, PyAssetDefinitionId, PyAssetId};
use crate::data_model::crypto::*;
use crate::data_model::PyMirror;
use crate::{data_model::account::PyAccountId, isi::PyInstruction};
use iroha_data_model::account::AccountId;
use iroha_data_model::prelude::DomainId;

#[allow(unsafe_code)]
const DEFAULT_TRANSACTION_TIME_TO_LIVE_MS: NonZeroU64 =
    unsafe { NonZeroU64::new_unchecked(100_000) };
const DEFAULT_TRANSACTION_STATUS_TIMEOUT_MS: u64 = 15_000;
const DEFAULT_ADD_TRANSACTION_NONCE: bool = false;

#[pyclass]
pub struct Client {
    client: IrohaClient,
}

#[pymethods]
impl Client {
    #[staticmethod]
    fn create(
        key_pair: &PyKeyPair,
        account_id: &str,
        web_login: &str,
        password: &str,
        api_url: &str,
    ) -> PyResult<Self> {
        let config = Configuration {
            public_key: key_pair.0.public_key().clone(),
            private_key: key_pair.0.private_key().clone(),
            account_id: AccountId::from_str(account_id)
                .map_err(|e| PyValueError::new_err(e.to_string()))?,
            basic_auth: Some(BasicAuth {
                web_login: WebLogin::from_str(web_login)
                    .map_err(|e| PyValueError::new_err(e.to_string()))?,
                password: iroha_primitives::small::SmallStr::from_str(password),
            }),
            torii_api_url: url::Url::parse(api_url)
                .map_err(|e| PyValueError::new_err(e.to_string()))?,
            transaction_time_to_live_ms: Some(DEFAULT_TRANSACTION_TIME_TO_LIVE_MS),
            transaction_status_timeout_ms: DEFAULT_TRANSACTION_STATUS_TIMEOUT_MS,
            // deprecated, does nothing.
            transaction_limits: iroha_data_model::transaction::TransactionLimits::new(0, 0),
            add_transaction_nonce: DEFAULT_ADD_TRANSACTION_NONCE,
        };
        let client = IrohaClient::new(&config).map_err(|e| PyValueError::new_err(e.to_string()))?;
        Ok(Self { client })
    }

    fn submit_executable(&self, py: Python<'_>, isi: PyObject) -> PyResult<String> {
        let isi = if let Ok(isi) = isi.extract::<PyInstruction>(py) {
            vec![isi.0]
        } else if let Ok(isi) = isi.extract::<Vec<PyInstruction>>(py) {
            isi.into_iter().map(|isi| isi.0).collect()
        } else {
            return Err(PyValueError::new_err(""));
        };
        self.client
            .submit_all(isi)
            .map(|hash| hash.to_string())
            .map_err(|e| PyRuntimeError::new_err(format!("Error submitting instruction: {}", e)))
    }

    fn query_all_domains(&self) -> PyResult<Vec<String>> {
        let query = iroha_data_model::query::prelude::FindAllDomains {};

        let val = self
            .client
            .request(query)
            .map_err(|e| PyRuntimeError::new_err(format!("{e:?}")))?;

        let mut items = Vec::new();
        for item in val {
            items.push(
                item.map(|d| d.id.to_string())
                    .map_err(|e| PyRuntimeError::new_err(format!("{e:?}")))?,
            );
        }
        Ok(items)
    }

    fn query_all_accounts_in_domain(&self, domain_id: &str) -> PyResult<Vec<String>> {
        let query = iroha_data_model::query::prelude::FindAccountsByDomainId {
            domain_id: DomainId::from_str(domain_id)
                .map_err(|e| PyValueError::new_err(e.to_string()))?
                .into(),
        };

        let val = self
            .client
            .request(query)
            .map_err(|e| PyRuntimeError::new_err(format!("{e:?}")))?;

        let mut items = Vec::new();
        for item in val {
            items.push(
                item.map(|d| d.id.to_string())
                    .map_err(|e| PyRuntimeError::new_err(format!("{e:?}")))?,
            );
        }
        Ok(items)
    }

    fn query_all_accounts(&self) -> PyResult<Vec<String>> {
        let query = iroha_data_model::query::prelude::FindAllAccounts;

        let val = self
            .client
            .request(query)
            .map_err(|e| PyRuntimeError::new_err(format!("{e:?}")))?;

        let mut items = Vec::new();
        for item in val {
            items.push(
                item.map(|d| d.id.to_string())
                    .map_err(|e| PyRuntimeError::new_err(format!("{e:?}")))?,
            );
        }
        Ok(items)
    }

    fn query_all_assets_owned_by_account(&self, account_id: &str) -> PyResult<Vec<String>> {
        let query = iroha_data_model::query::prelude::FindAssetsByAccountId {
            account_id: AccountId::from_str(account_id)
                .map_err(|e| PyValueError::new_err(e.to_string()))?
                .into(),
        };

        let val = self
            .client
            .request(query)
            .map_err(|e| PyRuntimeError::new_err(format!("{e:?}")))?;

        let mut items = Vec::new();
        for item in val {
            items.push(
                item.map(|d| d.id.to_string())
                    .map_err(|e| PyRuntimeError::new_err(format!("{e:?}")))?,
            );
        }
        Ok(items)
    }

    fn query_all_assets(&self) -> PyResult<Vec<String>> {
        let query = iroha_data_model::query::prelude::FindAllAssets;

        let val = self
            .client
            .request(query)
            .map_err(|e| PyRuntimeError::new_err(format!("{e:?}")))?;

        let mut items = Vec::new();
        for item in val {
            items.push(
                item.map(|d| d.id.to_string())
                    .map_err(|e| PyRuntimeError::new_err(format!("{e:?}")))?,
            );
        }
        Ok(items)
    }

    fn query_all_asset_definitions(&self) -> PyResult<Vec<String>> {
        let query = iroha_data_model::query::prelude::FindAllAssetsDefinitions;

        let val = self
            .client
            .request(query)
            .map_err(|e| PyRuntimeError::new_err(format!("{e:?}")))?;

        let mut items = Vec::new();
        for item in val {
            items.push(
                item.map(|d| d.id.to_string())
                    .map_err(|e| PyRuntimeError::new_err(format!("{e:?}")))?,
            );
        }
        Ok(items)
    }
}

macro_rules! register_query {
    ($query_name:ty; $ret:ty) => {
        register_query!($query_name; $ret;);
    };
    ($query_name:ty; $ret:ty; $($param_name:ident: $param_typ:ty),*) => {
        paste! {
            #[pymethods]
            impl Client {
                fn [<$query_name:snake>](
                    &self,
                    $($param_name: $param_typ),*
                ) -> PyResult<$ret> {
                    #[allow(unused_imports)]
                    use std::ops::Deref as _;

                    let query = iroha_data_model::query::prelude::$query_name {
                        $(
                            $param_name: $param_name.deref().clone().into()
                        ),*
                    };
                    let val = self.client.request(query)
                        .map_err(|e| PyRuntimeError::new_err(format!("{e:?}")))?;
                    val.mirror()
                }
            }
        }
    };
}

register_query!(FindAllAssets; Vec<PyAsset>);
register_query!(FindAllAssetsDefinitions; Vec<PyAssetDefinition>);
register_query!(FindAssetById; PyAsset; id: PyAssetId);
register_query!(FindAssetDefinitionById; PyAssetDefinition; id: PyAssetDefinitionId);
register_query!(FindAssetsByAccountId; Vec<PyAsset>; account_id: PyAccountId);
register_query!(FindAssetsByAssetDefinitionId; Vec<PyAsset>; asset_definition_id: PyAssetDefinitionId);

pub fn register_items(_py: Python<'_>, module: &PyModule) -> PyResult<()> {
    module.add_class::<Client>()?;
    Ok(())
}
