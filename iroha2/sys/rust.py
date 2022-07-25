# Export
from typing import NamedTuple
import collections
import dataclasses
from importlib import import_module
from ..iroha2 import Dict, List

ClassPath = str


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

    return obj.to_rust() if hasattr(obj, 'to_rust') else obj


def get_class(path) -> type:
    if isinstance(path, type):
        return path
    path = path.split('.')
    name = path[-1]
    import_path = '.' + '.'.join(path[:-1])
    mod = import_module(import_path, package='iroha2.sys')
    return getattr(mod, name)


class _Enum(type):

    @staticmethod
    def _make_class(variants):

        class RustEnum:
            __variants = None

            @classmethod
            def _variants(cls):
                if not cls.__variants:
                    cls.__variants = {k: get_class(v) for k, v in variants}
                return cls.__variants

            def _from_value(self, value):
                for variant, ty in self._variants().items():
                    if isinstance(value, ty):
                        self.variant = variant
                        self.value = value
                        return

                raise TypeError(f"Unknown type for enum: {value}")

            def __init__(self, value, variant=None):
                if variant is None:
                    self._from_value(value)
                else:
                    self.variant = variant
                    self.value = value

            def to_rust(self) -> dict:
                return {self.variant: to_rust(self.value)}

        for var, ty in variants:

            def constructor_meta(value, var, ty):
                if isinstance(ty, str):
                    ty = get_class(ty)

                if not isinstance(value, ty):
                    value = ty(value)
                return RustEnum(value, variant=var)

            # Type here might be a string also
            if ty == type(None):
                # https://stackoverflow.com/questions/2295290/what-do-lambda-function-closures-capture
                constructor = (
                    lambda var: lambda: RustEnum(None, variant=var))(var)
            else:

                constructor = (
                    lambda var, ty: lambda v: constructor_meta(v, var, ty))(
                        var, ty)

            setattr(RustEnum, var, staticmethod(constructor))

        return RustEnum

    def __getitem__(
        cls,
        variants,
    ) -> type:
        if isinstance(variants, tuple) and isinstance(variants[0], str):
            variants = [variants]

        return cls.__class__._make_class(variants)


class Enum(metaclass=_Enum):
    pass


def make_tuple(name, fields=None):
    if fields is None:
        fields = []
    cls = NamedTuple(name, [(f"f{i}", typ) for i, typ in enumerate(fields)])
    cls.to_rust = lambda tup: tuple(to_rust(i) for i in tup)
    return cls


def make_struct(name, fields):

    def struct_to_rust(s):
        return {k: to_rust(v) for k, v in dataclasses.asdict(s).items()}

    return dataclasses.make_dataclass(name,
                                      fields,
                                      namespace={"to_rust": struct_to_rust})
