//! Module with python dictionary which can be hashed

use std::collections::btree_map::IntoIter;
use std::collections::BTreeMap;
use std::convert::TryFrom;

use color_eyre::eyre::eyre;
use pyo3::basic::CompareOp;
use pyo3::class::iter::{IterNextOutput, PyIterProtocol};
use pyo3::conversion::{ToBorrowedObject, ToPyObject};
use pyo3::exceptions::PyKeyError;
use pyo3::types::{PyDict, PyList};
use pyo3::{prelude::*, PyMappingProtocol, PyNativeType, PyObjectProtocol};
use pythonize::{PythonizeDictType, PythonizeListType};

pub use dict::Dict;
pub use list::List;

type Hash = isize;

pub mod list {
    use pyo3::{types::PySequence, PySequenceProtocol};

    use crate::to_py_err;

    use super::*;

    /// List which can be hashed. Requires all items to be hashable
    #[pyclass]
    #[derive(Debug, Clone, Default)]
    pub struct List {
        vec: Vec<PyObject>,
    }

    impl From<&PyList> for List {
        fn from(list: &PyList) -> Self {
            let py = list.py();
            let vec = list
                .into_iter()
                .map(move |i| i.to_object(py))
                .collect::<Vec<_>>();
            Self { vec }
        }
    }

    impl PythonizeListType for List {
        fn create_sequence<T, U>(
            py: Python,
            elements: impl IntoIterator<Item = T, IntoIter = U>,
        ) -> PyResult<&PySequence>
        where
            T: ToPyObject,
            U: ExactSizeIterator<Item = T>,
        {
            let vec = elements.into_iter().map(move |k| k.to_object(py)).collect();
            Py::new(py, List { vec })?
                .into_ref(py)
                .downcast()
                .map_err(Into::into)
        }
    }

    impl List {
        pub fn hash(&self, py: Python) -> PyResult<Hash> {
            let sum_hash = |a: isize, b: isize| a.wrapping_add(b).into_py(py).as_ref(py).hash();

            self.iter(py)
                .filter_map(|i| i.extract::<isize>().ok())
                .fold(Ok(0), |a, b| a.and_then(|a| sum_hash(a, b)))
        }

        pub fn iter<'py>(&'py self, py: Python<'py>) -> impl Iterator<Item = &'py PyAny> + 'py {
            self.vec.iter().map(move |i| i.as_ref(py))
        }
    }

    #[pyproto]
    impl PyObjectProtocol for List {
        /// Comparison which relies on hashes
        fn __richcmp__(&self, other: Self, op: CompareOp) -> PyResult<bool> {
            if let CompareOp::Eq = op {
                Python::with_gil(|py| Ok(self.hash(py)? == other.hash(py)?))
            } else {
                Ok(false)
            }
        }

        fn __hash__(&self) -> PyResult<isize> {
            Python::with_gil(|py| self.hash(py))
        }

        fn __str__(&self) -> PyResult<String> {
            Python::with_gil(|py| {
                let items = self
                    .iter(py)
                    .map(|k| k.str().map(ToString::to_string))
                    .collect::<PyResult<Vec<_>>>()?
                    .join(",");
                Ok(format!("[{}]", items))
            })
        }

        fn __repr__(&self) -> PyResult<String> {
            self.__str__()
        }
    }

    #[pyproto]
    impl PySequenceProtocol for List {
        fn __len__(&'p self) -> usize {
            self.vec.len()
        }

        fn __getitem__(&'p self, idx: isize) -> PyResult<PyObject> {
            #[allow(clippy::cast_sign_loss, clippy::cast_possible_wrap)]
            let idx = if idx >= 0 {
                idx
            } else {
                (self.vec.len() as isize) - idx
            } as usize;

            self.vec
                .get(idx)
                .map(Clone::clone)
                .ok_or_else(|| eyre!("Failed to get item at index {}", idx))
                .map_err(to_py_err)
        }

        fn __setitem__(&mut self, idx: isize, value: PyObject) -> PyResult<()> {
            #[allow(clippy::cast_sign_loss, clippy::cast_possible_wrap)]
            let idx = if idx >= 0 {
                idx
            } else {
                (self.vec.len() as isize) - idx
            } as usize;

            *self
                .vec
                .get_mut(idx)
                .ok_or_else(|| eyre!("Failed to get item at index {}", idx))
                .map_err(to_py_err)? = value;
            Ok(())
        }
    }
}

pub mod dict {
    use pyo3::types::PyMapping;

    use super::*;

    /// Dictionary which can be hashed. Requires both keys and values to be hashable
    #[pyclass]
    #[derive(Debug, Clone, Default)]
    pub struct Dict {
        map: BTreeMap<
            // Key hash
            Hash,
            BTreeMap<
                // Value hash
                Hash,
                // Entry
                (PyObject, PyObject),
            >,
        >,
    }

    impl TryFrom<&PyDict> for Dict {
        type Error = PyErr;
        fn try_from(dict: &PyDict) -> PyResult<Self> {
            let mut map = Dict::new();
            for (k, v) in dict {
                map.set_item(dict.py(), k, v)?;
            }
            Ok(map)
        }
    }

    fn as_dict_obj(py: Python, obj: PyObject) -> PyResult<PyObject> {
        let obj = obj.into_ref(py);
        let obj = if obj.is_instance::<PyDict>()? {
            Dict::try_from(obj.downcast::<PyDict>()?)?.into_py(py)
        } else {
            obj.to_object(py)
        };
        Ok(obj)
    }

    impl Dict {
        fn is_eq(py: Python, a: &PyObject, b: &PyObject) -> bool {
            a.as_ref(py)
                .rich_compare(b.as_ref(py), CompareOp::Eq)
                .and_then(PyAny::extract)
                .unwrap_or(false)
        }

        /// Sets item with key and value
        pub fn set_item<K: ToPyObject, V: ToPyObject>(
            &mut self,
            py: Python,
            k: K,
            v: V,
        ) -> PyResult<()> {
            let k = as_dict_obj(py, k.to_object(py))?;
            let v = as_dict_obj(py, v.to_object(py))?;
            let k_hash = k.as_ref(py).hash()?;
            let v_hash = v.as_ref(py).hash()?;
            self.map.entry(k_hash).or_default().insert(v_hash, (k, v));
            Ok(())
        }

        /// Gets item by key
        pub fn get_item<K: ToBorrowedObject>(
            &self,
            py: Python,
            k: K,
        ) -> PyResult<Option<PyObject>> {
            let k = as_dict_obj(py, k.to_object(py))?;
            let k_hash = k.as_ref(py).hash()?;
            let bucket = match self.map.get(&k_hash) {
                Some(bucket) => bucket,
                None => return Ok(None),
            };
            Ok(bucket
                .values()
                .find(|(bucket_k, _)| Self::is_eq(py, &k, bucket_k))
                .map(|(_, v)| v.clone()))
        }

        /// Remove item by key
        pub fn remove_item<K: ToBorrowedObject>(
            &mut self,
            py: Python,
            k: K,
        ) -> PyResult<Option<PyObject>> {
            let k = as_dict_obj(py, k.to_object(py))?;
            let k_hash = k.as_ref(py).hash()?;
            let bucket = match self.map.get_mut(&k_hash) {
                Some(bucket) => bucket,
                None => return Ok(None),
            };
            Ok(bucket
                .values_mut()
                .find(|(bucket_k, _)| Self::is_eq(py, &k, bucket_k))
                .map(|(_, v)| v.clone()))
        }

        /// Iterator over both keys and values
        pub fn iter<'py>(
            &'py self,
            py: Python<'py>,
        ) -> impl Iterator<Item = (&'py PyAny, &'py PyAny)> + 'py {
            self.map
                .values()
                .flat_map(BTreeMap::values)
                .map(move |(k, v)| (k.clone().into_ref(py), v.clone().into_ref(py)))
        }

        /// Iterator which consumes object
        pub fn into_iter(self, py: Python<'_>) -> impl Iterator<Item = (&'_ PyAny, &'_ PyAny)> {
            self.map
                .into_iter()
                .flat_map(|(_, bucket)| bucket.into_iter())
                .map(move |(_, (k, v))| (k.into_ref(py), v.into_ref(py)))
        }

        /// Iterator over keys
        pub fn keys<'py>(&'py self, py: Python<'py>) -> impl Iterator<Item = &'py PyAny> + 'py {
            self.iter(py).map(|(k, _)| k)
        }

        /// Iterator over keys which consumes object
        pub fn into_keys(self, py: Python<'_>) -> impl Iterator<Item = &'_ PyAny> {
            self.into_iter(py).map(|(k, _)| k)
        }

        /// Iterator over values
        pub fn values<'py>(&'py self, py: Python<'py>) -> impl Iterator<Item = &'py PyAny> + 'py {
            self.iter(py).map(|(_, v)| v)
        }

        /// Iterator over values which consumes object
        pub fn into_values(self, py: Python<'_>) -> impl Iterator<Item = &'_ PyAny> {
            self.into_iter(py).map(|(_, v)| v)
        }

        /// Hashes object
        #[allow(clippy::unwrap_used)]
        pub fn hash(&self, py: Python) -> Hash {
            let sum_hash =
                |a: isize, b: isize| a.wrapping_add(b).into_py(py).as_ref(py).hash().unwrap();

            self.map
                .iter()
                .flat_map(|(&key, bucket)| bucket.keys().map(move |&value| sum_hash(key, value)))
                .fold(0, sum_hash)
        }

        /// Returns number of items in dictionary
        pub fn len(&self) -> usize {
            self.map.iter().fold(0, |prev, (_, next)| prev + next.len())
        }

        /// Checks whether dict is empty
        pub fn is_empty(&self) -> bool {
            self.map.len() == 0
        }
    }

    #[pymethods]
    impl Dict {
        /// Constructor
        #[new]
        pub fn new() -> Self {
            Self::default()
        }

        /// Returns an iterator over keys
        #[pyo3(name = "keys")]
        fn _keys(&self) -> Keys {
            Keys::new(self.clone())
        }

        /// Returns an iterator over values
        #[pyo3(name = "values")]
        fn _values(&self) -> Values {
            Values::new(self.clone())
        }

        /// Returns an iterator over both keys and values
        fn items(&self) -> Items {
            Items::new(self.clone())
        }
    }

    #[pyproto]
    impl PyObjectProtocol for Dict {
        /// Comparison which relies on hashes
        fn __richcmp__(&self, other: Self, op: CompareOp) -> bool {
            matches!(op, CompareOp::Eq if Python::with_gil(|py| self.hash(py) == other.hash(py)))
        }

        fn __hash__(&self) -> isize {
            Python::with_gil(|py| self.hash(py))
        }

        fn __str__(&self) -> PyResult<String> {
            Python::with_gil(|py| {
                let items = self
                    .iter(py)
                    .map(|(k, v)| Ok(format!("{}: {}", k.str()?, v.str()?)))
                    .collect::<PyResult<Vec<_>>>()?
                    .join(",");
                Ok(format!("{{{}}}", items))
            })
        }

        fn __repr__(&self) -> PyResult<String> {
            Python::with_gil(|py| {
                let items = self
                    .iter(py)
                    .map(|(k, v)| Ok(format!("{}: {}", k.repr()?, v.repr()?)))
                    .collect::<PyResult<Vec<_>>>()?
                    .join(",");
                Ok(format!("{{{}}}", items))
            })
        }
    }

    #[pyproto]
    impl PyMappingProtocol for Dict {
        fn __len__(&self) -> usize {
            self.len()
        }

        fn __setitem__(&mut self, key: PyObject, value: PyObject) -> PyResult<()> {
            Python::with_gil(|py| self.set_item(py, key, value))
        }

        fn __delitem__(&mut self, key: PyObject) -> PyResult<()> {
            Python::with_gil(|py| self.remove_item(py, key))?;
            Ok(())
        }

        fn __getitem__(&self, key: PyObject) -> PyResult<PyObject> {
            match Python::with_gil(|py| self.get_item(py, key.clone()))? {
                Some(obj) => Ok(obj),
                None => Err(PyErr::new::<PyKeyError, _>(key)),
            }
        }
    }

    #[pyclass]
    struct Items {
        dict: IntoIter<Hash, BTreeMap<Hash, (PyObject, PyObject)>>,
        bucket: Option<IntoIter<Hash, (PyObject, PyObject)>>,
    }

    impl Items {
        fn new(dict: Dict) -> Self {
            Self {
                dict: dict.map.into_iter(),
                bucket: None,
            }
        }

        fn next(&mut self) -> Option<(PyObject, PyObject)> {
            if let Some(bucket) = &mut self.bucket {
                if let Some((_, entry)) = bucket.next() {
                    return Some(entry);
                }
            }
            self.bucket = match self.dict.next() {
                Some((_, bucket)) => Some(bucket.into_iter()),
                None => return None,
            };

            self.next()
        }
    }

    #[pyclass]
    struct Keys {
        items: Items,
    }

    impl Keys {
        fn new(dict: Dict) -> Self {
            let items = Items::new(dict);
            Self { items }
        }
    }

    #[pyclass]
    struct Values {
        items: Items,
    }

    impl Values {
        fn new(dict: Dict) -> Self {
            let items = Items::new(dict);
            Self { items }
        }
    }

    #[pyproto]
    impl PyIterProtocol for Items {
        fn __next__(mut slf: PyRefMut<Self>) -> IterNextOutput<(PyObject, PyObject), ()> {
            match slf.next() {
                Some(entry) => IterNextOutput::Yield(entry),
                None => IterNextOutput::Return(()),
            }
        }
    }

    #[pyproto]
    impl PyIterProtocol for Keys {
        fn __next__(mut slf: PyRefMut<Self>) -> IterNextOutput<PyObject, ()> {
            match slf.items.next() {
                Some((entry, _)) => IterNextOutput::Yield(entry),
                None => IterNextOutput::Return(()),
            }
        }
    }

    #[pyproto]
    impl PyIterProtocol for Values {
        fn __next__(mut slf: PyRefMut<Self>) -> IterNextOutput<PyObject, ()> {
            match slf.items.next() {
                Some((_, entry)) => IterNextOutput::Yield(entry),
                None => IterNextOutput::Return(()),
            }
        }
    }

    impl PythonizeDictType for Dict {
        fn create_mapping(py: Python) -> PyResult<&PyMapping> {
            Py::new(py, Dict::new())?
                .into_ref(py)
                .downcast()
                .map_err(Into::into)
        }
    }
}
