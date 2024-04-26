use pyo3::{
    exceptions::{PyRuntimeError, PyValueError},
    prelude::*,
};

use iroha_crypto::{Algorithm, Hash, KeyPair, PrivateKey, PublicKey, Signature};

use super::PyMirror;

#[pyclass(name = "PrivateKey")]
#[derive(Clone, derive_more::From, derive_more::Into, derive_more::Deref)]
pub struct PyPrivateKey(pub PrivateKey);

impl PyMirror for PrivateKey {
    type Mirror = PyPrivateKey;

    fn mirror(self) -> PyResult<Self::Mirror> {
        Ok(PyPrivateKey(self))
    }
}

#[pymethods]
impl PyPrivateKey {
    #[new]
    fn new(encoded: &str) -> PyResult<Self> {
        let pk = PrivateKey::from_hex(Algorithm::default(), &encoded)
            .map_err(|e| PyValueError::new_err(format!("Invalid private key: {e}")))?;
        Ok(Self(pk))
    }
}

#[pyclass(name = "PublicKey")]
#[derive(Clone, derive_more::From, derive_more::Into, derive_more::Deref)]
pub struct PyPublicKey(pub PublicKey);

#[pymethods]
impl PyPublicKey {
    #[new]
    fn new(encoded: &str) -> PyResult<Self> {
        let pk = encoded
            .parse()
            .map_err(|e| PyValueError::new_err(format!("Invalid private key: {e}")))?;
        Ok(Self(pk))
    }

    fn __repr__(&self) -> String {
        format!("{:?}", self.0)
    }
}

impl PyMirror for PublicKey {
    type Mirror = PyPublicKey;

    fn mirror(self) -> PyResult<Self::Mirror> {
        Ok(PyPublicKey(self))
    }
}

#[pyclass(name = "KeyPair")]
#[derive(Clone, derive_more::From, derive_more::Into, derive_more::Deref)]
pub struct PyKeyPair(pub KeyPair);

impl PyMirror for KeyPair {
    type Mirror = PyKeyPair;

    fn mirror(self) -> PyResult<Self::Mirror> {
        Ok(PyKeyPair(self))
    }
}

#[pymethods]
impl PyKeyPair {
    #[staticmethod]
    fn generate() -> PyResult<Self> {
        Ok(PyKeyPair(KeyPair::random()))
    }

    #[staticmethod]
    fn from_json(json_str: &str) -> PyResult<Self> {
        serde_json::from_str::<KeyPair>(json_str)
            .map(|k| k.into())
            .map_err(|error| {
                PyErr::new::<PyValueError, _>(format!(
                    "Error: Failed to deserialize keypair: {}",
                    error
                ))
            })
            .into()
    }

    #[getter]
    fn get_private_key(&self) -> PyPrivateKey {
        self.0.private_key().clone().into()
    }

    #[getter]
    fn get_public_key(&self) -> PyPublicKey {
        self.0.public_key().clone().into()
    }

    fn sign(&self, payload: &[u8]) -> PySignature {
        PySignature(Signature::new(&self.0, payload))
    }

    fn __repr__(&self) -> String {
        format!("{:?}", self.0)
    }
}

#[pyclass(name = "Signature")]
#[derive(Clone, derive_more::From, derive_more::Into, derive_more::Deref)]
pub struct PySignature(pub Signature);

impl PyMirror for Signature {
    type Mirror = PySignature;

    fn mirror(self) -> PyResult<Self::Mirror> {
        Ok(PySignature(self))
    }
}

#[pymethods]
impl PySignature {
    fn __bytes__(&self) -> &[u8] {
        self.0.payload()
    }
}

#[pyfunction]
fn hash(bytes: &[u8]) -> [u8; Hash::LENGTH] {
    Hash::new(bytes).into()
}

pub fn register_items(_py: Python<'_>, module: &PyModule) -> PyResult<()> {
    module.add_class::<PyPrivateKey>()?;
    module.add_class::<PyPublicKey>()?;
    module.add_class::<PyKeyPair>()?;
    module.add_wrapped(wrap_pyfunction!(hash))?;
    Ok(())
}
