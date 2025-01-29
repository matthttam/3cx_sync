import os
import json
from collections import UserDict
from copy import deepcopy
import platformdirs
from app.util import initialize_or_get_user_config_file


class CSVMapping(UserDict):
    DEFAULT_FILENAME = "csv_mapping.json"

    def __init__(self, *args, mapping_file_path: str = None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.set_original_config()
        self.mapping_file_path = mapping_file_path or initialize_or_get_user_config_file(
            "3cx_sync", "3cx_sync", "conf", self.DEFAULT_FILENAME
        )
        # self.mapping_file_path = mapping_file_path
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
            if os.path.getsize(self.mapping_file_path) > 0:
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

    def save_to(self, path):
        with open(path, "w") as mapping_file:
            json.dump(self.data, mapping_file)

    def set_original_config(self):
        self.original_config = deepcopy(self.data)
