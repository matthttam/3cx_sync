import os
import json
from collections import UserDict
from typing import Any


class CSVMapping(UserDict):

    @property
    def mapping_file_path(self):
        return os.path.join(os.getcwd(), "conf", "csv_mapping.json")

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def __setitem__(self, key: Any, item: Any) -> None:
        return super().__setitem__(key, item)

    def __getitem__(self, key: Any) -> Any:
        return super().__getitem__(key)

    def load_mapping_config(self):
        self.validate_file_exists()
        self.validate_file_not_empty()
        self.load_mapping_dict()

    def validate_file_exists(self):
        if not os.path.isfile(self.mapping_file_path):
            self.initialize_mapping_file()

    def validate_file_not_empty(self):
        if os.stat(self.mapping_file_path).st_size == 0:
            self.initialize_mapping_file()

    def load_mapping_dict(self):
        with open(self.mapping_file_path, "r") as mapping_file:
            mapping_config = json.load(mapping_file)
            mapping_file.close()
            self.update(mapping_config)

    def initialize_mapping_file(self):
        with open(self.mapping_file_path, "w") as mapping_file:
            mapping_file.write("{}")
            mapping_file.close()

    def save_mapping_config(self):
        with open(self.mapping_file_path, "w") as mapping_file:
            json.dump(self.__dict__["data"], mapping_file)
        mapping_file.close()

    def inverted_mapping(self, mapping: dict):
        return {v: k for k, v in mapping.items()}
