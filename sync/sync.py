import logging
import threading
import time
from app.config import AppConfig
from sync.sync_strategy import SyncSourceStrategy
from tcx_api.tcx_api_connection import TCX_API_Connection
from tcx_api.resources.users import UsersResource, ListUserParameters
from tcx_api.components.schemas.pbx import User
from tcx_api.exceptions import APIAuthenticationError
from sync.comparison import UserChangeDetail, UserComparer
from tcx_api.resources.group import GroupResource
from tcx_api.resources.users_exceptions import (
    UserCreateError,
    UserUpdateError,
    UserListError,
    UserHotdeskLogoutError,
)
from sync.logging import SyncLogger


class Sync:
    user_data = list()

    def __init__(
        self, sync_logger: SyncLogger, sync_source: SyncSourceStrategy
    ) -> None:
        self.running_event = threading.Event()
        self.running_event.set()  # Allow sync to run initially

        self.logger = sync_logger.get_logger()
        self.sync_source = sync_source(output=self.logger.info)

    def log(self, method, *args, **kwargs) -> None:
        """Logs a message using the specified method after checking if sync should pause.

        Args:
            method (str): The logging method to call (e.g., 'info', 'error').
            *args: Positional arguments for the logger method.
            **kwargs: Keyword arguments for the logger method.
        """
        log_method = getattr(self.logger, method, None)
        if callable(log_method):
            log_method(
                *args, **kwargs
            )  # Call the logging method with provided arguments
        else:
            raise ValueError(f"Invalid logging method: {method}")
        self._pause_if_needed()

    def sync(self):
        self.log("info", "Initializing Sync")
        self.log("info", "Loading 3CX Config")
        self.config = AppConfig()
        self.log("info", "3CX Config Loaded")
        self.log("info", "Initializing API Connection")
        self._pause_if_needed()
        self.api_connection = TCX_API_Connection(server_url=self.config.server_url)
        self._pause_if_needed()
        try:
            self.authenticate()
        except APIAuthenticationError:
            raise

        self.user_resource = UsersResource(api=self.api_connection)
        self.group_resource = GroupResource(api=self.api_connection)

        self._pause_if_needed()
        self.sync_source.initialize()
        self._pause_if_needed()
        self.source_user_list = self.sync_source.get_source_users()
        # self.source_group_list = self.sync_source.get_source_groups()

        self._pause_if_needed()
        self.tcx_user_list = self.get_users()
        user_comparer = UserComparer(
            tcx_user_list=self.tcx_user_list, sync_source=self.sync_source
        )
        user_change_details = user_comparer.get_user_change_details()
        user_change_details.sort(key=lambda x: x.user_to_update.Number)
        if len(user_change_details) > 0:
            self.log(
                "info",
                f"Count of users to update: {
                            len(user_change_details)}",
            )
            self.update_users(user_change_details=user_change_details)
        else:
            self.log("info", "No users to update.")

        users_to_create = user_comparer.get_users_to_create()
        if len(users_to_create) > 0:
            self.log(
                "info",
                f"Count of users to create: {
                            len(users_to_create)}",
            )
            self.create_users(users=users_to_create)
        else:
            self.log("info", "No users to create.")

        self.log("info", "Sync Complete")

    def index_users(self, users: list[User], key: str = "Number") -> dict[str, User]:
        return {
            getattr(user, key): user
            for user in users
            if user is not None and getattr(user, key) is not None
        }

    def create_users(self, users: list[User]):
        for user in users:
            self.create_user(user)

    def create_user(self, user: User):
        try:
            self.log("info", f"Creating 3CX user {user.Number}")
            new_user_dict = self.get_new_user()
            merged_user_dict = new_user_dict | user.model_dump()
            self._pause_if_needed()
            self.user_resource.create_user(merged_user_dict)
            self.log("info", f"Created 3CX user {merged_user_dict['Number']}")
        except UserCreateError as e:
            self.log("info", str(e))

    def get_new_user(self):
        new_user = self.user_resource.get_new_user()
        default_group = self.group_resource.get_default_group()
        new_user["PrimaryGroupId"] = default_group.Id
        new_user["Groups"].append(
            {"GroupId": default_group.Id, "Rights": {"RoleName": "users"}}
        )
        return new_user

    def update_users(self, user_change_details: list[UserChangeDetail]) -> None:
        for user_change_detail in user_change_details:
            self.update_user(user_change_detail)
            if self.config["app"].get("logout_hotdesk_on_disable", False):
                self.handle_logout_hotdesk_on_disable(user_change_detail)

    def handle_logout_hotdesk_on_disable(
        self, user_change_detail: UserChangeDetail
    ) -> None:
        enabled_change = user_change_detail.field_changes.get("Enabled")
        if enabled_change and enabled_change.new is False:
            self.log_user_out_of_assigned_hotdesks_by_number(user_change_detail.Number)

    def log_user_out_of_assigned_hotdesks_by_number(self, user_number: str) -> None:
        try:
            hotdesk_users = self.user_resource.get_hotdesks_by_assigned_user_number(
                user_number=user_number
            )
            if hotdesk_users:
                for hotdesk_user in hotdesk_users:
                    self.log(
                        "info",
                        f"Logging user {user_number} out of hotdesk {hotdesk_user.Number}",
                    )
                    self.user_resource.clear_hotdesk_assignment(hotdesk_user)
            else:
                self.log(
                    "info",
                    f"User {user_number} is being disabled. No action required for hotdesking as the user is not currently signed in to any hotdesk.",
                )
        except UserHotdeskLogoutError as e:
            self.log("info", str(e))

    def update_user(self, user_change_detail: UserChangeDetail):
        try:
            self.log(
                "info",
                f"Updating 3CX user {
                user_change_detail.Number}",
            )
            self._pause_if_needed()
            self.log("info", f"Changing {str(user_change_detail)}")
            self.user_resource.update_user(user_change_detail.user_to_update)

        except UserUpdateError as e:
            self.log("info", str(e))

    def get_users(self) -> list[User]:
        try:
            self.log("info", "Fetching Users From 3CX")
            users = self.user_resource.list_user(
                params=ListUserParameters(
                    expand="Groups($expand=Rights,GroupRights),ForwardingProfiles,ForwardingExceptions,Phones,Greetings"
                )
            )
        except UserListError as e:
            self.log("info", f"Failed to Fetch Users: {str(e)}")
            raise
        self.log("info", f"Fetched {len(users)} Users From 3CX")
        return users

    def authenticate(self) -> None:
        self.log("info", f"Authenticating to 3CX at {self.config.server_url}")
        try:
            self.api_connection.authenticate(
                username=self.config["3cx"].get("username"),
                password=self.config["3cx"].get("password"),
            )
            self.log("info", "Authentication Successful")
        except APIAuthenticationError as e:
            self.log("info", f"Failed to authenticate: {str(e)}")
            raise

    def _pause_if_needed(self):
        self.running_event.wait()  # Block thread if False

    def pause_sync(self):
        self.running_event.clear()  # Reset to False

    def resume_sync(self):
        self.running_event.set()  # Reset to True


# def run_sync(logger: logging.Logger, sync_source:SyncSourceStrategy):
def run_sync(sync: Sync):
    try:
        sync.sync()
    except APIAuthenticationError:
        Sync.logger.error("Failed to sync. Unable to authenticate.")
    except Exception as e:
        Sync.logger.error(f"Failed to sync. {e}")
