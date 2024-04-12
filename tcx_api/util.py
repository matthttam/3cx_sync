from enum import StrEnum, EnumMeta
from typing import Any, Callable, TypeVar


class TcxStrEnumMeta(EnumMeta):
    # StrEnum from 3CX can contain teh word None which we can't use in Python
    # So, we use NONE instead. This metaclass makes it so looking for None
    # returns the value for NONE instead.
    def __getitem__(self, name):
        if name == "None":
            name = "NONE"
        return super().__getitem__(name).value


class TcxStrEnum(StrEnum, metaclass=TcxStrEnumMeta):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        if name == "NONE":
            return "None"
        return name


class Util:
    T = TypeVar("T")

    @staticmethod
    def instanciate_object(var: Any, object_class: Callable[[type], T]) -> T | None:
        return (
            var
            if isinstance(var, object_class)
            else object_class(**var) if isinstance(var, dict) else None
        )

    @staticmethod
    def instanciate_list_of_objects(
        var: list, object_class: Callable[[type], T]
    ) -> list[T] | list:
        return (
            var
            if var is not None and all(isinstance(v, object_class) for v in var)
            else [object_class(**v) for v in var] if var else list()
        )

    @staticmethod
    def instanciate_str_enum(var: str, enum_var: TcxStrEnum) -> str | None:
        # ([enum_var[v] for v in var] if var else None)
        return enum_var[var] if var else None

    @staticmethod
    def instanciate_list_of_str_enum(
        var: list, enum_var: TcxStrEnum
    ) -> list[str] | list:
        return (
            var
            if var is not None and all(isinstance(v, enum_var) for v in var)
            else [enum_var[v] for v in var] if var else list()
        )
