import os
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
        self.load()

    @property
    def is_dirty(self) -> bool:
        return self.original_config != self.data

    def load_defaults(self) -> None:
        self.update(self.default_config)

    def load(self) -> None:
        """Load configuration from the specified file."""
        try:
            # Check if the file exists and is not empty
            if self.mapping_file_path.stat().st_size > 0:
                # if os.path.getsize(self.mapping_file_path) > 0:
                with open(self.mapping_file_path, "r") as mapping_file:
                    self.update(json.load(mapping_file))
                self.set_original_config()
            else:
                print(f"Warning: {self.mapping_file_path} is empty.")
        except FileNotFoundError:
            print(f"Warning: {self.mapping_file_path} does not exist")
            raise
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading mapping file: {e}")
            raise

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
