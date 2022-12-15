# Export
import abc
from collections.abc import Iterable
import typing
import types
from typing import NamedTuple, Tuple, Union, TypeVar, Optional
from functools import partial
import enum
import collections
import dataclasses
from importlib import import_module
from ..iroha2 import Dict, List
import inspect

ClassPath = str


def get_caller() -> types.ModuleType:
    """
    Returns reference to the calling module
    """
    stack = inspect.stack()
    for frame_info in stack:
        mod = inspect.getmodule(frame_info.frame)
        if mod is not None and mod.__name__ != __name__:
            return mod
    return None


class SelfResolvingTypeVar(typing.TypeVar, _root=True):
    """
    Hacky workaround type for dependency cycles caused by self-referencing types.
    """

    def evaluate(self):
        """
        Evaluate the underlying TypeVar to the actual type.
        """
        return self.__bound__._evaluate(self.caller_module.__dict__, globals(),
                                        set())

    def resolve(self):
        """
        Overwrite self with the actual type
        """
        self = self.evaluate()

    def __call__(self, args, **kvargs):
        return self.evaluate()(args, kvargs)

    def __init__(self, *args, **kvargs):
        super().__init__(*args, **kvargs)

        caller_module = get_caller()

        if not hasattr(caller_module, "__typevars_to_resolve"):
            caller_module.__typevars_to_resolve = []
        caller_module.__typevars_to_resolve.append(self)

        self.caller_module = caller_module

    @classmethod
    def resolve_all(_):
        """
        Resolves all self-referencing placeholders in the calling module,
        overwriting them with actual types.
        Should be called at the end of the module.
        """
        caller_module = get_caller()
        for tv in getattr(caller_module, "__typevars_to_resolve", []):
            tv.resolve()


def query(*path):

    class IntoInner:

        @staticmethod
        def parse_output(out):
            for p in path:
                out = out[p]
            return out

    return IntoInner


def to_rust(obj):
    if isinstance(obj, list):
        return [to_rust(i) for i in obj]

    if isinstance(obj, tuple):
        if len(obj) == 0:
            return None
        else:
            return tuple(to_rust(i) for i in obj)

    if isinstance(obj, dict):
        return {k: to_rust(v) for k, v in obj.items()}

    if hasattr(obj, "to_rust"):
        return obj.to_rust()

    return obj


def from_rust(obj, cls):
    if isinstance(cls, typing.GenericAlias):
        if not isinstance(obj, Iterable)\
           and not isinstance(obj, List):
            raise TypeError
        contents_type = get_class(cls.__args__[0])
        return [from_rust(i, contents_type) for i in obj]

    if hasattr(cls, 'from_rust'):
        obj = cls.from_rust(obj)
    if hasattr(cls, '_into_wrapped'):
        obj = cls._into_wrapped(obj)
    return obj


def get_class(path: Union[type, str]) -> type:
    if isinstance(path, type):
        return path
    path = path.split('.')
    name = path[-1]
    import_path = '.' + '.'.join(path[:-1])
    try:
        mod = import_module(import_path, package='iroha2.sys')
        return getattr(mod, name)
    except AttributeError:
        # Forward reference, not yet in scope
        # Return symbolic variable to be resolved later
        return SelfResolvingTypeVar(name, bound=f'{name}')


def make_enum_variant(base, variant_name, variant_type):

    def repr_enum_variant(self):
        return f"{base.__name__}.{variant_name}({repr(self._value)})"

    def enum_variant_to_rust(self):
        encoded = to_rust(self._value)
        return {variant_name: encoded}

    return type(f"{base.__name__}.{variant_name}", (base, ), {
        "to_rust": enum_variant_to_rust,
        "__repr__": repr_enum_variant,
    })


def make_enum(enum_name: str, variants: [Tuple[str, type]],
              typs: TypeVar) -> type:
    """
    Creates a type corresponding to rust Enum.
    Actually creates a base enum type and a type
    corresponding to each of the variants, available as 
    `EnumName.VariantName`. Base enum type can never be 
    instantiated, calling it directly tries to guess
    the variant and instantiate corresponding type,
    if the value passed to constructor is unambiguous.
    E.g. for a fictional enum `Value[Integer, String]`
    `Value(8)` will return `Value.Integer(8)`.
    """

    typemap = {name: typ for name, typ in variants}

    # __new__ must know the base enum type
    def make_new(base):

        def new(cls, value: Optional[typs] = None, name: Optional[str] = None):
            # We should never construct base enum object directly,
            # always a subclass of representing a concrete variant
            if cls == base:
                if name is None:
                    for var_name in typemap:

                        # Resolve forward references
                        if isinstance(typemap[var_name], SelfResolvingTypeVar):
                            typemap[var_name] = typemap[var_name].evaluate()

                        # Found variant of suitable type
                        if isinstance(value, typemap[var_name]):
                            # Multiple variants of suitable type exist,
                            # invocation is ambiguous without specifying
                            # variant
                            if name is not None:
                                raise ValueError(
                                    f"{base.__name__} instantiated with ambiguous type: {value}"
                                )
                            name = var_name

                    # No variant with such type exists
                    if name is None:
                        raise TypeError

                cls = getattr(base, name)

            # Instantiate variant-type object
            return super(base, cls).__new__(cls)

        return new

    def init_enum(self, value: typs = None, name=None):
        self._value = value

    def enum_from_rust(cls, obj):
        if isinstance(obj, dict):
            name = list(obj.keys())[0]
            value = obj[name]
            return cls(from_rust(value, typemap[name]), name)
        elif isinstance(obj, str):
            return cls(None, obj)
        else:
            raise ValueError

    # Dereference to contained value
    def get_value_attr(self, name):
        return getattr(self._value, name)

    enum_type = type(
        enum_name,
        (abc.ABC, ),
        {
            "__init__": init_enum,
            "__getattr__": get_value_attr,
            "from_rust": classmethod(enum_from_rust),
            # to_rust is defined on variant subclasses
        })

    # These methods need to be generated already
    # having the base enum type.
    setattr(enum_type, "__new__", make_new(enum_type))
    for name, typ in variants:
        setattr(enum_type, name, make_enum_variant(enum_type, name, typ))

    return enum_type


def make_tuple(name, fields=None):
    """
    Create an analogue to a rust typle.
    """

    if fields is None:
        fields = []

    cls = NamedTuple(name, [(f"f{i}", typ) for i, typ in enumerate(fields)])
    cls.to_rust = lambda tup: tuple(to_rust(i) for i in tup)
    return cls


def make_struct(structname, fields):
    """
    Create an analogue to a rust typle.
    """

    def struct_to_rust(s):
        # `asdict` doesn't work here since it relies on deepcopy, which isn't
        # available for PyO3 structs.
        return {field: to_rust(getattr(s, field)) for (field, _) in fields}

    def struct_from_rust(cls, obj):
        args = []

        for (argname, argtype) in fields:
            argtype = get_class(argtype)
            try:
                # Special case, since those are flattened
                # TODO: requires changes to iroha schema
                # to handle properly
                if structname == "EvaluatesTo" or structname == "Metadata":
                    arg = obj
                else:
                    arg = obj[argname]
            except KeyError:
                raise KeyError(f"Error deserializing {structname}: "
                               f"no key for field {argname}")
            except TypeError:
                arg = obj

            args.append(from_rust(arg, argtype))

        return cls(*args)

    return dataclasses.make_dataclass(structname,
                                      fields,
                                      namespace={
                                          "to_rust":
                                          struct_to_rust,
                                          "from_rust":
                                          classmethod(struct_from_rust),
                                      })


def wrapper(base):
    """
    This function is a decorator that marks class as
    a manual wrapper for a code-generated counterpart.

    This allows to automatically target wrapping classes
    when deserializing from json.

    Wrapping class must be a subclass of the class being wrapped.

    For example, this is how one would wrap auto-generated Account class
    to add some convenience methods:
    ```python
    from ...sys.iroha_data_model.account import Account as _Account

    @wrapper(_Account)
    class Account(_Account):

       # ...

       def __repr__(self):
         # ...some nicer implementation

       def some_nice_transform(self):
         # ...
    ```

    Without `wrapper` user would be faced with base
    Account class when receiving data from iroha client.
    """

    def decorate(subclass):
        if not issubclass(subclass, base):
            raise TypeError("Wrapping class isn't a subclass of wrapped class")

        def into_wrapped(self):
            self.__class__ = subclass

        base._into_wrapped = into_wrapped
        return subclass

    return decorate
