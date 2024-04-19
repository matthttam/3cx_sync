import os
# from .sync import Sync
from sync.sync import SyncSourceStrategy
from app.mapping import CSVMapping

import csv

from typing import Optional, List
from tcx_api.components.schemas.pbx import User


class SyncCSV(SyncSourceStrategy):

    def initialize(self):
        self.output("Initializing CSV Source")
        self.output("Loading CSV Mapping")
        self.mapping = CSVMapping()
        self.output("CSV Mapping Loaded")

    def get_source_users(self) -> Optional[List[User]]:
        user_data = list()
        self.output("Loading CSV User Data")
        csv_data_path = self.mapping.get("Extension", {}).get("Path", "")
        if not os.path.isfile(csv_data_path):
            self.output(f"Unable to find file at: {csv_data_path}")
            raise (FileNotFoundError)

        with open(csv_data_path) as csv_file:
            csv_reader = csv.reader(csv_file)
            user_mapping = self.mapping.get("Extension").get("New")
            headers = next(csv_reader)
            headers = [user_mapping[key] for key in headers]

            for row in csv_reader:
                row_dict = dict(zip(headers, row))
                user_data.append(row_dict)
        self.output(f"Loaded {len(user_data)} Users from CSV File")
        return user_data

    def get_source_groups(self):
        return None

        self.output("Sync Complete")

    def load_data(self):

        self.output("CSV Data Loaded")
