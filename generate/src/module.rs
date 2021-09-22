use std::collections::BTreeMap;
use std::fs;
use std::io::Write;
use std::iter::FromIterator;
use std::ops::{Deref, DerefMut};

use super::as_py::*;
use color_eyre::eyre::{eyre, Result, WrapErr};
use either::Either;
use iroha_schema::Metadata;
use syn::{Path, Type, TypePath};

#[derive(Debug, Clone, Default)]
pub struct Module {
    r#mod: BTreeMap<String, Either<Module, Metadata>>,
}

impl Deref for Module {
    type Target = BTreeMap<String, Either<Module, Metadata>>;
    fn deref(&self) -> &Self::Target {
        &self.r#mod
    }
}

impl DerefMut for Module {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.r#mod
    }
}

impl Module {
    pub fn insert(&mut self, name: String, ty: Metadata) {
        let syn_ty = syn::parse_str::<Type>(&name).unwrap();

        match syn_ty {
            Type::Path(TypePath {
                path: Path { segments, .. },
                ..
            }) => {
                let mut entry = self
                    .entry(segments[0].ident.to_string())
                    .or_insert_with(|| Either::Left(Self::default()));
                for s in segments.iter().take(segments.len() - 1).skip(1) {
                    entry = entry
                        .as_mut()
                        .unwrap_left()
                        .entry(s.ident.to_string())
                        .or_insert_with(|| Either::Left(Self::default()))
                }
                entry
                    .as_mut()
                    .unwrap_left()
                    .entry(segments.last().unwrap().ident.to_string())
                    .or_insert_with(|| Either::Right(ty));
            }
            Type::Array(_) | Type::Tuple(_) => drop(self.r#mod.insert(name, Either::Right(ty))),

            _ => (),
        }
    }

    fn write_meta(f: &mut fs::File, name: String, ty: Metadata) -> Result<()> {
        match ty {
            Metadata::Struct(s) => {
                let s = StructClass::from_meta(name, s);
                writeln!(f, "{}", s)?;
            }
            Metadata::TupleStruct(s) => {
                let s = UnnamedStructClass::from_meta(name, s);
                writeln!(f, "{}", s)?;
            }
            Metadata::Enum(e) => {
                let e = EnumClass::from_meta(name, e);
                writeln!(f, "{}", e)?;
            }
            Metadata::Int(_)
            | Metadata::FixedPoint(_)
            | Metadata::Vec(_)
            | Metadata::Map(_)
            | Metadata::Bool
            | Metadata::Array(_)
            | Metadata::Result(_)
            | Metadata::Option(_)
            | Metadata::String => (),
        }
        Ok(())
    }

    fn write_dir_int(&self, dir: &std::path::Path, r#in: &ModulePath) -> Result<()> {
        fs::create_dir_all(&dir).wrap_err("Failed to create directory for module")?;

        let f = dir.join("__init__.py");
        let mut f = fs::File::create(f).wrap_err("Failed to create __init__.py file")?;

        let (module, meta): (Vec<_>, Vec<_>) = self.r#mod.iter().partition(|(_, v)| v.is_left());

        if r#in.mods.is_empty() {
            writeln!(f, "from ..iroha2 import *")?;
        }
        writeln!(
            f,
            "from .{}rust import Enum, Struct, Tuple, Dict",
            ".".repeat(r#in.mods.len())
        )?;

        for (name, ty) in meta {
            let ty = ty.as_ref().right().unwrap();
            Self::write_meta(&mut f, name.clone(), ty.clone())
                .wrap_err_with(|| eyre!("Failed to write metadata for type {}", name))?;
        }
        drop(f);

        for (name, module) in module {
            let module = module.as_ref().left().unwrap();
            module
                .write_dir_int(&dir.join(name), &r#in.clone().add(name.clone()))
                .wrap_err_with(|| eyre!("Failed to write module {}", name))?;
        }

        Ok(())
    }

    pub fn write_dir(&self, dir: impl AsRef<std::path::Path>) -> Result<()> {
        self.write_dir_int(dir.as_ref(), &ModulePath::default())
    }
}

impl FromIterator<(String, Metadata)> for Module {
    fn from_iter<T: IntoIterator<Item = (String, Metadata)>>(iter: T) -> Self {
        let mut new = Self::default();
        for (k, v) in iter {
            new.insert(k, v);
        }
        new
    }
}
