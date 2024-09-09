from typing import Any
from pydantic import BaseModel, ConfigDict


class Schema(BaseModel):
    model_config = ConfigDict(populate_by_name=True, use_enum_values=True)

    def model_dump(self, **kwargs) -> dict[str, Any]:
        # Set default options for model_dump
        default_options = {
            "exclude_unset": True,
            "exclude_none": True,
            "serialize_as_any": True,
            "by_alias": True
        }

        # Update with any user-provided options
        default_options.update(kwargs)
        # Call the original model_dump with the updated options
        return super().model_dump(**default_options)
