use std::convert::TryFrom;
use std::fmt;

use iroha_schema::prelude::*;
use syn::{GenericArgument, Path, PathArguments, Type, TypeArray, TypePath, TypeTuple};

/// Type which represents python type for code gen
#[derive(PartialEq, Eq, Clone, Hash, Debug)]
pub struct PyType(pub String);

/// Module path type. For both rust and python
#[derive(PartialEq, Eq, Clone, Hash, Debug, Default)]
pub struct ModulePath {
    /// individual module parts
    pub mods: Vec<String>,
}

#[derive(PartialEq, Eq, Clone, Hash, Debug)]
pub struct RustType {
    /// in module
    module: ModulePath,
    /// With identifier
    ident: String,
    /// With generics
    generics: Vec<RustType>,

    /// Syn type (for a record)
    ty: Type,
}

#[derive(PartialEq, Eq, Clone, Debug)]
pub struct StructClass {
    fields: Vec<(String, PyType)>,
    name: String,
}

#[derive(PartialEq, Eq, Clone, Debug)]
pub struct UnnamedStructClass {
    fields: Vec<PyType>,
    name: String,
}

#[derive(PartialEq, Eq, Clone, Debug)]
pub struct EnumClass {
    variants: Vec<(String, PyType)>,
    name: String,
}

impl From<String> for RustType {
    fn from(ty: String) -> Self {
        syn::parse_str::<Type>(&ty).unwrap().into()
    }
}

impl From<Type> for RustType {
    fn from(ty: Type) -> Self {
        fn get_args(args: &PathArguments) -> Vec<Type> {
            match args {
                PathArguments::AngleBracketed(args) => args.args.iter(),
                _ => return vec![],
            }
            .map(|arg| {
                if let GenericArgument::Type(arg) = arg {
                    arg.clone()
                } else {
                    unreachable!()
                }
            })
            .collect()
        }

        match &ty {
            Type::Path(TypePath {
                path: Path { segments, .. },
                ..
            }) => {
                let path = segments
                    .iter()
                    .map(|seg| seg.ident.to_string())
                    .collect::<Vec<_>>();
                let path = path[..path.len() - 1].to_vec();
                let module = ModulePath { mods: path };
                let ident = segments.last().unwrap().ident.to_string();
                let generics = get_args(&segments.last().unwrap().arguments)
                    .into_iter()
                    .map(Self::from)
                    .collect();

                Self {
                    module,
                    ident,
                    generics,
                    ty,
                }
            }

            Type::Array(TypeArray {
                elem,
                // Length is not used in python typing.
                len: _len,
                ..
            }) => Self {
                module: Default::default(),
                ident: "[]".to_owned(),
                generics: vec![Self::from(*elem.clone())],
                ty,
            },
            Type::Tuple(TypeTuple { elems, .. }) => Self {
                module: Default::default(),
                ident: "()".to_owned(),
                generics: elems.iter().cloned().map(Self::from).collect::<Vec<_>>(),
                ty,
            },

            _ => todo!("Should not be such types within python library"),
        }
    }
}

impl ModulePath {
    pub fn add(mut self, name: String) -> Self {
        self.mods.push(name);
        self
    }
}

impl TryFrom<Type> for ModulePath {
    type Error = ();
    fn try_from(ty: Type) -> Result<Self, ()> {
        let segments = match ty {
            Type::Path(TypePath {
                path: Path { segments, .. },
                ..
            }) if segments.len() > 1 => segments,
            _ => return Err(()),
        };
        let segments = segments.iter().collect::<Vec<_>>();
        let mods = segments[..segments.len() - 1]
            .iter()
            .map(|seg| seg.ident.to_string())
            .collect();
        Ok(Self { mods })
    }
}

impl From<RustType> for PyType {
    fn from(ty: RustType) -> Self {
        match ty.ident.as_ref() {
            "Option" => return Self::from(ty.generics[0].clone()),
            "Vec" | "[]" => {
                #[cfg(feature = "typing")]
                return Self(format!("list[{}]", Self::from(ty.generics[0].clone())));
                #[cfg(not(feature = "typing"))]
                return Self("list".to_owned());
            }
            "BTreeMap" | "HashMap" => return Self("Dict".to_owned()),

            "u8" | "u16" | "u32" | "u64" | "u128" | "i8" | "i16" | "i32" | "i64" | "i128" => {
                return Self("int".to_owned())
            }
            "String" => return Self("str".to_owned()),
            "bool" => return Self("bool".to_owned()),
            "()" if ty.generics.is_empty() => return Self("type(None)".to_owned()),
            "()" => {
                return Self(format!(
                    "({})",
                    ty.generics
                        .into_iter()
                        .map(Self::from)
                        .map(|ty| ty.to_string())
                        .collect::<Vec<_>>()
                        .join(", ")
                ))
            }
            _ => (),
        }

        let path = ty
            .module
            .mods
            .into_iter()
            .chain(std::iter::once(ty.ident))
            .collect::<Vec<_>>()
            .join(".");
        Self(format!("\"{}\"", path))
    }
}

impl From<String> for PyType {
    fn from(ty: String) -> Self {
        RustType::from(ty).into()
    }
}

impl fmt::Display for PyType {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.0)
    }
}

impl fmt::Display for ModulePath {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.mods.join("."))
    }
}

impl fmt::Display for StructClass {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let mut fields = self
            .fields
            .iter()
            .map(|(name, ty)| format!("(\"{}\", {})", name, ty))
            .collect::<Vec<_>>()
            .join(", ");

        if fields.is_empty() {
            fields = "()".to_owned();
        }

        writeln!(f, "{} = Struct[{}]", self.name, fields)
    }
}

impl fmt::Display for UnnamedStructClass {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let fields = self
            .fields
            .iter()
            .map(|a| a.0.clone())
            .collect::<Vec<_>>()
            .join(", ");

        if fields.is_empty() {
            return write!(f, "{} = Tuple[()]", self.name);
        }
        write!(f, "{} = Tuple[{}]", self.name, fields)
    }
}

impl fmt::Display for EnumClass {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let variants = self
            .variants
            .iter()
            .map(|(name, ty)| format!("(\"{}\", {})", name, ty))
            .collect::<Vec<_>>()
            .join(", ");
        write!(f, "{} = Enum[{}] ", self.name, variants)
    }
}

impl StructClass {
    pub fn from_meta(name: String, NamedFieldsMeta { declarations }: NamedFieldsMeta) -> Self {
        let (names, tys): (Vec<_>, Vec<_>) =
            declarations.into_iter().map(|d| (d.name, d.ty)).unzip();
        let tys = tys.into_iter().map(RustType::from).collect::<Vec<_>>();

        let tys = tys.into_iter().map(PyType::from).collect::<Vec<_>>();
        let fields = names.into_iter().zip(tys).collect::<Vec<_>>();

        Self { fields, name }
    }
}

impl EnumClass {
    pub fn from_meta(name: String, EnumMeta { variants }: EnumMeta) -> Self {
        let (names, tys): (Vec<_>, Vec<_>) = variants.into_iter().map(|d| (d.name, d.ty)).unzip();
        let tys = tys
            .into_iter()
            .map(|ty| {
                let ty: Option<&str> = ty.as_deref();
                syn::parse_str::<Type>(ty.unwrap_or("()")).unwrap()
            })
            .map(RustType::from)
            .collect::<Vec<_>>();

        let tys = tys.into_iter().map(PyType::from).collect::<Vec<_>>();
        let variants = names.into_iter().zip(tys).collect::<Vec<_>>();

        Self { variants, name }
    }
}

impl UnnamedStructClass {
    pub fn from_meta(name: String, UnnamedFieldsMeta { types }: UnnamedFieldsMeta) -> Self {
        let types = types.into_iter().map(RustType::from).collect::<Vec<_>>();
        let fields = types.into_iter().map(PyType::from).collect::<Vec<_>>();
        Self { fields, name }
    }
}
