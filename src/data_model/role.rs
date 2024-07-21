use pyo3::prelude::*;

use super::PyMirror;
use iroha_data_model::prelude::Permission;
use iroha_data_model::prelude::Role;

#[pyclass(name = "Role")]
#[derive(Clone, derive_more::From, derive_more::Into, derive_more::Deref)]
pub struct PyRole(pub Role);

impl PyMirror for Role {
    type Mirror = PyRole;

    fn mirror(self) -> PyResult<Self::Mirror> {
        Ok(PyRole(self))
    }
}

#[pymethods]
impl PyRole {
    #[getter]
    fn get_role_id(&self) -> String {
        self.0.id.name.to_string()
    }

    #[getter]
    fn get_permissions(&self) -> Vec<PyPermission> {
        self.0
            .permissions
            .iter()
            .map(|x| PyPermission(x.clone()))
            .collect()
    }

    fn __repr__(&self) -> String {
        format!("{:?}", self.0)
    }
}

#[pyclass(name = "Permission")]
#[derive(Clone, derive_more::From, derive_more::Into, derive_more::Deref)]
pub struct PyPermission(pub Permission);

impl PyMirror for Permission {
    type Mirror = PyPermission;

    fn mirror(self) -> PyResult<Self::Mirror> {
        Ok(PyPermission(self))
    }
}

#[pymethods]
impl PyPermission {
    #[getter]
    fn get_name(&self) -> String {
        format!("{:?}", self.0.name)
    }

    #[getter]
    fn get_payload(&self) -> String {
        format!("{:?}", self.0.payload)
    }

    fn __repr__(&self) -> String {
        format!("{:?}", self.0)
    }
}

pub fn register_items(_py: Python<'_>, module: &PyModule) -> PyResult<()> {
    module.add_class::<PyRole>()?;
    Ok(())
}
