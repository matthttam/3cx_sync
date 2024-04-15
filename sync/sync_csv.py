import os
from .sync import Sync
import tkinter as tk
from app.config import TCXConfig
from app.mapping import CSVMapping
from tcx_api.tcx_api_connection import TCX_API_Connection
from tcx_api.resources.user import UserResource
import csv
from tcx_api.resources.user import ListUserParameters
from tcx_api import exceptions as TCX_Exceptions


class SyncCSV(Sync):
    def __init__(self, text: tk.Text = None) -> None:
        super().__init__(text=text)

    def sync(self):
        self.output("Initializing CSV Sync")
        self.output("Loading 3CX Config")
        self.config = TCXConfig()
        self.output("3CX Config Loaded")
        self.output("Initializing API Connection")
        self.api_connection = TCX_API_Connection(
            server_url=self.config.get_server_url()
        )
        self.User = UserResource(api=self.api_connection)
        self.output("Loading CSV Mapping")
        self.mapping = CSVMapping()
        self.output("CSV Mapping Loaded")

        ### Use CSV Mapping to parse CSV data into usable 3CX Schema Objects
        self.output_spacer()
        self.output("Starting CSV Sync")

        self.load_data()
        self.parse_data()
        return  # TEMP RETURN TO STOP
        if not self.authenticate():
            return False

        try:
            self.output("Fetching Users")
            users = self.User.list_user(params=ListUserParameters(top=10))
        except TCX_Exceptions.APIError as e:
            self.output("Failed to fetch users: {e}")
            return False
        self.output(f"Fetched {len(users)} users")

        self.output("Sync Complete")

    def load_data(self):
        self.output("Loading CSV Data")
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
                self.user_data.append(row_dict)

        self.output("CSV Data Loaded")

    def authenticate(self):
        self.output("Authenticating to 3CX")
        self.output("Server Path is " + self.config.get_server_url())
        try:
            self.api_connection.authenticate(
                username=self.config["3cx"].get("username"),
                password=self.config["3cx"].get("password"),
            )
            self.output("Authentication Successful")
            return True
        except TCX_Exceptions.APIAuthenticationError as e:
            self.output("Failed to authenticate: {e}")
            return False
