#[macro_export]
macro_rules! mirror_fieldless_enum {
    (
        $(#[$outer:meta])*
        $name:ty;
        $($field:ident),*
    ) => {
        paste::paste! {
            #[pyclass(rename_all = "UPPERCASE", name = "" $name "")]
            #[derive(Clone, Copy, Debug)]
            $(#[$outer])*
            enum [<Py $name>] {
                $($field),*
            }

            impl From<$name> for [<Py $name>] {
                fn from(value: $name) -> Self {
                    match value {
                        $(
                            $name::$field => Self::$field
                        ),*
                    }
                }
            }

            impl Into<$name> for [<Py $name>] {
                fn into(self) -> $name {
                    match self {
                        $(
                            Self::$field => $name::$field
                        ),*
                    }
                }
            }
        }
    };
}

#[macro_export]
macro_rules! mirror_struct {
    (
        $(#[$outer:meta])*
        $name:ty
    ) => {
        paste::paste! {
            #[pyclass(name = "" $name "")]
            #[derive(Clone, derive_more::From, derive_more::Into, derive_more::Deref)]
            $(#[$outer])*
            pub struct [<Py $name>](pub $name);

            impl crate::data_model::PyMirror for $name {
                type Mirror = [<Py $name>];

                fn mirror(self) -> PyResult<Self::Mirror> {
                    Ok([<Py $name>](self))
                }
            }

            #[pymethods]
            impl [<Py $name>] {
                fn __repr__(&self) -> String {
                    format!("{:?}", self.0)
                }

                fn __str__(&self) -> String {
                    format!("{}", self.0)
                }
            }
        }
    };
}
