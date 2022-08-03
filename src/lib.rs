//! iroha2-python sys library with all classes (wrapped rust structures) with methods

// Allow panic because of bad and unsafe pyo3
#![allow(
    clippy::panic,
    clippy::needless_pass_by_value,
    clippy::used_underscore_binding,
    clippy::multiple_inherent_impl
)]

use std::collections::HashMap;
use std::ops::{Deref, DerefMut};

use color_eyre::eyre;
use iroha_client::{client, config::Configuration};
use iroha_crypto::{Hash, KeyGenConfiguration};
use iroha_crypto::{PrivateKey, PublicKey};
use iroha_data_model::prelude::*;
use iroha_version::prelude::*;
use pyo3::class::iter::IterNextOutput;
use pyo3::prelude::*;

use crate::python::*;

mod python;
mod types;

#[pymethods]
impl KeyPair {
    /// Generates new key
    /// # Errors
    #[new]
    pub fn generate() -> PyResult<Self> {
        iroha_crypto::KeyPair::generate()
            .map_err(to_py_err)
            .map(Into::into)
    }

    /// Create keypair with some seed
    /// # Errors
    #[staticmethod]
    pub fn with_seed(seed: Vec<u8>) -> PyResult<Self> {
        let cfg = KeyGenConfiguration::default().use_seed(seed);
        iroha_crypto::KeyPair::generate_with_configuration(cfg)
            .map_err(to_py_err)
            .map(Into::into)
    }

    /// Gets public key
    #[getter]
    pub fn public(&self) -> ToPy<PublicKey> {
        ToPy(self.public_key().clone())
    }

    /// Gets private key
    #[getter]
    pub fn private(&self) -> ToPy<PrivateKey> {
        ToPy(self.private_key().clone())
    }
}

/// Hash bytes
#[pyfunction]
pub fn hash(bytes: Vec<u8>) -> ToPy<Hash> {
    ToPy(Hash::new(&bytes))
}

#[pymethods]
impl Client {
    /// Creates new client
    #[new]
    pub fn new(cfg: ToPy<Configuration>) -> PyResult<Self> {
        client::Client::new(&cfg).map_err(to_py_err).map(Self::from)
    }

    /// Creates new client with specified headers
    ///
    /// # Errors
    /// - If configuration isn't valid
    #[staticmethod]
    pub fn with_headers(
        cfg: ToPy<Configuration>,
        headers: HashMap<String, String>,
    ) -> PyResult<Self> {
        client::Client::with_headers(&cfg, headers)
            .map_err(to_py_err)
            .map(Self::from)
    }

    /// Queries peer
    /// # Errors
    /// Can fail if there is no access to peer
    pub fn request(&mut self, query: ToPy<QueryBox>) -> PyResult<ToPy<Value>> {
        self.deref_mut()
            .request(query.into_inner())
            .map_err(to_py_err)
            .map(ToPy)
    }

    /// Get transaction body
    /// # Errors
    pub fn tx_body(
        &mut self,
        isi: Vec<ToPy<Instruction>>,
        metadata: ToPy<UnlimitedMetadata>,
    ) -> PyResult<Vec<u8>> {
        let isi = isi.into_iter().map(ToPy::into_inner).into();
        self.build_transaction(isi, metadata.into_inner())
            .map(VersionedTransaction::from)
            .map_err(to_py_err)
            .map(|tx| tx.encode_versioned())
    }

    /// Sends transaction to peer
    /// # Errors
    /// Can fail if there is no access to peer
    pub fn submit_all_with_metadata(
        &mut self,
        isi: Vec<ToPy<Instruction>>,
        metadata: ToPy<UnlimitedMetadata>,
    ) -> PyResult<ToPy<Hash>> {
        let isi = isi.into_iter().map(ToPy::into_inner);
        self.deref_mut()
            .submit_all_with_metadata(isi, metadata.into_inner())
            .map(|h| *h)
            .map_err(to_py_err)
            .map(ToPy)
    }

    /// Sends transaction to peer and waits till its finalization
    /// # Errors
    /// Can fail if there is no access to peer
    pub fn submit_all_blocking_with_metadata(
        &mut self,
        isi: Vec<ToPy<Instruction>>,
        metadata: ToPy<UnlimitedMetadata>,
    ) -> PyResult<ToPy<Hash>> {
        let isi = isi.into_iter().map(ToPy::into_inner);
        self.deref_mut()
            .submit_all_blocking_with_metadata(isi, metadata.into_inner())
            .map(|h| *h)
            .map_err(to_py_err)
            .map(ToPy)
    }

    /// Listen on web socket events
    pub fn listen_for_events(&mut self, event_filter: ToPy<FilterBox>) -> PyResult<EventIterator> {
        self.deref_mut()
            .listen_for_events(event_filter.into_inner())
            .map_err(to_py_err)
            .map(|iter| {
                let boxed = Box::new(iter);
                EventIterator::new(boxed)
            })
    }
}

// HACK: `EventIterator` was made private in iroha for some reason
#[pyclass]
pub struct EventIterator {
    inner: Box<dyn Iterator<Item = eyre::Result<Event>> + Send>,
}

impl EventIterator {
    fn new(inner: Box<dyn Iterator<Item = eyre::Result<Event>> + Send>) -> Self {
        Self { inner }
    }
}

#[pymethods]
impl EventIterator {
    fn __iter__(slf: PyRefMut<Self>) -> PyRefMut<Self> {
        slf
    }

    fn __next__(mut slf: PyRefMut<Self>) -> IterNextOutput<ToPy<Event>, &'static str> {
        #[allow(clippy::unwrap_used)]
        slf.inner
            .next()
            .map(Result::unwrap) // TODO:
            .map(ToPy)
            .map_or(IterNextOutput::Return("Ended"), IterNextOutput::Yield)
    }
}

#[rustfmt::skip]
wrap_class!(
    KeyPair        { keys: iroha_crypto::KeyPair   }: Debug + Clone,
    Client         { cl:   client::Client          }: Debug + Clone,
);

/// A Python module implemented in Rust.
#[pymodule]
pub fn iroha2(_: Python, m: &PyModule) -> PyResult<()> {
    register_wrapped_classes(m)?;
    m.add_class::<types::Dict>()?;
    m.add_class::<types::List>()?;
    Ok(())
}
