use std::ops::{Deref, DerefMut};

use pyo3::exceptions::PyException;
use pyo3::prelude::*;
use pythonize::PythonizeTypes;

use crate::types;

#[macro_export]
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

        #[pyproto]
        impl PyObjectProtocol for $ty {
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

pub fn to_py_err(err: impl Into<iroha_error::Error>) -> PyErr {
    PyException::new_err(err.into().report().to_string())
}

#[derive(Debug, Clone, Copy, Eq, PartialEq)]
pub struct Dict<T>(pub T);

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

pub struct Pythonizer;
impl<'py> PythonizeTypes<'py> for Pythonizer {
    type Dict = types::dict::PythonizeDict<'py>;
    type List = types::list::PythonizeList<'py>;
}

impl<'source, T: serde::de::DeserializeOwned> FromPyObject<'source> for Dict<T> {
    fn extract(obj: &'source PyAny) -> PyResult<Self> {
        let obj = if obj.hasattr("to_rust")? {
            obj.call_method0("to_rust")?
        } else {
            obj
        };

        pythonize::depythonize_custom::<Pythonizer, _>(obj)
            .map_err(to_py_err)
            .map(Self)
    }
}

impl<'source, T: serde::Serialize> IntoPy<PyObject> for Dict<T> {
    fn into_py(self, py: Python) -> PyObject {
        #[allow(clippy::expect_used)]
        pythonize::pythonize_custom::<Pythonizer, _>(py, &self.into_inner())
            .expect("Lets hope pythonize won't complain :(")
    }
}
