from sync.strategy.csv.mapping import ExtensionMappingConfig
from sync.logging import LogLevel, SyncLogger
from sync.schema import CSVUser
from sync.strategy.strategy import SyncSourceStrategy


from pydantic import TypeAdapter
from threecxapi.components.schemas.pbx import User


import csv
import os
from pathlib import Path


class SyncCSV(SyncSourceStrategy):
    config_path: Path = None

    def __init__(self, logger: SyncLogger, config_path: str = None):
        super().__init__(logger)
        self.config_path = Path(config_path).resolve() if config_path else None

    def initialize(self):
        self.logger.log(LogLevel.INFO, "Initializing CSV Source")
        self._load_extension_mapping_config()
        self._set_comparison_properties()

    @property
    def extension_mapping_config(self):
        return self._extension_mapping_config

    @extension_mapping_config.setter
    def extension_mapping_config(self, value):
        self._extension_mapping_config = value

    def _load_extension_mapping_config(self):
        self.logger.log(LogLevel.INFO, "Loading CSV Mapping")
        self.extension_mapping_config = ExtensionMappingConfig(self.config_path)
        self.logger.log(LogLevel.INFO, f"CSV Mapping Loaded from '{self.extension_mapping_config._config_path}'")

    def _set_comparison_properties(self):
        CSVUser.set_comparison_properties(self.extension_mapping_config.get_update_fields())
        self.logger.log(LogLevel.INFO, "Comparison Properties Set")

    def get_source_users(self) -> list[User] | None:
        self.logger.log(LogLevel.INFO, "Loading CSV User Data")
        csv_data_path = self._get_csv_data_path()
        user_data = self._parse_csv_file(csv_data_path)
        csv_user_list = self._validate_csv_users(user_data)
        self.logger.log(LogLevel.INFO, f"Loaded {len(csv_user_list)} Users from CSV File")
        return csv_user_list

    def _get_csv_data_path(self) -> Path:
        """Retrieve and validate the CSV data file path."""
        csv_data_path = self.extension_mapping_config.csv_path
        if not csv_data_path or not csv_data_path.is_file():
            self.logger.log(LogLevel.ERROR, f"Unable to find file at: {csv_data_path}")
            raise FileNotFoundError(f"CSV file not found at: {csv_data_path}")
        return csv_data_path


    def _parse_csv_file(self, csv_data_path: str) -> list[dict]:
        """Parse the CSV file and return a list of user dictionaries."""
        user_data = []
        with open(csv_data_path) as csv_file:
            csv_reader = csv.reader(csv_file)
            headers = next(csv_reader)
            user_mapping = self.extension_mapping_config.get_mapping_dictionary()

            for row in csv_reader:
                row_dict = dict(zip(headers, row))
                user_dict = {key: row_dict[value] for key, value in user_mapping.items() if value in row_dict}
                if user_dict.get("Enabled") == "0":
                    user_dict["HotdeskingAssignment"] = ""
                user_data.append(user_dict)
        return user_data

    def _validate_csv_users(self, user_data: list[dict]) -> list[CSVUser]:
        """Validate and convert raw user data into a list of CSVUser objects."""
        return TypeAdapter(list[CSVUser]).validate_python(user_data)

    def get_user_update_fields(self) -> list:
        return self.extension_mapping_config.get_update_fields()

    def get_source_groups(self):
        return None
