import json
from typing import Type

from pydantic import BaseModel, Field

from app.util import initialize_or_get_user_config_path
from abc import ABC, abstractmethod
from copy import deepcopy
from pathlib import Path

class MappingField(BaseModel, ABC):
    ...

class MappingModel(BaseModel, ABC):
    mappings: list[MappingField] = Field(default_factory=list, description="List of MappingField inherited instances")
    default_mappings: list[MappingField] = Field(default_factory=list, description="List of MappingFIeld inherited instances set if no other config loadeds")

class JSONMappingConfig(ABC):
    DEFAULT_FILENAME: str
    MAPPING_MODEL: Type[MappingModel]  # This will be overridden by subclasses

    def __init__(self, config_path: Path = None) -> None:
        self.config_path = (
            config_path or initialize_or_get_user_config_path("3cx_sync", "3cx_sync", "conf")
        ) / self.DEFAULT_FILENAME

        self.model = self.load()  # Load existing config or use default
        self.set_original_config()

    def __init_subclass__(cls, **kwargs):
        """Ensure subclasses set MAPPING_MODEL."""
        super().__init_subclass__(**kwargs)
        if not hasattr(cls, "MAPPING_MODEL") or cls.MAPPING_MODEL is None:
            raise TypeError(f"{cls.__name__} must define a valid MAPPING_MODEL.")
        
        if not hasattr(cls, "DEFAULT_FILENAME") or not isinstance(cls.DEFAULT_FILENAME, str) or not cls.DEFAULT_FILENAME:
            raise TypeError(f"{cls.__name__ } must define a valid DEFAULT_FILENAME")

    @property
    def is_dirty(self) -> bool:
        return self.original_config != self.model.model_dump()

    def load_defaults(self) -> None:
        """Reset to default values."""
        self.model = self.MAPPING_MODEL()  # Create a fresh default instance
        self.set_original_config()

    def load(self) -> BaseModel:
        """Load configuration from file or return defaults."""
        if self.config_path.exists():
            data = json.loads(self.config_path.read_text())
            return self.MAPPING_MODEL(**data)  # Validate and create model instance
        return self.MAPPING_MODEL()  # Default values if file is missing

    def save(self):
        """Save model to JSON file."""
        with open(self.config_path, "w") as mapping_file:
            json.dump(self.model.model_dump(), mapping_file, indent=4)
        self.set_original_config()

    def save_to(self, path: str):
        """Save model to a specified path."""
        file_path = Path(path) / self.DEFAULT_FILENAME
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(json.dumps(self.mapping_model.model_dump(), indent=4))
        

    def set_original_config(self):
        """Track the original config for change detection."""
        self.original_config = deepcopy(self.model.model_dump())

    def update(self, **kwargs):
        """Update model fields dynamically while maintaining type safety."""
        self.model = self.model.model_copy(update=kwargs)
