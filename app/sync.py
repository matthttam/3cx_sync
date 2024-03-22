from abc import ABC, abstractmethod
import tkinter as tk
from app.config import TCXConfig
from app.mapping import CSVMapping
from datetime import datetime
from app.api import API


class Sync(ABC):

    def __init__(self, text: tk.Text = None) -> None:
        self.text = text
        self.newline = ""  # Set to "\n" on first output

    def output(self, value) -> None:
        text_output = self.newline + self.get_timestamp() + value
        if self.text:
            self.text.insert(tk.END, text_output)
            self.newline = "\n"
        else:
            print(text_output)

    def output_spacer(self) -> None:
        self.output("----------")

    def get_timestamp(self) -> str:
        dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        return f"[{dt}]"

    @abstractmethod
    def sync(self) -> None: ...


class SyncCSV(Sync):
    def __init__(self, text: tk.Text = None) -> None:
        super().__init__(text=text)

    def sync(self):
        self.output("Starting CSV Sync")
        self.output("Loading 3CX Config")
        # Load 3CX Config
        self.config = TCXConfig()
        self.output("3CX Config Loaded")
        # Load Mapping
        self.output("Loading CSV Mapping")
        self.mapping = CSVMapping()
        self.output("CSV Mapping Loaded")
        self.output_spacer()

        self.output("Initializing API Connection")

        response = self.authenticate()
        if not response:
            return False

        self.output("Fetching Users")
        users = self.api.Users.get_users()
        if not users:
            return False
        self.output(f"Fetched {len(users)} users")
        self.output("Syncing")
        self.output("Sync Complete")

    def authenticate(self):
        self.output("Authenticating to 3CX")
        self.output("Server Path is " + self.config.get_server_url())
        self.api = API(server_url=self.config.get_server_url())
        response = self.api.authenticate(
            username=self.config["3cx"].get("username"),
            password=self.config["3cx"].get("password"),
        )
        if not response:
            self.output("Authentication Failed")
            return False
        self.output("Authentication Successful")
        return response
