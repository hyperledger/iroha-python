use iroha_data_model::domain::prelude::*;
use iroha_data_model::domain::NewDomain;
use pyo3::types::PyDict;
use pyo3::{exceptions::PyValueError, prelude::*};

use crate::data_model::account::*;
use crate::data_model::asset::*;
use crate::mirror_struct;

use std::collections::BTreeMap;

use super::MetadataWrapper;

mirror_struct! {
    /// Domain id
    DomainId
}

#[pymethods]
impl PyDomainId {
    #[new]
    fn new(name: &str) -> PyResult<Self> {
        let name = name
            .parse()
            .map_err(|e| PyValueError::new_err(format!("Invalid Domain name: {e}")))?;
        Ok(Self(DomainId::new(name)))
    }

    #[getter]
    fn get_name(&self) -> &str {
        self.0.name().as_ref()
    }

    #[setter]
    fn set_name(&mut self, name: &str) -> PyResult<()> {
        self.0.name = name
            .parse()
            .map_err(|e| PyValueError::new_err(format!("Invalid AssedDefinitionId name: {e}")))?;
        Ok(())
    }
}

mirror_struct! {
    /// Domain id
    Domain
}

#[pymethods]
impl PyDomain {
    #[getter]
    fn get_id(&self) -> PyDomainId {
        PyDomainId(self.0.id.clone())
    }

    #[getter]
    fn get_account(&self) -> BTreeMap<PyAccountId, PyAccount> {
        self.accounts
            .iter()
            .map(|(id, account)| (id.clone().into(), account.clone().into()))
            .collect()
    }

    #[getter]
    fn get_asset_definitions(&self) -> BTreeMap<PyAssetDefinitionId, PyAssetDefinition> {
        self.asset_definitions
            .iter()
            .map(|(id, asset)| (id.clone().into(), asset.clone().into()))
            .collect()
    }

    #[getter]
    fn get_logo(&self) -> Option<&str> {
        self.0.logo.as_ref().map(|logo| logo.as_ref())
    }

    #[getter]
    fn get_owned_by(&self) -> PyAccountId {
        self.0.owned_by.clone().into()
    }

    #[getter]
    fn get_metadata(&self, py: Python<'_>) -> PyResult<Py<PyDict>> {
        MetadataWrapper(self.0.metadata.clone()).into_py(py)
    }
}

mirror_struct!(NewDomain);

#[pymethods]
impl PyNewDomain {
    #[new]
    fn new(py: Python<'_>, id: PyObject) -> PyResult<Self> {
        let id = if let Ok(id) = id.extract::<PyDomainId>(py) {
            id.0
        } else if let Ok(id_str) = id.extract::<&str>(py) {
            id_str
                .parse()
                .map_err(|e| PyValueError::new_err(format!("Invalid domain id: {e}")))?
        } else {
            return Err(PyValueError::new_err("id should be either DomainId or str"));
        };

        Ok(Self(Domain::new(id)))
    }

    #[getter]
    fn get_id(&self) -> PyDomainId {
        PyDomainId(self.0.id.clone())
    }

    #[setter]
    fn set_id(&mut self, id: PyDomainId) {
        self.0.id = id.clone().into()
    }

    #[getter]
    fn get_logo(&self) -> Option<&str> {
        self.0.logo.as_ref().map(|logo| logo.as_ref())
    }

    #[setter]
    fn set_logo(&mut self, new: Option<String>) -> PyResult<()> {
        if let Some(path) = new {
            self.0.logo = Some(
                path.parse()
                    .map_err(|e| PyValueError::new_err(format!("Malformed IPFS path: {e}")))?,
            )
        }
        Ok(())
    }

    #[getter]
    fn get_metadata(&self, py: Python<'_>) -> PyResult<Py<PyDict>> {
        MetadataWrapper(self.0.metadata.clone()).into_py(py)
    }
}

pub fn register_items(_py: Python<'_>, module: &PyModule) -> PyResult<()> {
    module.add_class::<PyDomainId>()?;
    Ok(())
}
