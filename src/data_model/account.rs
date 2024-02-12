use iroha_data_model::account::{prelude::*, NewAccount};

use pyo3::{
    exceptions::PyValueError,
    prelude::*,
    types::{PyDict, PyList},
};
use std::collections::{BTreeMap, BTreeSet};

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
    fn new(name: &str, domain: &str) -> PyResult<Self> {
        let name = name
            .parse()
            .map_err(|e| PyValueError::new_err(format!("Invalid Account name: {e}")))?;
        let domain = domain
            .parse()
            .map_err(|e| PyValueError::new_err(format!("Invalid Domain name: {e}")))?;
        Ok(Self(AccountId::new(name, domain)))
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

    #[getter]
    fn get_domain(&self) -> &str {
        self.0.domain_id().name().as_ref()
    }

    #[setter]
    fn set_domain(&mut self, name: &str) -> PyResult<()> {
        self.0.domain_id.name = name
            .parse()
            .map_err(|e| PyValueError::new_err(format!("Invalid Domain name: {e}")))?;
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
    fn get_assets(&self) -> BTreeMap<PyAssetId, PyAsset> {
        self.assets
            .iter()
            .map(|(id, asset)| (id.clone().into(), asset.clone().into()))
            .collect()
    }

    #[getter]
    fn get_signatories(&self, py: Python<'_>) -> Py<PyList> {
        let signatories = self
            .0
            .signatories
            .iter()
            .map(|signatory| PyPublicKey(signatory.clone()).into_py(py))
            .collect::<Vec<_>>();
        PyList::new(py, signatories).into()
    }

    #[getter]
    fn get_metadata(&self, py: Python<'_>) -> PyResult<Py<PyDict>> {
        MetadataWrapper(self.0.metadata.clone()).into_py(py)
    }
}

mirror_struct!(NewAccount);

#[pymethods]
impl PyNewAccount {
    #[new]
    fn new(py: Python<'_>, id: PyObject, signatories: PyObject) -> PyResult<Self> {
        let id = if let Ok(id) = id.extract::<PyAccountId>(py) {
            id.0
        } else if let Ok(id_str) = id.extract::<&str>(py) {
            id_str
                .parse()
                .map_err(|e| PyValueError::new_err(format!("Invalid account id: {e}")))?
        } else {
            return Err(PyValueError::new_err(
                "id should be either AccountId or str",
            ));
        };

        let signatories = if let Ok(single) = signatories.extract::<PyPublicKey>(py) {
            vec![single.0]
        } else if let Ok(multiple) = signatories.extract::<Vec<PyPublicKey>>(py) {
            multiple.into_iter().map(|key| key.0).collect::<Vec<_>>()
        } else {
            return Err(PyValueError::new_err(
                "signatories should be either a list of public keys or a single public key",
            ));
        };

        Ok(Self(Account::new(id, signatories)))
    }

    #[getter]
    fn get_id(&self) -> PyAccountId {
        PyAccountId(self.0.id.clone())
    }

    #[setter]
    fn set_id(&mut self, id: PyAccountId) {
        self.0.id = id.clone().into()
    }

    #[getter]
    fn get_signatories(&self, py: Python<'_>) -> Py<PyList> {
        let signatories = self
            .0
            .signatories
            .iter()
            .map(|signatory| PyPublicKey(signatory.clone()).into_py(py))
            .collect::<Vec<_>>();
        PyList::new(py, signatories).into()
    }

    #[setter]
    fn set_signatories(&mut self, signatories: Vec<PyPublicKey>) {
        let signatories = signatories
            .into_iter()
            .map(Into::into)
            .collect::<BTreeSet<_>>();
        self.0.signatories = signatories
    }

    #[getter]
    fn get_metadata(&self, py: Python<'_>) -> PyResult<Py<PyDict>> {
        MetadataWrapper(self.0.metadata.clone()).into_py(py)
    }
}

pub fn register_items(_py: Python<'_>, module: &PyModule) -> PyResult<()> {
    module.add_class::<PyAccountId>()?;
    module.add_class::<PyAccount>()?;
    module.add_class::<PyNewAccount>()?;
    Ok(())
}
