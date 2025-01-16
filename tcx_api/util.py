from enum import StrEnum, EnumMeta, auto


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


# Function to create a dynamic enum class
def create_enum_from_model(model_class):
    # Extract field names from the model class
    field_names = model_class.__annotations__.keys()

    # Create a new TcxStrEnum
    return TcxStrEnum(model_class.__name__ + "Properties", {field_name: auto() for field_name in field_names})