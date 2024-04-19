import tkinter as tk
from datetime import datetime
from abc import ABC, abstractmethod
from typing import List, Callable, Optional
from app.config import TCXConfig
from tcx_api.tcx_api_connection import TCX_API_Connection
from tcx_api.resources.user import UserResource
from tcx_api.components.schemas.pbx import User, Group
from tcx_api.resources.user import ListUserParameters
from tcx_api import exceptions as TCX_Exceptions


class SyncSourceStrategy(ABC):
    def __init__(self, output: Callable):
        self.output = output

    @abstractmethod
    def initialize(self) -> None:
        ...

    @abstractmethod
    def get_source_users(self) -> Optional[List[User]]:
        ...

    @abstractmethod
    def get_source_groups(self) -> Optional[List[Group]]:
        ...


class Sync:
    user_data = list()

    def __init__(self, sync_source: SyncSourceStrategy, text: tk.Text) -> None:
        self.sync_source = sync_source(output=self.output)
        self.text = text
        self.newline = ""  # Set to "\n" on first output

    def output(self, value) -> None:
        text_output = self.newline + self.get_timestamp() + value
        self.text.insert(tk.END, text_output)
        self.newline = "\n"
        # self.text.master.update()
        self.text.winfo_toplevel().update()

    def get_timestamp(self) -> str:
        dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        return f"[{dt}]"

    def sync(self):
        self.output("Initializing Sync")
        self.output("Loading 3CX Config")
        self.config = TCXConfig()
        self.output("3CX Config Loaded")
        self.output("Initializing API Connection")
        self.api_connection = TCX_API_Connection(
            server_url=self.config.get_server_url()
        )
        self.UserResource = UserResource(api=self.api_connection)
        self.sync_source.initialize()
        self.source_user_list = self.sync_source.get_source_users()
        self.source_group_list = self.sync_source.get_source_groups()
        self.tcx_user_list = self.get_users()

    def get_users(self) -> List[User]:
        try:
            self.output("Fetching Users From 3CX")
            users = self.UserResource.list_user(params=ListUserParameters())
        except TCX_Exceptions.APIError as e:
            self.output("Failed to Fetch Users: {e}")
            return False
        self.output(f"Fetched {len(users)} Users From 3CX")

    def get_groups(self) -> List[Group]:
        pass

    def authenticate(self):
        self.output(f"Authenticating to 3CX at {self.config.get_server_url()}")
        try:
            self.api_connection.authenticate(
                username=self.config["3cx"].get("username"),
                password=self.config["3cx"].get("password"),
            )
            self.output("Authentication Successful")
        except TCX_Exceptions.APIAuthenticationError as e:
            self.output("Failed to authenticate: {e}")
            raise e
