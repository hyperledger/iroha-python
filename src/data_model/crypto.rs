use pyo3::{
    exceptions::{PyRuntimeError, PyValueError},
    prelude::*,
};

use iroha_crypto::{Algorithm, Hash, KeyPair, PrivateKey, PublicKey, Signature};
use iroha_primitives::const_vec::ConstVec;

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

#[pyclass(name = "PublicKey")]
#[derive(Clone, derive_more::From, derive_more::Into, derive_more::Deref)]
pub struct PyPublicKey(pub PublicKey);

#[pymethods]
impl PyPublicKey {
    #[staticmethod]
    fn from_string(encoded: &str) -> PyResult<Self> {
        let pk = encoded
            .parse()
            .map_err(|e| PyValueError::new_err(format!("Invalid public key: {e}")))?;
        Ok(Self(pk))
    }

    fn __repr__(&self) -> String {
        format!("{}", self.0)
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

fn string_to_algorithm(string: &str) -> PyResult<Algorithm> {
    match string {
        "Ed25519" => Ok(Algorithm::Ed25519),
        "Secp256k1" => Ok(Algorithm::Secp256k1),
        "BlsNormal" => Ok(Algorithm::BlsNormal),
        "BlsSmall" => Ok(Algorithm::BlsSmall),
        _ => Err(PyErr::new::<PyValueError, _>(format!(
            "Error: '{}' is not a supported cryptography algorithm. Supported ones are 'Ed25519', 'Secp256k1', 'BlsNormal' and 'BlsSmall'.",
            string
        ))),
    }
}

#[pymethods]
impl PyKeyPair {
    #[staticmethod]
    fn random() -> PyResult<Self> {
        Ok(PyKeyPair(KeyPair::random()))
    }
    #[staticmethod]
    fn random_with_algorithm(algorithm: &str) -> PyResult<Self> {
        Ok(PyKeyPair(KeyPair::random_with_algorithm(
            string_to_algorithm(algorithm)?,
        )))
    }

    #[staticmethod]
    fn from_hex_seed(hex_seed: &str) -> PyResult<Self> {
        let bytes = hex::decode(hex_seed)
            .map_err(|e| PyValueError::new_err(format!("Failed to decode hex: {e}")))?;
        Ok(PyKeyPair(KeyPair::from_seed(bytes, Algorithm::default())))
    }
    #[staticmethod]
    fn from_hex_seed_with_algorithm(hex_seed: &str, algorithm: &str) -> PyResult<Self> {
        let bytes = hex::decode(hex_seed)
            .map_err(|e| PyValueError::new_err(format!("Failed to decode hex: {e}")))?;
        Ok(PyKeyPair(KeyPair::from_seed(
            bytes,
            string_to_algorithm(algorithm)?,
        )))
    }

    #[staticmethod]
    fn from_private_key(pk: PyPrivateKey) -> PyResult<Self> {
        Ok(PyKeyPair(
            KeyPair::new(PublicKey::from(pk.0.clone()), pk.0)
                .map_err(|e| PyRuntimeError::new_err(format!("{e:?}")))?,
        ))
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
        PySignature(Signature::new(&self.0.private_key(), payload))
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
    fn __bytes__(&self) -> Vec<u8> {
        unsafe {
            let ss: ShadowSignature = std::mem::transmute(self.0.clone());
            let mut v = Vec::new();
            v.extend_from_slice(&ss.payload);
            v
        }
    }
}

struct ShadowSignature {
    pub payload: ConstVec<u8>,
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
