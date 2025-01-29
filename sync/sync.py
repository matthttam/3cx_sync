import threading
from app.config import AppConfig
from sync.sync_strategy import SyncSourceStrategy
from threecxapi.connection import ThreeCXApiConnection
from threecxapi.resources.users import UsersResource, ListUserParameters
from threecxapi.components.schemas.pbx import User
from threecxapi.components.responses.pbx import UserCollectionResponse
from threecxapi.exceptions import APIAuthenticationError
from sync.comparison import UserChangeDetail, UserComparer
from threecxapi.resources.groups import GroupsResource
from threecxapi.resources.exceptions.users_exceptions import (
    UserCreateError,
    UserUpdateError,
    UserListError,
    UserHotdeskLogoutError,
    UserHotdeskLookupError,
)
from sync.logging import SyncLogger, LogLevel


class Sync:
    user_data = list()

    def __init__(
        self,
        api_connection,
        app_config: AppConfig,
        sync_source: SyncSourceStrategy,
        logger: SyncLogger,
    ) -> None:
        self.running_event = threading.Event()
        self.running_event.set()  # Allow sync to run initially

        self.logger = logger
        self.sync_source = sync_source
        self.app_config = app_config
        self.api_connection = api_connection

        # Set up resources
        self.users_resource = UsersResource(api=self.api_connection)
        self.groups_resource = GroupsResource(api=self.api_connection)

    @staticmethod
    def pause_if_needed(method):
        def wrapper(self, *args, **kwargs):
            self._pause_if_needed()
            result = method(self, *args, **kwargs)
            self._pause_if_needed()
            return result

        return wrapper

    @pause_if_needed
    def initialize_sync_source(self):
        self.logger.log(LogLevel.INFO, "Initializing Sync Source")
        self.sync_source.initialize()

    @pause_if_needed
    def get_users(self) -> list[User]:
        try:
            self.logger.log(LogLevel.INFO, "Fetching Users From 3CX")
            user_collection_response = self.users_resource.list_user(
                params=ListUserParameters(
                    expand="Groups($expand=Rights,GroupRights),ForwardingProfiles,ForwardingExceptions,Phones,Greetings"
                )
            )
        except UserListError as e:
            self.logger.log(LogLevel.ERROR, f"Failed to Fetch Users: {e}")
            raise
        self.logger.log(
            LogLevel.INFO,
            f"Fetched {len(user_collection_response.value)} Users From 3CX",
        )
        return user_collection_response.value

    @pause_if_needed
    def handle_users_to_update(self, user_change_details):
        if len(user_change_details) > 0:
            self.logger.log(
                LogLevel.INFO,
                f"Count of users to update: {
                            len(user_change_details)}",
            )
            self.update_users(user_change_details=user_change_details)
        else:
            self.logger.log(LogLevel.INFO, "No users to update.")

    @pause_if_needed
    def handle_users_to_create(self, users_to_create):
        if len(users_to_create) > 0:
            self.logger.log(
                LogLevel.INFO,
                f"Count of users to create: {
                            len(users_to_create)}",
            )
            self.create_users(users=users_to_create)
        else:
            self.logger.log(LogLevel.INFO, "No users to create.")

    @pause_if_needed
    def initialize_user_comparer(self):
        return UserComparer(
            tcx_user_list=self.tcx_user_list, sync_source=self.sync_source
        )

    def pause_sync(self):
        self.running_event.clear()  # Reset to False

    def resume_sync(self):
        self.running_event.set()  # Reset to True

    def get_new_user(self):
        new_user = self.users_resource.get_new_user()
        default_group = self.groups_resource.get_default_group()
        new_user["PrimaryGroupId"] = default_group.Id
        new_user["Groups"].append(
            {"GroupId": default_group.Id, "Rights": {"RoleName": "users"}}
        )
        return new_user

    @pause_if_needed
    def create_users(self, users: list[User]):
        for user in users:
            self.create_user(user)

    @pause_if_needed
    def create_user(self, user: User):
        try:
            self.logger.log(LogLevel.INFO, f"Creating 3CX user {user.Number}")
            new_user_dict = self.get_new_user()
            merged_user_dict = new_user_dict | user.model_dump()
            self.users_resource.create_user(merged_user_dict)
            self.logger.log(
                LogLevel.INFO, f"Created 3CX user {merged_user_dict['Number']}"
            )

        except UserCreateError as e:
            self.logger.log(LogLevel.ERROR, str(e))

    @pause_if_needed
    def update_users(self, user_change_details: list[UserChangeDetail]) -> None:
        for user_change_detail in user_change_details:
            self.update_user(user_change_detail)

    @pause_if_needed
    def update_user(self, user_change_detail: UserChangeDetail):
        try:
            self.logger.log(
                LogLevel.INFO, f"Updating 3CX user {user_change_detail.Number}"
            )
            self.logger.log(LogLevel.INFO, f"Changing {str(user_change_detail)}")
            self.users_resource.update_user(user_change_detail.user_to_update)
            self.logout_user_hotdesks_on_disable(user_change_detail)
        except UserUpdateError as e:
            self.logger.log(LogLevel.ERROR, str(e))

    @pause_if_needed
    def logout_user_hotdesks_on_disable(
        self, user_change_detail: UserChangeDetail
    ) -> None:
        # If the option to log out hotdesk on disable is enabled, and the user is being disabled
        # log the user out of any assigned hotdesks
        if (
            self.app_config.logout_hotdesk_on_disable
            and user_change_detail.is_disabling
        ):
            try:
                self._logout_user_hotdesks_by_number(user_change_detail.Number)
            except UserHotdeskLogoutError as e:
                self.logger.log(LogLevel.ERROR, str(e))
            except UserHotdeskLookupError as e:
                self.logger.log(LogLevel.ERROR, str(e))

    @pause_if_needed
    def _logout_user_hotdesks_by_number(self, user_number: str) -> None:
        hotdesk_user_collection_response = (
            self.users_resource.get_hotdesks_by_assigned_user_number(
                user_number=user_number
            )
        )
        if not hotdesk_user_collection_response.value:
            self.logger.log(
                LogLevel.INFO,
                f"User {user_number} is being disabled. "
                "No hotdesk logout required as the user is not signed in to any hotdesk.",
            )
            return

        for hotdesk_user in hotdesk_user_collection_response.value:
            self.logger.log(
                LogLevel.INFO,
                f"Logging user {user_number} out of hotdesk {hotdesk_user.Number}",
            )
            self.users_resource.clear_hotdesk_assignment(hotdesk_user)

    def sync(self):
        self.initialize_sync_source()
        self.source_user_list = self.sync_source.get_source_users()
        self.tcx_user_list = self.get_users()
        user_comparer = self.initialize_user_comparer()
        user_change_details = user_comparer.get_user_change_details()
        user_change_details.sort(key=lambda x: x.user_to_update.Number)
        self.handle_users_to_update(user_change_details)
        users_to_create = user_comparer.get_users_to_create()
        self.handle_users_to_create(users_to_create)
        self.logger.log(LogLevel.INFO, "Sync Complete")

    def _pause_if_needed(self):
        self.running_event.wait()  # Block thread if False


def run_sync(sync_source: SyncSourceStrategy, logger: SyncLogger):
    try:
        logger.log(LogLevel.INFO, "Initializing Sync")
        app_config = get_app_config(logger)
        api_connection = get_api_connection(app_config, logger)
        sync = Sync(api_connection, app_config, sync_source(logger), logger)
        sync.sync()
    except APIAuthenticationError:
        logger.log(LogLevel.ERROR, "Failed to sync. Unable to authenticate.")
    except Exception as e:
        logger.log(LogLevel.ERROR, f"Failed to sync. {e}")


def get_app_config(logger: SyncLogger):
    logger.log(LogLevel.INFO, "Loading App Config")
    app_config = AppConfig()
    app_config.load()
    logger.log(LogLevel.INFO, "App Config Loaded")
    return app_config


def get_api_connection(app_config, logger):
    logger.log(LogLevel.INFO, "Initializing API Connection")
    api_connection = ThreeCXApiConnection(server_url=app_config.server_url)
    logger.log(LogLevel.INFO, "API Connection Initialized")
    logger.log(LogLevel.INFO, f"Authenticating to 3CX at {app_config.server_url}")
    try:
        api_connection.authenticate(
            username=app_config["3cx"].get("username"),
            password=app_config["3cx"].get("password"),
        )
        logger.log(LogLevel.INFO, "Authentication Successful")
    except APIAuthenticationError as e:
        logger.log(LogLevel.ERROR, f"Failed to authenticate: {str(e)}")
        raise
    return api_connection
