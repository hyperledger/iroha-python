//! iroha2-python sys library with all classes (wrapped rust structures) with methods

// Allow panic because of bad and unsafe pyo3
#![allow(clippy::panic)]

use std::ops::{Deref, DerefMut};

use iroha_client::{client, config::Configuration};
use iroha_crypto::{Hash, PrivateKey, PublicKey};
use iroha_data_model::prelude::*;
use pyo3::class::iter::IterNextOutput;
use pyo3::exceptions::PyException;
use pyo3::prelude::*;
use pyo3::PyIterProtocol;

macro_rules! wrap_class {
    (
        $(
            $ty:ident {
                $field:ident : $outer_ty:ty
            } : $( $derive:ident $(+)? )*
        ),*
        $(,)?
    ) => {$(
        #[pyclass]
        #[derive($($derive,)*)]
        pub struct $ty {
            $field: $outer_ty,
        }

        impl Deref for $ty {
            type Target = $outer_ty;
            fn deref(&self) -> &Self::Target {
                &self.$field
            }
        }

        impl DerefMut for $ty {
            fn deref_mut(&mut self) -> &mut Self::Target {
                &mut self.$field
            }
        }

        impl From<$outer_ty> for $ty {
            fn from(outer: $outer_ty) -> Self {
                Self {
                    $field: outer,
                }
            }
        }

        impl From<$ty> for $outer_ty {
            fn from(from: $ty) -> Self {
                from.$field
            }
        }

        #[pymethods]
        impl $ty {
            fn __str__(&self) -> String {
                format!("{:#?}", self)
            }
        }
    )*
        fn register_wrapped_classes(m: &PyModule) -> PyResult<()> {
            $(m.add_class::<$ty>()?;)*
            Ok(())
        }
    };
}

#[derive(Debug, Clone, Copy, Eq, PartialEq)]
pub struct Dict<T>(T);

impl<T> Deref for Dict<T> {
    type Target = T;
    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl<T> DerefMut for Dict<T> {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}

impl<T> Dict<T> {
    #[allow(clippy::missing_const_for_fn)]
    pub fn into_inner(self) -> T {
        self.0
    }
}

impl<'source, T: serde::de::DeserializeOwned> FromPyObject<'source> for Dict<T> {
    fn extract(obj: &'source PyAny) -> PyResult<Self> {
        let obj = if obj.hasattr("to_rust")? {
            obj.call_method0("to_rust")?
        } else {
            obj
        };

        pythonize::depythonize(obj).map_err(to_py_err).map(Self)
    }
}

impl<'source, T: serde::Serialize> IntoPy<PyObject> for Dict<T> {
    fn into_py(self, py: Python) -> PyObject {
        #[allow(clippy::expect_used)]
        pythonize::pythonize(py, &self.into_inner()).expect("Lets hope pythonize won't complain :(")
    }
}

fn to_py_err(err: impl Into<iroha_error::Error>) -> PyErr {
    PyException::new_err(err.into().report().to_string())
}

#[pymethods]
impl KeyPair {
    /// Generates new key
    /// # Errors
    #[new]
    pub fn generate() -> PyResult<Self> {
        let keys = iroha_crypto::KeyPair::generate().map_err(to_py_err)?;
        Ok(Self { keys })
    }

    #[getter]
    pub fn public(&self) -> Dict<PublicKey> {
        Dict(self.public_key.clone())
    }

    #[getter]
    pub fn private(&self) -> Dict<PrivateKey> {
        Dict(self.private_key.clone())
    }
}

#[pymethods]
impl Client {
    #[new]
    pub fn new(cfg: Dict<Configuration>) -> Self {
        client::Client::new(&cfg).into()
    }

    /// Queries peer
    /// # Errors
    /// Can fail if there is no access to peer
    pub fn request(&mut self, query: Dict<QueryBox>) -> PyResult<Dict<Value>> {
        self.deref_mut()
            .request(query.into_inner())
            .map_err(to_py_err)
            .map(Dict)
    }

    /// Sends transaction to peer
    /// # Errors
    /// Can fail if there is no access to peer
    pub fn submit_all_with_metadata(
        &mut self,
        isi: Vec<Dict<Instruction>>,
        metadata: Dict<UnlimitedMetadata>,
    ) -> PyResult<Dict<Hash>> {
        let isi = isi.into_iter().map(Dict::into_inner).collect();
        self.deref_mut()
            .submit_all_with_metadata(isi, metadata.into_inner())
            .map_err(to_py_err)
            .map(Dict)
    }

    /// Sends transaction to peer and waits till its finalization
    /// # Errors
    /// Can fail if there is no access to peer
    pub fn submit_all_blocking_with_metadata(
        &mut self,
        isi: Vec<Dict<Instruction>>,
        metadata: Dict<UnlimitedMetadata>,
    ) -> PyResult<Dict<Hash>> {
        let isi = isi.into_iter().map(Dict::into_inner).collect();
        self.deref_mut()
            .submit_all_blocking_with_metadata(isi, metadata.into_inner())
            .map_err(to_py_err)
            .map(Dict)
    }

    /// Listen on web socket events
    pub fn listen_for_events(
        &mut self,
        event_filter: Dict<EventFilter>,
    ) -> PyResult<EventIterator> {
        self.deref_mut()
            .listen_for_events(*event_filter)
            .map(EventIterator::from)
            .map_err(to_py_err)
    }

    /// Account field on client
    #[getter]
    pub fn account(&self) -> Dict<AccountId> {
        Dict(self.account_id.clone())
    }
}

#[pyproto]
impl PyIterProtocol for EventIterator {
    fn __next__(
        mut slf: PyRefMut<Self>,
    ) -> IterNextOutput<Dict<Result<Event, String>>, &'static str> {
        match slf.next() {
            Some(item) => IterNextOutput::Yield(Dict(item.map_err(|e| e.to_string()))),
            None => IterNextOutput::Return("Ended"),
        }
    }
}

#[rustfmt::skip]
wrap_class!(
    KeyPair        { keys: iroha_crypto::KeyPair }: Debug + Clone,
    Client         { cl:   client::Client        }: Debug + Clone,
    EventIterator  { it:   client::EventIterator }: Debug,
);

/// A Python module implemented in Rust.
#[pymodule]
pub fn iroha2(_: Python, m: &PyModule) -> PyResult<()> {
    register_wrapped_classes(m)?;
    m.add_class::<pythonize::dict::Dict>()?;
    Ok(())
}
