import os
import json
from collections import UserDict
from typing import Any


class CSVMapping(UserDict):

    @property
    def mapping_file_path(self):
        return os.path.join(os.getcwd(), "conf", "csv_mapping.json")

    def __init__(self, *args, suppress_load=False, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if not suppress_load:
            self.load()

    def __setitem__(self, key: Any, item: Any) -> None:
        return super().__setitem__(key, item)

    def __getitem__(self, key: Any) -> Any:
        return super().__getitem__(key)

    def load(self):
        if not self.load_mapping_config():
            self.initialize_mapping_file()

    def load_mapping_config(self) -> bool:
        if not os.path.exists(self.mapping_file_path):
            return False

        if os.stat(self.mapping_file_path).st_size == 0:
            return False

        self.load_mapping_file()
        return True

    def load_mapping_file(self):
        with open(self.mapping_file_path, "r") as mapping_file:
            mapping_config = json.load(mapping_file)
            mapping_file.close()
            self.update(mapping_config)

    def initialize_mapping_file(self):
        with open(self.mapping_file_path, "w") as mapping_file:
            mapping_file.write("{}")
            mapping_file.close()

    def save(self):
        self.save_mapping_file()

    def save_mapping_file(self):
        with open(self.mapping_file_path, "w") as mapping_file:
            json.dump(self.__dict__["data"], mapping_file)
            mapping_file.close()
