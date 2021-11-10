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

use iroha_client::{client, config::Configuration};
use iroha_crypto::{Hash, KeyGenConfiguration, Signature};
use iroha_crypto::{PrivateKey, PublicKey};
use iroha_data_model::prelude::*;
use iroha_version::prelude::*;
use pyo3::class::basic::PyObjectProtocol;
use pyo3::class::iter::IterNextOutput;
use pyo3::prelude::*;
use pyo3::PyIterProtocol;

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
        ToPy(self.public_key.clone())
    }

    /// Gets private key
    #[getter]
    pub fn private(&self) -> ToPy<PrivateKey> {
        ToPy(self.private_key.clone())
    }
}

/// Hash bytes
#[pyfunction]
pub fn hash(bytes: Vec<u8>) -> ToPy<Hash> {
    ToPy(Hash::new(&bytes))
}

/// Sign payload using keypair
#[pyfunction]
pub fn sign(keys: KeyPair, payload: Vec<u8>) -> PyResult<ToPy<Signature>> {
    iroha_crypto::Signature::new(keys.into(), &payload)
        .map_err(to_py_err)
        .map(ToPy)
}

#[pymethods]
impl Client {
    /// Creates new client
    #[new]
    pub fn new(cfg: ToPy<Configuration>) -> Self {
        client::Client::new(&cfg).into()
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
        let isi = isi.into_iter().map(ToPy::into_inner).collect();
        self.build_transaction(isi, metadata.into_inner())
            .map(VersionedTransaction::from)
            .map_err(to_py_err)
            .and_then(|tx| tx.encode_versioned().map_err(to_py_err))
    }

    /// Get transaction body
    /// # Errors
    pub fn query_body(&mut self, request: ToPy<QueryBox>) -> PyResult<Vec<u8>> {
        let request = QueryRequest::new(request.into_inner(), self.account_id.clone());
        request
            .sign(self.cl.key_pair.clone())
            .map(VersionedSignedQueryRequest::from)
            .map_err(to_py_err)
            .and_then(|req| req.encode_versioned().map_err(to_py_err))
    }

    /// Sends transaction to peer
    /// # Errors
    /// Can fail if there is no access to peer
    pub fn submit_all_with_metadata(
        &mut self,
        isi: Vec<ToPy<Instruction>>,
        metadata: ToPy<UnlimitedMetadata>,
    ) -> PyResult<ToPy<Hash>> {
        let isi = isi.into_iter().map(ToPy::into_inner).collect();
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
        let isi = isi.into_iter().map(ToPy::into_inner).collect();
        self.deref_mut()
            .submit_all_blocking_with_metadata(isi, metadata.into_inner())
            .map(|h| *h)
            .map_err(to_py_err)
            .map(ToPy)
    }

    /// Listen on web socket events
    pub fn listen_for_events(
        &mut self,
        event_filter: ToPy<EventFilter>,
    ) -> PyResult<EventIterator> {
        self.deref_mut()
            .listen_for_events(*event_filter)
            .map(EventIterator::from)
            .map_err(to_py_err)
    }

    /// Account field on client
    #[getter]
    pub fn get_account(&self) -> ToPy<AccountId> {
        ToPy(self.account_id.clone())
    }

    /// Account field on client
    #[setter]
    pub fn set_account(&mut self, account: ToPy<AccountId>) {
        self.account_id = account.into_inner();
    }

    /// Headers field on client
    #[getter]
    pub fn get_headers(&self) -> HashMap<String, String> {
        self.headers.clone()
    }

    /// Account field on client
    #[setter]
    pub fn set_headers(&mut self, headers: HashMap<String, String>) {
        self.headers = headers;
    }
}

#[pyproto]
impl PyIterProtocol for EventIterator {
    fn __iter__(slf: PyRefMut<Self>) -> PyRefMut<Self> {
        slf
    }

    fn __next__(mut slf: PyRefMut<Self>) -> IterNextOutput<ToPy<Event>, &'static str> {
        #[allow(clippy::unwrap_used)]
        slf.next()
            .map(Result::unwrap)
            .map(ToPy)
            .map_or(IterNextOutput::Return("Ended"), IterNextOutput::Yield)
    }
}

#[rustfmt::skip]
wrap_class!(
    KeyPair        { keys: iroha_crypto::KeyPair   }: Debug + Clone,
    Client         { cl:   client::Client          }: Debug + Clone,
    EventIterator  { it:   client::EventIterator   }: Debug,
);

/// A Python module implemented in Rust.
#[pymodule]
pub fn iroha2(_: Python, m: &PyModule) -> PyResult<()> {
    register_wrapped_classes(m)?;
    m.add_class::<types::Dict>()?;
    m.add_class::<types::List>()?;
    Ok(())
}
