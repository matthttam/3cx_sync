import tkinter as tk
from app.config import AppConfig
from sync.sync_strategy import SyncSourceStrategy
from tcx_api.tcx_api_connection import TCX_API_Connection
from tcx_api.resources.user import UserResource, ListUserParameters
from tcx_api.components.schemas.pbx import User, Group
from tcx_api import exceptions as TCX_Exceptions
from tcx_api.exceptions import APIAuthenticationError
from sync.comparison import UserChangeDetail, UserComparer
from tcx_api.resources.group import GroupResource, ListGroupParameters


class Sync:
    user_data = list()

    def __init__(self, app: tk.Tk, sync_source: SyncSourceStrategy) -> None:
        self.app = app
        self.sync_source = sync_source(output=self.app.output)

    def sync(self):
        self.app.output("Initializing Sync")
        self.app.output("Loading 3CX Config")
        self.config = AppConfig()
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
        self.user_resource = UserResource(api=self.api_connection)
        self.group_resource = GroupResource(api=self.api_connection)

        self.sync_source.initialize()
        self.source_user_list = self.sync_source.get_source_users()
        # self.source_group_list = self.sync_source.get_source_groups()
        self.tcx_user_list = self.get_users()
        user_comparer = UserComparer(
            tcx_user_list=self.tcx_user_list, sync_source=self.sync_source)
        user_change_details = user_comparer.get_user_change_details()
        # user_change_details = self.hydrate_user_change_details(user_change_details)
        user_change_details.sort(key=lambda x: x.user_to_update.Number)
        if len(user_change_details) > 0:
            self.app.output(f"Count of users to update: {
                            len(user_change_details)}")
            self.update_users(user_change_details=user_change_details)
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
            new_user_dict = self.get_new_user()
            merged_user_dict = new_user_dict | user.model_dump()
            self.user_resource.create_user(merged_user_dict)
            self.app.output(f"Created 3CX user {merged_user_dict['Number']}")
        except TCX_Exceptions.UserCreateError as e:
            self.app.output(str(e))

    def get_new_user(self):
        new_user = self.user_resource.get_new_user()
        default_group = self.group_resource.get_default_group()
        new_user['Groups'].append(
            {'GroupId': default_group.Id,
                'Rights': {'RoleName': 'users'}
             })
        return new_user

    def update_users(self, user_change_details: list[UserChangeDetail]):
        for user_change_detail in user_change_details:
            self.update_user(user_change_detail)

    def update_user(self, user_change_detail: UserChangeDetail):
        try:
            self.app.output(f"Updating 3CX user {
                user_change_detail.Number}")
            self.app.output(f"Changing {str(user_change_detail)}")
            self.user_resource.update_user(user_change_detail.user_to_update)

        except TCX_Exceptions.UserUpdateError as e:
            self.app.output(str(e))

    def get_users(self) -> list[User]:
        try:
            self.app.output("Fetching Users From 3CX")
            users = self.user_resource.list_user(
                params=ListUserParameters(expand="Groups($expand=Rights,GroupRights),ForwardingProfiles,ForwardingExceptions,Phones,Greetings"))
        except TCX_Exceptions.UserListError as e:
            self.app.output(f"Failed to Fetch Users: {str(e)}")
            raise
        self.app.output(f"Fetched {len(users)} Users From 3CX")
        return users

    # def hydrate_user_change_details(self, user_change_details: list[UserChangeDetail]) -> list[UserChangeDetail]:
    #    try:
    #        self.app.output(f"Fetching Additional Details for {len(
    #                        user_change_details)} Users to Update")
    #        for user_change_detail in user_change_details:
#
    #            detailed_user = self.UserResource.get_user(id=user_change_detail.user_to_update_dict['Id'],
    #                                                       params=ListUserParameters(expand="Groups($expand=Rights,GroupRights),ForwardingProfiles,ForwardingExceptions,Phones,Greetings"))
#
    #            user_change_detail.user_to_update = User(
    #                **(detailed_user.model_dump() | user_change_detail.user_to_update_dict))
#
    #    except TCX_Exceptions.UserListError as e:
    #        self.app.output(
    #            f"Failed to Fetch Additional Details for Users to Update: {str(e)}")
    #        raise
    #    self.app.output(
    #        f"Fetched {len(user_change_details)} Detailed Users From 3CX")
    #    return user_change_details

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
            raise
