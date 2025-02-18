import json

from pydantic import BaseModel

from app.util import initialize_or_get_user_config_path
from abc import ABC
from collections import UserDict
from copy import deepcopy
from pathlib import Path


class JSONMapping(UserDict, ABC):
    DEFAULT_FILENAME = ""
    DEFAULT_CONFIG = {}

    def __init__(self, config_path: Path = None) -> None:
        super().__init__()
        assert self.DEFAULT_FILENAME != ""
        assert self.DEFAULT_CONFIG != {}

        self.set_original_config()
        self.mapping_file_path = (
            config_path or initialize_or_get_user_config_path("3cx_sync", "3cx_sync", "conf")
        ) / self.DEFAULT_FILENAME

    def initialize(self):
        self.load_defaults()
        self.load() if self.mapping_file_path.exists() else None

    @property
    def is_dirty(self) -> bool:
        return self.original_config != self.data

    def load_defaults(self) -> None:
        self.update()

    def load(self) -> None:
        """Load configuration from the specified file."""
        with open(self.mapping_file_path, "r") as mapping_file:
            self.update(json.load(mapping_file))
        self.set_original_config()

    def save(self):
        with open(self.mapping_file_path, "w") as mapping_file:
            json.dump(self.data, mapping_file)
        self.set_original_config()

    def save_to(self, path: str):
        file_path = Path(path) / self.DEFAULT_FILENAME
        with file_path.open("w") as mapping_file:
            json.dump(self.data, mapping_file)

    def set_original_config(self):
        self.original_config = deepcopy(self.data)


class JSONMappingNew(ABC):
    DEFAULT_FILENAME = ""
    DEFAULT_MODEL = BaseModel  # This will be overridden by subclasses

    def __init__(self, config_path: Path = None) -> None:
        assert self.DEFAULT_FILENAME != "", "DEFAULT_FILENAME must be set in subclass"
        assert self.DEFAULT_MODEL != BaseModel, "DEFAULT_MODEL must be set in subclass"

        self.mapping_file_path = (
            config_path or initialize_or_get_user_config_path("3cx_sync", "3cx_sync", "conf")
        ) / self.DEFAULT_FILENAME

        self.model = self.load()  # Load existing config or use default
        self.set_original_config()

    def initialize(self):
        print("Delete initialize method of JSONMappingNew")

    @property
    def is_dirty(self) -> bool:
        return self.original_config != self.model.model_dump()

    def load_defaults(self) -> None:
        """Reset to default values."""
        self.model = self.DEFAULT_MODEL()  # Create a fresh default instance
        self.set_original_config()

    def load(self) -> BaseModel:
        """Load configuration from file or return defaults."""
        if self.mapping_file_path.exists():
            with open(self.mapping_file_path, "r") as mapping_file:
                data = json.load(mapping_file)
            return self.DEFAULT_MODEL(**data)  # Validate and create model instance
        return self.DEFAULT_MODEL()  # Default values if file is missing

    def save(self):
        """Save model to JSON file."""
        with open(self.mapping_file_path, "w") as mapping_file:
            json.dump(self.model.model_dump(), mapping_file, indent=4)
        self.set_original_config()

    def save_to(self, path: str):
        """Save model to a specified path."""
        file_path = Path(path) / self.DEFAULT_FILENAME
        with file_path.open("w") as mapping_file:
            json.dump(self.model.model_dump(), mapping_file, indent=4)

    def set_original_config(self):
        """Track the original config for change detection."""
        self.original_config = deepcopy(self.model.model_dump())

    def update(self, **kwargs):
        """Update model fields dynamically while maintaining type safety."""
        self.model = self.model.model_copy(update=kwargs)
