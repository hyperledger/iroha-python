# Export
from importlib import import_module
from .iroha2 import Dict

ClassPath = str


def all(it):
    for i in it:
        if not i:
            return False
    return True


def to_rust(obj):
    if isinstance(obj, list):
        return [to_rust(obj) for i in obj]
    if isinstance(obj, tuple):
        return (to_rust(obj) for i in obj)
    if isinstance(obj, dict):
        return {k: to_rust(v) for k, v in obj}

    return obj.to_rust() if hasattr(obj, 'to_rust') else obj


def get_class(path) -> type:
    if isinstance(path, type):
        return path
    path = path.split('.')
    name = path[-1]
    import_path = '.' + '.'.join(path[:-1])
    mod = import_module(import_path, package='iroha2.sys')
    return getattr(mod, name)


class _Tuple(type):
    def _make_class(fields):
        class RustTuple:
            __fields = None

            @staticmethod
            def _fields():
                if not RustTuple.__fields:
                    RustTuple.__fields = [get_class(f) for f in fields]
                return RustTuple.__fields

            def __init__(self, *args):
                if not all(
                        isinstance(a, f)
                        for a, f in zip(args, self._fields())):
                    raise ValueError(args)
                self.items = args

            def to_rust(self) -> tuple:
                return tuple(to_rust(i) for i in self.items)

        return RustTuple

    def __getitem__(
        cls,
        fields,
    ) -> type:
        if isinstance(fields, (ClassPath, type)):
            fields = [fields]

        return cls.__class__._make_class(fields)


class Tuple(metaclass=_Tuple):
    pass


class _Enum(type):
    def _make_class(variants):
        class RustEnum:
            __variants = None

            @staticmethod
            def _variants():
                if not RustEnum.__variants:
                    RustEnum.__variants = {
                        k: get_class(v)
                        for k, v in variants
                    }
                return RustEnum.__variants

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
            if ty == type(None):
                constructor = lambda: RustEnum(None, variant=var)
            else:
                # https://stackoverflow.com/questions/2295290/what-do-lambda-function-closures-capture
                constructor = (
                    lambda var: lambda v: RustEnum(v, variant=var))(var)

            constructor = staticmethod(constructor)
            setattr(RustEnum, var, constructor)

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


class _Struct(type):
    def _make_class(fields):
        class RustStruct:
            __fields = None

            @staticmethod
            def _fields():
                if not RustStruct.__fields:
                    RustStruct.__fields = [(k, get_class(v))
                                           for k, v in fields]
                return RustStruct.__fields

            def _from_args(self, *args):
                for v, (k, _) in zip(args, self._fields()):
                    self.items[k] = v

            def _from_kwargs(self, **kwargs):
                for k, v in kwargs.items():
                    self.items[k] = v

            def __init__(self, *args, **kwargs):
                self.items = {}

                if len(args) != 0:
                    self._from_args(*args)
                if len(kwargs) != 0:
                    self._from_kwargs(**kwargs)

                if len(self.items) != len(self._fields()):
                    raise ValueError("Some fields are missing")

            def to_rust(self) -> tuple:
                return {k: to_rust(v) for k, v in self.items.items()}

        return RustStruct

    def __getitem__(
        cls,
        fields,
    ) -> type:
        if isinstance(fields, tuple) and isinstance(fields[0], str):
            fields = [fields]

        return cls.__class__._make_class(fields)


class Struct(metaclass=_Struct):
    pass
