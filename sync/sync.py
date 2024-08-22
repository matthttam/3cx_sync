import tkinter as tk
from datetime import datetime
from app.config import TCXConfig
from sync.sync_strategy import SyncSourceStrategy
from tcx_api.tcx_api_connection import TCX_API_Connection
from tcx_api.resources.user import UserResource
from tcx_api.components.schemas.pbx import User, Group
from tcx_api.resources.user import ListUserParameters
from tcx_api import exceptions as TCX_Exceptions
from tcx_api.exceptions import APIAuthenticationError
from sync.comparison import UserChangeDetail, UserComparer


class Sync:
    user_data = list()

    def __init__(self, app: tk.Tk, sync_source: SyncSourceStrategy) -> None:
        self.app = app
        self.sync_source = sync_source(output=self.app.output)

    def sync(self):
        self.app.output("Initializing Sync")
        self.app.output("Loading 3CX Config")
        self.config = TCXConfig()
        self.config.load()
        self.app.output("3CX Config Loaded")
        self.app.output("Initializing API Connection")
        self.api_connection = TCX_API_Connection(
            server_url=self.config.server_url
        )
        try:
            self.authenticate()
        except APIAuthenticationError:
            raise
        self.api_connection.refresh_access_token()
        self.UserResource = UserResource(api=self.api_connection)
        self.sync_source.initialize()
        self.source_user_list = self.sync_source.get_source_users()
        # self.source_group_list = self.sync_source.get_source_groups()
        self.tcx_user_list = self.get_users()
        user_comparer = UserComparer(
            tcx_user_list=self.tcx_user_list, sync_source=self.sync_source)
        users_to_update = user_comparer.get_users_to_update()
        if len(users_to_update) > 0:
            self.app.output(f"Count of users to update: {
                            len(users_to_update)}")
            self.update_users(user_change_details=users_to_update)
        else:
            self.app.output("No users to update.")

        users_to_create = user_comparer.get_users_to_create()
        if len(users_to_create) > 0:
            self.app.output(f"Count of users to create: {
                            len(users_to_create)}")
            self.create_users(users=users_to_create)
        else:
            self.app.output("No users to create.")

        self.app.output("Sync Complete")

    def index_users(self, users: list[User], key: str = "Number") -> dict[str, User]:
        return {getattr(user, key): user for user in users if user is not None and getattr(user, key) is not None}

    def create_users(self, users: list[User]):
        for user in users:
            self.create_user(user)

    def create_user(self, user: User):
        try:
            self.app.output(f"Creating 3CX user {user.Number}")
            self.UserResource.create_user(user)
            self.app.output(f"Created 3CX user {user.Number}")
        except TCX_Exceptions.UserCreateError as e:
            self.app.output(str(e))

    def update_users(self, user_change_details: list[UserChangeDetail]):
        for user_change_detail in user_change_details:
            self.update_user(user_change_detail)

    def update_user(self, user_change_detail: UserChangeDetail):
        try:
            self.app.output(f"Updating 3CX user {
                user_change_detail.Number}")
            self.app.output(f"Changing {str(user_change_detail)}")
            self.UserResource.update_user(user_change_detail.user_to_update)

        except TCX_Exceptions.UserUpdateError as e:
            self.app.output(str(e))

    def get_users(self) -> list[User]:
        try:
            self.app.output("Fetching Users From 3CX")
            users = self.UserResource.list_user(
                params=ListUserParameters(expand="Groups($expand=Rights,GroupRights),ForwardingProfiles,ForwardingExceptions,Phones,Greetings"))
        except TCX_Exceptions.UserListError as e:
            self.app.output(f"Failed to Fetch Users: {str(e)}")
            raise
        self.app.output(f"Fetched {len(users)} Users From 3CX")
        return users

    def get_groups(self) -> list[Group]:
        pass

    def authenticate(self):
        self.app.output(f"Authenticating to 3CX at {self.config.server_url}")
        try:
            self.api_connection.authenticate(
                username=self.config["3cx"].get("username"),
                password=self.config["3cx"].get("password"),
            )
            self.app.output("Authentication Successful")
        except TCX_Exceptions.APIAuthenticationError as e:
            self.app.output(f"Failed to authenticate: {str(e)}")
            raise e
