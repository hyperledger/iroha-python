use pyo3::{
    exceptions::{PyRuntimeError, PyValueError},
    prelude::*,
};

use super::crypto::*;
use super::PyAccountId;
use iroha_crypto::{Hash, Signature};
use iroha_data_model::prelude::{SignedTransaction, TransactionQueryOutput, TransactionValue};
use iroha_data_model::transaction::TransactionPayload;
use parity_scale_codec::{Decode, Encode};

use super::PyMirror;

#[pyclass(name = "TransactionQueryOutput")]
#[derive(Clone, derive_more::From, derive_more::Into, derive_more::Deref)]
pub struct PyTransactionQueryOutput(pub TransactionQueryOutput);

impl PyMirror for TransactionQueryOutput {
    type Mirror = PyTransactionQueryOutput;

    fn mirror(self) -> PyResult<Self::Mirror> {
        Ok(PyTransactionQueryOutput(self))
    }
}

#[pymethods]
impl PyTransactionQueryOutput {
    #[getter]
    fn get_block_hash(&self) -> [u8; Hash::LENGTH] {
        self.0.block_hash.as_ref().clone()
    }

    #[getter]
    fn get_transaction(&self) -> PyTransactionValue {
        PyTransactionValue(self.0.transaction.clone())
    }
}

#[pyclass(name = "TransactionValue")]
#[derive(Clone, derive_more::From, derive_more::Into, derive_more::Deref)]
pub struct PyTransactionValue(pub TransactionValue);

impl PyMirror for TransactionValue {
    type Mirror = PyTransactionValue;

    fn mirror(self) -> PyResult<Self::Mirror> {
        Ok(PyTransactionValue(self))
    }
}

#[pymethods]
impl PyTransactionValue {
    #[getter]
    fn get_value(&self) -> PySignedTransaction {
        self.0.value.clone().into()
    }

    #[getter]
    fn get_error(&self) -> Option<String> {
        self.0.error.as_ref().map(|e| e.to_string())
    }
}

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
    fn append_signature(&mut self, key_pair: &PyKeyPair) {
        self.0 = self.0.clone().sign(&key_pair.0);
    }

    /*
    /// Return transaction instructions
    #[inline]
    pub fn instructions(&self) -> &Executable {
        let SignedTransaction::V1(tx) = self;
        &tx.payload.instructions
    }
    */
    /// Return transaction authority
    pub fn authority(&self) -> PyAccountId {
        self.0.authority().clone().into()
    }
    /*
    /// Return transaction metadata.
    pub fn metadata(&self) -> &UnlimitedMetadata {
        let SignedTransaction::V1(tx) = self;
        &tx.payload.metadata
    }
    */

    /// Creation timestamp as [`core::time::Duration`]
    pub fn creation_time_ms(&self) -> u64 {
        self.0.creation_time().as_millis() as u64
    }

    /// If transaction is not committed by this time it will be dropped.
    pub fn time_to_live(&self) -> Option<u64> {
        self.0.time_to_live().map(|t| t.as_millis() as u64)
    }

    /// Transaction nonce
    pub fn nonce(&self) -> u32 {
        if let Some(num) = self.0.nonce() {
            num.into()
        } else {
            0
        }
    }

    /// Transaction chain id
    pub fn chain_id(&self) -> String {
        format!("{:?}", self.0.chain_id())
    }

    /// Return transaction signatures
    pub fn signatures(&self) -> Vec<PySignature> {
        self.0
            .signatures()
            .into_iter()
            .map(|s| {
                let s2: Signature = s.clone().into();
                s2.into()
            })
            .collect()
    }

    /// Calculate transaction [`Hash`](`iroha_crypto::HashOf`).
    pub fn hash(&self) -> [u8; Hash::LENGTH] {
        let hash: Hash = self.0.hash().into();
        hash.into()
    }
}

pub fn register_items(_py: Python<'_>, module: &PyModule) -> PyResult<()> {
    module.add_class::<PySignedTransaction>()?;
    module.add_class::<PyTransactionQueryOutput>()?;
    Ok(())
}
