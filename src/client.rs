use paste::paste;

use pyo3::{
    exceptions::{PyRuntimeError, PyValueError},
    prelude::*,
};

use iroha_client::client::Client as IrohaClient;

use crate::data_model::asset::{PyAsset, PyAssetDefinition, PyAssetDefinitionId, PyAssetId};
use crate::data_model::PyMirror;
use crate::{data_model::account::PyAccountId, isi::PyInstruction};

#[pyclass]
pub struct Client {
    client: IrohaClient,
}

#[pymethods]
impl Client {
    #[new]
    fn new(config: &str) -> PyResult<Self> {
        //let config = iroha_config::client::Configuration;
        //let client = IrohaClient::new();
        let config: iroha_config::client::Configuration =
            serde_json::from_str(config).map_err(|e| PyValueError::new_err(e.to_string()))?;
        let client = IrohaClient::new(&config).map_err(|e| PyValueError::new_err(e.to_string()))?;
        Ok(Self { client })
    }

    fn submit(&self, py: Python<'_>, isi: PyObject) -> PyResult<String> {
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
