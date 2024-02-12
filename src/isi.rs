use iroha_data_model::isi::{
    InstructionExpr, MintExpr, RegisterExpr, TransferExpr, UnregisterExpr,
};
use iroha_data_model::NumericValue;
use pyo3::{exceptions::PyValueError, prelude::*};

use crate::data_model::account::{PyAccountId, PyNewAccount};
use crate::data_model::asset::{PyAssetDefinitionId, PyAssetId, PyNewAssetDefinition};
use crate::data_model::domain::{PyDomainId, PyNewDomain};

#[derive(Debug, Clone)]
#[pyclass(name = "Instruction")]
pub struct PyInstruction(pub InstructionExpr);

#[pymethods]
impl PyInstruction {
    #[staticmethod]
    /// Create an instruction for registering a new object.
    /// Currently supported are: Account, AssetDefinition and Domain
    fn register(py: Python<'_>, object: PyObject) -> PyResult<PyInstruction> {
        if let Ok(new_asset_definition) = object.extract::<PyNewAssetDefinition>(py) {
            return Ok(PyInstruction(InstructionExpr::Register(RegisterExpr::new(
                new_asset_definition.0,
            ))));
        }

        if let Ok(new_account) = object.extract::<PyNewAccount>(py) {
            return Ok(PyInstruction(InstructionExpr::Register(RegisterExpr::new(
                new_account.0,
            ))));
        }

        if let Ok(new_domain) = object.extract::<PyNewDomain>(py) {
            return Ok(PyInstruction(InstructionExpr::Register(RegisterExpr::new(
                new_domain.0,
            ))));
        }

        Err(PyValueError::new_err(
            "Only registration of accounts, asset definitions and domains is supported",
        ))
    }

    #[staticmethod]
    /// Create an instruction for un-registering an object.
    /// Currently supported are: Account, AssetDefinition and Domain
    fn unregister(py: Python<'_>, object: PyObject) -> PyResult<PyInstruction> {
        if let Ok(asset_definition_id) = object.extract::<PyAssetDefinitionId>(py) {
            return Ok(PyInstruction(InstructionExpr::Unregister(
                UnregisterExpr::new(asset_definition_id.0),
            )));
        }

        if let Ok(account_id) = object.extract::<PyAccountId>(py) {
            return Ok(PyInstruction(InstructionExpr::Unregister(
                UnregisterExpr::new(account_id.0),
            )));
        }

        if let Ok(domain_id) = object.extract::<PyDomainId>(py) {
            return Ok(PyInstruction(InstructionExpr::Unregister(
                UnregisterExpr::new(domain_id.0),
            )));
        }

        Err(PyValueError::new_err(
            "Only unregistration of accounts, asset definitions and domains is supported",
        ))
    }

    #[staticmethod]
    /// Create an instruction to transfer ownership of an object
    /// Currently supported are: Account, AssetDefinition and Domain
    fn transfer_ownership(
        py: Python<'_>,
        object: PyObject,
        from: PyAccountId,
        to: PyAccountId,
    ) -> PyResult<PyInstruction> {
        let (from, to) = (from.0, to.0);

        if let Ok(asset_definition_id) = object.extract::<PyAssetDefinitionId>(py) {
            return Ok(PyInstruction(InstructionExpr::Transfer(TransferExpr::new(
                from,
                asset_definition_id.0,
                to,
            ))));
        }

        if let Ok(account_id) = object.extract::<PyAccountId>(py) {
            return Ok(PyInstruction(InstructionExpr::Transfer(TransferExpr::new(
                from,
                account_id.0,
                to,
            ))));
        }

        if let Ok(domain_id) = object.extract::<PyDomainId>(py) {
            return Ok(PyInstruction(InstructionExpr::Transfer(TransferExpr::new(
                from,
                domain_id.0,
                to,
            ))));
        }

        Err(PyValueError::new_err(
            "Only transferring ownership of accounts, asset definitions and domains is supported",
        ))
    }

    #[staticmethod]
    // Transfer asset value from one account to another
    fn transfer(
        py: Python<'_>,
        object: PyObject,
        from: PyAssetId,
        to: PyAccountId,
    ) -> PyResult<PyInstruction> {
        let (from, to) = (from.0, to.0);

        let val = if let Ok(val) = object.extract::<u32>(py) {
            NumericValue::U32(val)
        } else if let Ok(val) = object.extract::<u128>(py) {
            NumericValue::U128(val)
        } else if let Ok(val) = object.extract::<f64>(py) {
            let fixed = val.try_into().map_err(|e| {
                PyValueError::new_err(format!("Couldn't convert {} to fixed: {}", val, e))
            })?;
            NumericValue::Fixed(fixed)
        } else {
            return Err(PyValueError::new_err("Invalid value to transfer"));
        };

        Ok(PyInstruction(InstructionExpr::Transfer(TransferExpr::new(
            from, val, to,
        ))))
    }

    #[staticmethod]
    // Mint value to an Asset
    fn mint(py: Python<'_>, value: PyObject, to: PyAssetId) -> PyResult<PyInstruction> {
        let val = if let Ok(val) = value.extract::<u32>(py) {
            NumericValue::U32(val)
        } else if let Ok(val) = value.extract::<u128>(py) {
            NumericValue::U128(val)
        } else if let Ok(val) = value.extract::<f64>(py) {
            let fixed = val.try_into().map_err(|e| {
                PyValueError::new_err(format!("Couldn't convert {} to fixed: {}", val, e))
            })?;
            NumericValue::Fixed(fixed)
        } else {
            return Err(PyValueError::new_err("Invalid value to transfer"));
        };

        Ok(PyInstruction(InstructionExpr::Mint(MintExpr::new(
            val, to.0,
        ))))
    }
}

pub fn register_items(_py: Python<'_>, module: &PyModule) -> PyResult<()> {
    module.add_class::<PyInstruction>()?;
    Ok(())
}
