use pyo3::prelude::*;

use iroha_crypto::Hash;
use iroha_data_model::block::BlockHeader;

use super::PyMirror;

#[pyclass(name = "BlockHeader")]
#[derive(Clone, derive_more::From, derive_more::Into, derive_more::Deref)]
pub struct PyBlockHeader(pub BlockHeader);

impl PyMirror for BlockHeader {
    type Mirror = PyBlockHeader;

    fn mirror(self) -> PyResult<Self::Mirror> {
        Ok(PyBlockHeader(self))
    }
}

#[pymethods]
impl PyBlockHeader {
    #[getter]
    fn get_height(&self) -> u64 {
        self.0.height.get()
    }

    #[getter]
    fn get_timestamp_ms(&self) -> u64 {
        self.0.creation_time_ms
    }

    #[getter]
    fn get_consensus_previous_block_hash(&self) -> Option<[u8; Hash::LENGTH]> {
        self.0
            .prev_block_hash
            .as_ref()
            .map(|previous_block_hash| previous_block_hash.as_ref())
            .copied()
    }

    #[getter]
    fn get_transactions_hash(&self) -> [u8; Hash::LENGTH] {
        self.0.transactions_hash.as_ref().clone()
    }

    #[getter]
    fn get_view_change_index(&self) -> u32 {
        self.0.view_change_index
    }

    #[getter]
    fn get_consensus_estimation_ms(&self) -> u64 {
        self.0.consensus_estimation_ms
    }

    fn __repr__(&self) -> String {
        format!("{:?}", self.0)
    }
}

pub fn register_items(_py: Python<'_>, module: &PyModule) -> PyResult<()> {
    module.add_class::<PyBlockHeader>()?;
    Ok(())
}
