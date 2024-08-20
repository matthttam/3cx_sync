import tkinter as tk
from datetime import datetime
from typing import Optional, NamedTuple
from app.config import TCXConfig
from sync.sync_strategy import SyncSourceStrategy
from tcx_api.tcx_api_connection import TCX_API_Connection
from tcx_api.resources.user import UserResource
from tcx_api.components.schemas.pbx import User, Group
from tcx_api.resources.user import ListUserParameters
from tcx_api import exceptions as TCX_Exceptions
from tcx_api.exceptions import APIAuthenticationError
from sync.comparison import UserChangeDetail, UserComparer


# class UserComparisonResult(NamedTuple):
#    users_to_create: list[User]
#    users_to_update: list[User]
#
#
# class UserUpdateInfo(NamedTuple):
#    user_to_update: User


class Sync:
    user_data = list()

    def __init__(self, sync_source: SyncSourceStrategy, text: tk.Text) -> None:
        self.sync_source = sync_source(output=self.output)
        self.text = text
        self.newline = ""  # Set to "\n" on first output

    def output(self, value: str) -> None:
        text_output = self.newline + self.get_timestamp() + value
        self.text.insert(tk.END, text_output)
        self.newline = "\n"
        self.text.winfo_toplevel().update()

    def get_timestamp(self) -> str:
        dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        return f"[{dt}]"

    def sync(self):
        self.output("Initializing Sync")
        self.output("Loading 3CX Config")
        self.config = TCXConfig()
        self.config.load()
        self.output("3CX Config Loaded")
        self.output("Initializing API Connection")
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
        # users_to_create = self.get_users_to_create(tcx_user_list=self.tcx_user_list,
        #                                           source_user_list=self.source_user_list)
        # users_to_update = self.get_users_to_update(tcx_user_list=self.tcx_user_list,
        #                                           source_user_list=self.source_user_list, update_fields=self.sync_source.get_user_update_fields())

        # comparison_results = self.compare_users(tcx_user_list=self.tcx_user_list,
        #                                        source_user_list=self.source_user_list)
        user_comparer = UserComparer(
            tcx_user_list=self.tcx_user_list, sync_source=self.sync_source)
        users_to_update = user_comparer.get_users_to_update()
        if len(users_to_update) > 0:
            self.output(f"Count of users to update: {len(users_to_update)}")
            self.update_users(user_change_details=users_to_update)
        else:
            self.output("No users to update.")

        users_to_create = user_comparer.get_users_to_create()
        if len(users_to_create) > 0:
            self.output(f"Count of users to create: {len(users_to_create)}")
            self.create_users(users=users_to_create)
        else:
            self.output("No users to create.")

    def index_users(self, users: list[User], key: str = "Number") -> dict[str, User]:
        return {getattr(user, key): user for user in users if user is not None and getattr(user, key) is not None}

    def get_users_to_create(self, tcx_user_list: list[User], source_user_list: list[User]) -> list[User]:
        tcx_user_dict = self.index_users(users=tcx_user_list)
        tcx_user_keys = set(tcx_user_dict.keys())
        source_user_dict = self.index_users(users=source_user_list)
        source_user_keys = set(source_user_dict.keys())

        # Determine users to create
        user_keys_to_create = list(source_user_keys - tcx_user_keys)
        users_to_create = [source_user_dict[k] for k in list(
            set(source_user_dict).intersection(user_keys_to_create))]
        self.output(f"Count of users to create: {len(user_keys_to_create)}")
        return users_to_create

    # def get_users_to_update(self, tcx_user_list: list[User], source_user_list: list[User], update_fields: list) -> list[User]:
    #    tcx_user_dict = self.index_users(users=tcx_user_list)
    #    tcx_user_keys = set(tcx_user_dict.keys())
    #    source_user_dict = self.index_users(users=source_user_list)
    #    source_user_keys = set(source_user_dict.keys())
#
    #    users_to_update = []
    #    user_keys_to_compare = list(
    #        source_user_keys.intersection(tcx_user_keys))
    #    self.output(f"Comparing {len(user_keys_to_compare)} users")
#
    #    for key in user_keys_to_compare:
    #        tcx_user = tcx_user_dict[key]
    #        source_user = source_user_dict[key]
    #        updated_fields = {}
#
    #        for field in update_fields:
    #            tcx_value = getattr(tcx_user, field, None)
    #            source_value = getattr(source_user, field, None)
#
    #            if tcx_value != source_value:
    #                updated_fields[field] = source_value
#
    #        if updated_fields:
    #            updated_user = User(**(tcx_user.model_dump() | updated_fields))
    #            users_to_update.append(updated_user)
    #    return users_to_update

    # def compare_users(self, tcx_user_list: list[User], source_user_list: list[User]) -> UserComparisonResult:
    #    tcx_user_dict = self.index_users(users=tcx_user_list)
    #    tcx_user_keys = set(tcx_user_dict.keys())
    #    source_user_dict = self.index_users(users=source_user_list)
    #    source_user_keys = set(source_user_dict.keys())
#
    #    # Determine users to create
    #    user_keys_to_create = list(source_user_keys - tcx_user_keys)
    #    users_to_create = [source_user_dict[k] for k in list(
    #        set(source_user_dict).intersection(user_keys_to_create))]
    #    self.output(f"Count of users to create: {len(user_keys_to_create)}")
#
    #    # Determine users to compare with existing users
    #    user_keys_to_compare = list(
    #        source_user_keys.intersection(tcx_user_keys))
    #    users_to_compare = {k: source_user_dict[k] for k in list(
    #        set(source_user_dict).intersection(user_keys_to_compare))}
    #    self.output(f"Comparing {len(user_keys_to_compare)} users")
#
    #    # Determine users that have been changed
    #    users_to_update = list()
    #    source_users_to_update = {tcx_user_dict[k].Number: source_user_dict[k] for k in set(
    #        users_to_compare.keys()) if source_user_dict[k] != tcx_user_dict[k]}
    #    for key, source_user_to_update in source_users_to_update.items():
    #        users_to_update.append(tcx_user_dict[key] | source_user_to_update)
    #    self.output(f"Count of users to update: {len(users_to_update)}")
    #    return UserComparisonResult(users_to_create=users_to_create, users_to_update=users_to_update)

    def create_users(self, users: list[User]):
        for user in users:
            self.create_user(user)

    def create_user(self, user: User):
        try:
            self.UserResource.create_user(user)
            self.output(f"Created 3CX user {user.Number}")
        except TCX_Exceptions.UserCreateError as e:
            self.output(str(e))

    def update_users(self, user_change_details: list[UserChangeDetail]):
        for user_change_detail in user_change_details:
            self.update_user(user_change_detail)

    def update_user(self, user_change_detail: UserChangeDetail):
        try:
            self.output(f"Updating 3CX user {
                        user_change_detail.Number}")
            self.output(f"Changing {str(user_change_detail)}")
            self.UserResource.update_user(user_change_detail.user_to_update)

        except TCX_Exceptions.UserUpdateError as e:
            self.output(str(e))

    def get_users(self) -> list[User]:
        try:
            self.output("Fetching Users From 3CX")
            users = self.UserResource.list_user(
                params=ListUserParameters(expand="Groups($expand=Rights,GroupRights),ForwardingProfiles,ForwardingExceptions,Phones,Greetings"))
        except TCX_Exceptions.UserListError as e:
            self.output(f"Failed to Fetch Users: {str(e)}")
            raise
        self.output(f"Fetched {len(users)} Users From 3CX")
        return users

    def get_groups(self) -> list[Group]:
        pass

    def authenticate(self):
        self.output(f"Authenticating to 3CX at {self.config.server_url}")
        try:
            self.api_connection.authenticate(
                username=self.config["3cx"].get("username"),
                password=self.config["3cx"].get("password"),
            )
            self.output("Authentication Successful")
        except TCX_Exceptions.APIAuthenticationError as e:
            self.output(f"Failed to authenticate: {str(e)}")
            raise e
