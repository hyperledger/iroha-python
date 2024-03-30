use pyo3::{
    exceptions::{PyRuntimeError, PyValueError},
    prelude::*,
};

use super::crypto::PyKeyPair;
use iroha_data_model::prelude::SignedTransaction;
use parity_scale_codec::{Decode, Encode};

use super::PyMirror;

#[pyclass(name = "SignedTransaction")]
#[derive(Clone, derive_more::From, derive_more::Into, derive_more::Deref)]
pub struct PySignedTransaction(pub SignedTransaction);

impl PyMirror for SignedTransaction {
    type Mirror = PySignedTransaction;

    fn mirror(self) -> PyResult<Self::Mirror> {
        Ok(PySignedTransaction(self))
    }
}

#[pymethods]
impl PySignedTransaction {
    #[staticmethod]
    fn decode_hex(encoded: &str) -> PyResult<Self> {
        let bytes = hex::decode(encoded)
            .map_err(|e| PyValueError::new_err(format!("Failed to decode hex: {e}")))?;
        let pk = SignedTransaction::decode(&mut bytes.as_slice())
            .map_err(|e| PyValueError::new_err(format!("Failed to decode transaction: {e}")))?;
        Ok(Self(pk))
    }
    fn encode_hex(&self) -> String {
        hex::encode(self.encode())
    }
    fn append_signature(&mut self, key_pair: &PyKeyPair) -> PyResult<()> {
        self.0 = self
            .0
            .clone()
            .sign(key_pair.0.clone())
            .map_err(|e| PyValueError::new_err(format!("Failed to sign transaction: {e}")))?;
        Ok(())
    }
}

pub fn register_items(_py: Python<'_>, module: &PyModule) -> PyResult<()> {
    module.add_class::<PySignedTransaction>()?;
    Ok(())
}
