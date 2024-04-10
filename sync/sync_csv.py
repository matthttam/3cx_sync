from .sync import Sync
import tkinter as tk
from app.config import TCXConfig
from app.mapping import CSVMapping
from tcx_api.tcx_api_connection import TCX_API_Connection
from tcx_api.resources.user import UserFactory
from tcx_api.resources.resource_factory import ResourceFactory


class SyncCSV(Sync):
    def __init__(self, text: tk.Text = None) -> None:
        super().__init__(text=text)

    def sync(self):
        self.initialize()
        self.output_spacer()
        self.output("Starting CSV Sync")
        self.output("Authenticating to API")
        if not self.authenticate():
            return False

        self.output("Fetching Users")
        users = self.User.list_user(
            top=10,
        )
        self.output(str(users))
        if not users:
            return False
        self.output(f"Fetched {len(users)} users")

        user_entity = UserFactory.create_user(**users[0])
        print(user_entity)
        self.output("Sync Complete")

    def initialize(self):
        self.output("Initializing CSV Sync")
        # Load 3CX Config
        self.load_3cx_config()
        self.output("Initializing API Connection")
        self.api_connection = TCX_API_Connection(
            server_url=self.config.get_server_url()
        )
        self.load_resources()
        self.load_csv_mapping()

    def load_3cx_config(self):
        self.output("Loading 3CX Config")
        self.config = TCXConfig()
        self.output("3CX Config Loaded")

    def load_resources(self):
        self.resource_factory = ResourceFactory(api_connection=self.api_connection)
        self.User = self.resource_factory.get_resource("User")

    def load_csv_mapping(self):
        self.output("Loading CSV Mapping")
        self.mapping = CSVMapping()
        self.output("CSV Mapping Loaded")

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
        except Exception as e:
            self.output(f"Authentication Failed. {str(e)}")
            return False
