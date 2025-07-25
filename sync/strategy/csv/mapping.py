import json
from pathlib import Path
from collections import UserDict
from copy import deepcopy
import platformdirs
from app.util import initialize_or_get_user_config_path


class CSVMapping(UserDict):
    DEFAULT_FILENAME = "csv_mapping.json"

    def __init__(self, config_path: Path = None) -> None:
        super().__init__()
        self.set_original_config()
        self.mapping_file_path = (
            config_path or initialize_or_get_user_config_path("3cx_sync", "3cx_sync", "conf")
        ) / self.DEFAULT_FILENAME

        self.default_config = {
            "Extension": {
                "Path": platformdirs.user_documents_dir(),
                "Key": "Number",
                "New": {
                    "Number": "Number",
                    "FirstName": "FirstName",
                    "LastName": "LastName",
                    "EmailAddress": "Email",
                    "VMPIN": "VMPIN",
                    "VMEmailOptions": "VMEmailOptions",
                    "OutboundCallerID": "OutboundCallerID",
                    "SendEmailMissedCalls": "SendEmailMissedCalls",
                    "Enabled": "Enabled",
                    "EnableHotdesking": "AllowToUseHotdesking",
                    "RecordCalls": "RecordCalls",
                    "RecordExternalCallsOnly": "RecordExternalCallsOnly",
                    "VMEnabled": "VMEnabled",
                    "WebMeetingFriendlyName": "WebMeetingFriendlyName",
                },
                "Update": ["FirstName", "LastName", "EmailAddress", "Enabled"],
            }
        }

    def initialize(self):
        self.load_defaults()
        self.load() if self.mapping_file_path.exists() else None

    @property
    def is_dirty(self) -> bool:
        return self.original_config != self.data

    def load_defaults(self) -> None:
        self.update(self.default_config)

    def load(self) -> None:
        """Load configuration from the specified file."""
        if not self.mapping_file_path.exists():
            return
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
    
    def restore_original_config(self):
        """Restore the original configuration."""
        self.data = deepcopy(self.original_config)

    def get_parsed_config(self) -> list[dict]:
        """
        Returns an array with a dictionary for each field
        containing values for what each field has set.
        """
        parsed_config = []
        extension_mapping = self.get("Extension", {})
        new_mapping = extension_mapping.get("New", {})
        key_header = extension_mapping.get("Key", None)
        for field, header in new_mapping.items():
            update = field in extension_mapping.get("Update", {})
            static = field in extension_mapping.get("Static", {})
            parsed_config.append(
                {
                    "header": header,
                    "field": field,
                    "static": static,
                    "key": (header == key_header),
                    "update": update,
                }
            )
        return parsed_config
