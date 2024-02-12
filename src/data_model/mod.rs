use derive_more::{From, Into};

use iroha_client::client::{QueryOutput, ResultSet};
use iroha_data_model::{metadata::Metadata, IdentifiableBox, Value};
use pyo3::{
    exceptions::PyRuntimeError,
    prelude::*,
    types::{PyBool, PyDict, PyList, PyString},
};

use self::account::*;
use self::asset::*;
use self::domain::*;

pub mod account;
pub mod asset;
pub mod crypto;
pub mod domain;
pub mod role;

mod util;

pub trait PyMirror {
    type Mirror;

    fn mirror(self) -> PyResult<Self::Mirror>;
}

impl<T> PyMirror for ResultSet<T>
where
    T: PyMirror,
    T: Clone,
    Vec<T>: QueryOutput,
    <Vec<T> as TryFrom<Value>>::Error: Into<eyre::Report>,
{
    type Mirror = Vec<T::Mirror>;

    fn mirror(self) -> PyResult<Self::Mirror> {
        let mut items = Vec::new();
        for item in self {
            let pyitem = item
                .map_err(|e| PyRuntimeError::new_err(format!("{e}")))?
                .mirror()?;
            items.push(pyitem);
        }
        Ok(items)
    }
}

// Proxy struct to facilitate conversions
#[derive(From)]
struct IdentifiableBoxWrapper(IdentifiableBox);

impl IntoPy<PyResult<PyObject>> for IdentifiableBoxWrapper {
    fn into_py(self, py: Python<'_>) -> PyResult<PyObject> {
        Ok(match self.0 {
            IdentifiableBox::NewDomain(value) => PyNewDomain(value).into_py(py),
            IdentifiableBox::NewAccount(value) => PyNewAccount(value).into_py(py),
            IdentifiableBox::NewAssetDefinition(value) => PyNewAssetDefinition(value).into_py(py),
            IdentifiableBox::AssetDefinition(value) => PyAssetDefinition(value).into_py(py),
            IdentifiableBox::Domain(value) => PyDomain(value).into_py(py),
            IdentifiableBox::Account(value) => PyAccount(value).into_py(py),
            IdentifiableBox::Asset(value) => PyAsset(value).into_py(py),
            _ => unimplemented!(),
        })
    }
}

// Proxy struct to facilitate conversions
#[derive(From, Into)]
struct MetadataWrapper(Metadata);

impl IntoPy<PyResult<Py<PyDict>>> for MetadataWrapper {
    fn into_py(self, py: Python<'_>) -> PyResult<Py<PyDict>> {
        let dict = PyDict::new(py);
        for (name, value) in self.0.iter() {
            dict.set_item(
                PyString::new(py, name.as_ref()),
                Into::<ValueWrapper>::into(value.clone()).into_py(py)?,
            )?;
        }
        Ok(dict.into_py(py))
    }
}

// Proxy struct to facilitate conversions
#[derive(From, Into)]
struct ValueWrapper(Value);

impl IntoPy<PyResult<PyObject>> for ValueWrapper {
    fn into_py(self, py: Python<'_>) -> PyResult<PyObject> {
        fn to_py_ip(py: Python<'_>, ip: String) -> PyResult<PyObject> {
            PyModule::import(py, "ipaddress")?
                .getattr("ip_address")?
                .call1((ip,))
                .map(Into::into)
        }

        Ok(match self.0 {
            iroha_data_model::Value::Bool(v) => PyBool::new(py, v).into(),
            iroha_data_model::Value::String(v) => PyString::new(py, &v).into(),
            iroha_data_model::Value::Name(v) => PyString::new(py, v.as_ref()).into(),
            iroha_data_model::Value::Vec(elems) => {
                let mut pyelems = Vec::with_capacity(elems.len());
                for elem in elems {
                    let pyvalue = ValueWrapper(elem).into_py(py)?;
                    pyelems.push(pyvalue);
                }
                PyList::new(py, pyelems).into()
            }
            iroha_data_model::Value::Ipv4Addr(v) => to_py_ip(py, v.to_string())?,
            iroha_data_model::Value::Ipv6Addr(v) => to_py_ip(py, v.to_string())?,
            iroha_data_model::Value::LimitedMetadata(v) => {
                Into::<MetadataWrapper>::into(v).into_py(py)?.into()
            }
            _ => unimplemented!(),
        })
    }
}

pub fn register_items(py: Python<'_>, module: &PyModule) -> PyResult<()> {
    account::register_items(py, module)?;
    asset::register_items(py, module)?;
    domain::register_items(py, module)?;
    role::register_items(py, module)?;
    crypto::register_items(py, module)?;
    Ok(())
}
