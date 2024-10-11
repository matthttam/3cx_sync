import os
import json
import copy
from collections import UserDict
from typing import Any
import platformdirs


class CSVMapping(UserDict):
    def __init__(self, *args, supress_load=False, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.original_config = None
        if not supress_load:
            self.load_defaults()
            self.load()

    @property
    def mapping_file_path(self):
        app_data_dir = platformdirs.user_config_dir("3cx_sync", "3cx_sync")
        config_file_path = os.path.join(app_data_dir, "conf")
        os.makedirs(config_file_path, exist_ok=True)
        return os.path.join(config_file_path, "csv_mapping.json")

    @property
    def is_dirty(self) -> bool:
        return self.original_config != self.data

    def load_defaults(self) -> None:
        default_config = {
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
        self.update(default_config)

    def load(self) -> None:
        if (
            not os.path.exists(self.mapping_file_path)
            or os.stat(self.mapping_file_path).st_size == 0
        ):
            return
        try:
            with open(self.mapping_file_path, "r") as mapping_file:
                mapping_config = json.load(mapping_file)
                self.update(mapping_config)
            self.original_config = copy.deepcopy(self.data)
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading mapping file: {e}")

    def save(self):
        with open(self.mapping_file_path, "w") as mapping_file:
            json.dump(self.data, mapping_file)
        self.original_config = copy.deepcopy(self.data)
