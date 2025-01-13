import os
import csv
from abc import ABC, abstractmethod
from app.mapping import CSVMapping
from typing import Optional, List
from tcx_api.components.schemas.pbx import Group, User
from sync.schema import CSVUser
from pydantic import TypeAdapter
from sync.logging import SyncLogger, LogLevel
from app.util import initialize_or_get_user_config_file

class SyncSourceStrategy(ABC):
    @property
    @abstractmethod
    def mapping(self): ...

    def __init__(self, logger: SyncLogger):
        self.logger = logger

    @abstractmethod
    def initialize(self) -> None: ...

    @abstractmethod
    def get_source_users(self) -> Optional[list[User]]: ...

    @abstractmethod
    def get_source_groups(self) -> Optional[list[Group]]: ...

    @abstractmethod
    def get_user_update_fields(self) -> list: ...


class SyncCSV(SyncSourceStrategy):
    @property
    def mapping(self):
        return self._mapping

    @mapping.setter
    def mapping(self, value):
        self._mapping = value

    def initialize(self):
        self.logger.log(LogLevel.INFO, "Initializing CSV Source")
        self.logger.log(LogLevel.INFO, "Loading CSV Mapping")
        self.mapping = CSVMapping(mapping_file_path=initialize_or_get_user_config_file("3cx_sync", "3cx_sync", "conf", "csv_mapping.json"))
        self.mapping.initialize()
        CSVUser.set_comparison_properties(self.mapping.get("Extension", {}).get("Update", []))
        
        self.logger.log(LogLevel.INFO, "CSV Mapping Loaded")

    def get_source_users(self) -> Optional[List[User]]:
        user_data = list()
        self.logger.log(LogLevel.INFO, "Loading CSV User Data")
        csv_data_path = self.mapping.get("Extension", {}).get("Path", "")
        if not os.path.isfile(csv_data_path):
            self.logger.log(
                LogLevel.INFO, f"Unable to find file at: {csv_data_path}"
                )
            raise (FileNotFoundError)

        with open(csv_data_path) as csv_file:
            csv_reader = csv.reader(csv_file)
            user_mapping = self.mapping.get("Extension").get("New")
            headers = next(csv_reader)

            for row in csv_reader:
                row_dict = dict(zip(headers, row))
                user_dict = {
                    key: row_dict[value]
                    for key, value in user_mapping.items()
                    if value in row_dict
                }
                if user_dict["Enabled"] == "0":
                    user_dict["HotdeskingAssignment"] = ""
                user_data.append(user_dict)
        csv_user_list = TypeAdapter(List[CSVUser]).validate_python(user_data)
        self.logger.log(
            LogLevel.INFO, f"Loaded {len(csv_user_list)} Users from CSV File"
            )
        return csv_user_list

    def get_user_update_fields(self) -> list:
        return self.mapping["Extension"]["Update"]

    def get_source_groups(self):
        return None
