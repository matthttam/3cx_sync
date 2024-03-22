import os
import json
from collections import UserDict, defaultdict
from typing import Any


class CSVMapping(UserDict):

    @property
    def mapping_file_path(self):
        return os.path.join(os.getcwd(), "conf", "csv_mapping.json")

    def __init__(
        self,
    ) -> None:
        super().__init__(self.get_mapping())

    def __setitem__(self, key: Any, item: Any) -> None:
        return super().__setitem__(key, item)

    def __getitem__(self, key: Any) -> Any:
        return super().__getitem__(key)

    def get_mapping(self):
        if not os.path.isfile(self.mapping_file_path):
            self.initialize_mapping_file()
        if os.stat(self.mapping_file_path).st_size == 0:
            self.initialize_mapping_file()
        with open(self.mapping_file_path, "r") as mapping_file:
            mapping_config = json.load(mapping_file)
            mapping_file.close()
            return mapping_config

    def initialize_mapping_file(self):
        with open(self.mapping_file_path, "w") as mapping_file:
            mapping_file.write("{}")
            mapping_file.close()

    def save_mapping_config(self):
        with open(self.mapping_file_path, "w") as mapping_file:
            json.dump(self.__dict__["data"], mapping_file)
        mapping_file.close()
