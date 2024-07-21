use iroha_data_model::account::{prelude::*, Account, NewAccount};

use pyo3::{
    exceptions::PyValueError,
    prelude::*,
    types::{PyDict, PyList},
};
use std::collections::BTreeMap;

use crate::mirror_struct;

use super::{
    asset::{PyAsset, PyAssetId},
    crypto::PyPublicKey,
    MetadataWrapper,
};

mirror_struct! {
    #[derive(PartialEq, Eq, PartialOrd, Ord, Hash)]
    AccountId
}

#[pymethods]
impl PyAccountId {
    #[new]
    fn new(domain: &str, signatory: PyPublicKey) -> PyResult<Self> {
        let domain = domain
            .parse()
            .map_err(|e| PyValueError::new_err(format!("Invalid Domain name: {e}")))?;
        Ok(Self(AccountId::new(domain, signatory.into())))
    }

    #[getter]
    fn get_domain(&self) -> &str {
        self.0.domain().name().as_ref()
    }

    #[setter]
    fn set_domain(&mut self, name: &str) -> PyResult<()> {
        self.0.domain.name = name
            .parse()
            .map_err(|e| PyValueError::new_err(format!("Invalid Domain name: {e}")))?;
        Ok(())
    }

    #[getter]
    fn get_signatory(&self) -> PyPublicKey {
        self.0.signatory().clone().into()
    }

    #[setter]
    fn set_signatory(&mut self, signatory: PyPublicKey) -> PyResult<()> {
        self.0.signatory = signatory.into();
        Ok(())
    }
}

mirror_struct!(Account);

#[pymethods]
impl PyAccount {
    #[getter]
    fn get_id(&self) -> PyAccountId {
        PyAccountId(self.0.id.clone())
    }

    #[getter]
    fn get_metadata(&self, py: Python<'_>) -> PyResult<Py<PyDict>> {
        MetadataWrapper(self.0.metadata.clone()).into_py(py)
    }
}

pub fn register_items(_py: Python<'_>, module: &PyModule) -> PyResult<()> {
    module.add_class::<PyAccountId>()?;
    module.add_class::<PyAccount>()?;
    Ok(())
}
