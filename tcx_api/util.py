from enum import StrEnum, EnumMeta


class TcxStrEnumMeta(EnumMeta):
    # Map special string values to their Python equivalents
    SPECIAL_STRING_MAP = {"None": "NONE", "-INF": "NEGATIVE_INF"}
    SPECIAL_STRING_MAP_INV = {v: k for k, v in SPECIAL_STRING_MAP.items()}

    def __getitem__(self, name):
        name = self.SPECIAL_STRING_MAP.get(name, name)
        return super().__getitem__(name).value


class TcxStrEnum(StrEnum, metaclass=TcxStrEnumMeta):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return TcxStrEnumMeta.SPECIAL_STRING_MAP_INV.get(name, name)
