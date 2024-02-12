use pyo3::{
    exceptions::{PyRuntimeError, PyValueError},
    prelude::*,
};

use iroha_crypto::{Algorithm, KeyPair, PrivateKey, PublicKey, KeyGenConfiguration};

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
        let bytes = hex::decode(encoded)
            .map_err(|e| PyValueError::new_err(format!("Invalid private key: {e}")))?;
        let pk = PrivateKey::from_hex(Algorithm::default(), &bytes)
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
        let kp = KeyPair::generate()
            .map_err(|e| PyRuntimeError::new_err(format!("Failed to generate keypair: {e}")))?;
        Ok(PyKeyPair(kp))
    }
    
    #[staticmethod]
    fn from_json(json_str: &str) -> PyResult<Self> {
        serde_json::from_str::<KeyPair>(json_str).map(|k| k.into()).map_err(|error| {
            PyErr::new::<PyValueError, _>(format!("Error: Failed to deserialize keypair: {}", error))
        }).into()
    }

    #[getter]
    fn get_private_key(&self) -> PyPrivateKey {
        self.0.private_key().clone().into()
    }

    #[getter]
    fn get_public_key(&self) -> PyPublicKey {
        self.0.public_key().clone().into()
    }

    fn __repr__(&self) -> String {
        format!("{:?}", self.0)
    }
}

#[pyclass(name = "KeyGenConfiguration")]
#[derive(Clone, derive_more::From, derive_more::Into, derive_more::Deref)]
pub struct PyKeyGenConfiguration(pub KeyGenConfiguration);

impl PyMirror for KeyGenConfiguration {
    type Mirror = PyKeyGenConfiguration;

    fn mirror(self) -> PyResult<Self::Mirror> {
        Ok(PyKeyGenConfiguration(self))
    }
}

#[pymethods]
impl PyKeyGenConfiguration {
    #[staticmethod]
    fn default() -> Self {
        PyKeyGenConfiguration(KeyGenConfiguration::default())
    }

    fn use_seed_hex(&self, hex_str: &str) -> PyResult<Self> {
        let seed = hex::decode(hex_str).map_err(|e| PyValueError::new_err(format!("Invalid hex string: {e}")))?;
        let copy : KeyGenConfiguration = self.clone().into();
        Ok(copy.use_seed(seed).into())
    }
    
    fn use_private_key(&self, private_key: PyPrivateKey) -> PyResult<Self> {
        let copy : KeyGenConfiguration = self.clone().into();
        Ok(copy.use_private_key(private_key.into()).into())
    }
    
    fn generate(&self) -> PyResult<PyKeyPair> {
        let kp = KeyPair::generate_with_configuration(self.0.clone()).map_err(|e| PyRuntimeError::new_err(format!("Failed to generate keypair: {e}")))?;
        Ok(PyKeyPair(kp))
    }

    fn __repr__(&self) -> String {
        format!("{:?}", self.0)
    }
}


pub fn register_items(_py: Python<'_>, module: &PyModule) -> PyResult<()> {
    module.add_class::<PyPrivateKey>()?;
    module.add_class::<PyPublicKey>()?;
    module.add_class::<PyKeyPair>()?;
    module.add_class::<PyKeyGenConfiguration>()?;
    Ok(())
}
