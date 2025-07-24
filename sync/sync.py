import threading
from typing import Callable, Optional
from app.config import AppConfig
from sync.strategy.factory import create_sync_source
from sync.strategy.strategy import SyncSourceStrategy
from threecxapi.connection import ThreeCXApiConnection
from threecxapi.resources.users import UsersResource, ListUserParameters
from threecxapi.components.schemas.pbx import User
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
from sync.exceptions import ThreadTermination


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

        # Event to stop the sync process if early termination is triggered
        self.terminate_event = threading.Event()

        self.logger = logger
        self.sync_source = sync_source
        self.app_config = app_config
        self.api_connection = api_connection

        # Set up resources
        self.users_resource = UsersResource(api=self.api_connection)
        self.groups_resource = GroupsResource(api=self.api_connection)

    @property
    def is_terminated(self):
        return self.terminate_event.is_set()

    @property
    def is_paused(self):
        return not self.running_event.is_set()

    @staticmethod
    def handle_interupts(method):
        def wrapper(self, *args, **kwargs):
            self._handle_interupts()
            result = method(self, *args, **kwargs)
            self._handle_interupts()
            return result

        return wrapper

    @handle_interupts
    def initialize_sync_source(self):
        self.logger.log(LogLevel.INFO, "Initializing Sync Source")
        self.sync_source.initialize()

    @handle_interupts
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

    @handle_interupts
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

    @handle_interupts
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

    @handle_interupts
    def initialize_user_comparer(self):
        return UserComparer(tcx_user_list=self.tcx_user_list, sync_source=self.sync_source)

    def pause(self):
        self.running_event.clear()  # Reset to False

    def resume(self):
        self.running_event.set()  # Reset to True
        self.logger.log(LogLevel.INFO, "Resumed by user")

    def get_new_user(self):
        new_user = self.users_resource.get_new_user()
        default_group = self.groups_resource.get_default_group()
        new_user["PrimaryGroupId"] = default_group.Id
        new_user["Groups"].append({"GroupId": default_group.Id, "Rights": {"RoleName": "users"}})
        return new_user

    @handle_interupts
    def create_users(self, users: list[User]):
        for user in users:
            self.create_user(user)

    @handle_interupts
    def create_user(self, user: User):
        try:
            self.logger.log(LogLevel.INFO, f"Creating 3CX user {user.Number}")
            new_user_dict = self.get_new_user()
            merged_user_dict = new_user_dict | user.model_dump()
            self.users_resource.create_user(merged_user_dict)
            self.logger.log(LogLevel.INFO, f"Created 3CX user {merged_user_dict['Number']}")

        except UserCreateError as e:
            self.logger.log(LogLevel.ERROR, str(e))

    @handle_interupts
    def update_users(self, user_change_details: list[UserChangeDetail]) -> None:
        for user_change_detail in user_change_details:
            self.update_user(user_change_detail)

    @handle_interupts
    def update_user(self, user_change_detail: UserChangeDetail):
        try:
            self.logger.log(LogLevel.INFO, f"Updating 3CX user {user_change_detail.Number}")
            self.logger.log(LogLevel.INFO, f"Changing {str(user_change_detail)}")
            self.users_resource.update_user(user_change_detail.user_to_update)
            self.logout_user_hotdesks_on_disable(user_change_detail)
        except UserUpdateError as e:
            self.logger.log(LogLevel.ERROR, str(e))

    @handle_interupts
    def logout_user_hotdesks_on_disable(self, user_change_detail: UserChangeDetail) -> None:
        # If the option to log out hotdesk on disable is enabled, and the user is being disabled
        # log the user out of any assigned hotdesks
        if self.app_config.logout_hotdesk_on_disable and user_change_detail.is_disabling:
            try:
                self._logout_user_hotdesks_by_number(user_change_detail.Number)
            except UserHotdeskLogoutError as e:
                self.logger.log(LogLevel.ERROR, str(e))
            except UserHotdeskLookupError as e:
                self.logger.log(LogLevel.ERROR, str(e))

    @handle_interupts
    def _logout_user_hotdesks_by_number(self, user_number: str) -> None:
        hotdesk_user_collection_response = self.users_resource.get_hotdesks_by_assigned_user_number(
            user_number=user_number
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

    def run(self):
        self.initialize_sync_source()
        self.source_user_list = self.sync_source.get_source_users()
        self.tcx_user_list = self.get_users()

        # Create a UserComparer object to compare users from the source and 3CX
        user_comparer = self.initialize_user_comparer()
        user_change_details = user_comparer.get_user_change_details()
        user_change_details.sort(key=lambda x: x.user_to_update.Number)

        # Perform User Updates
        self.handle_users_to_update(user_change_details)

        # Perform User Creates
        users_to_create = user_comparer.get_users_to_create()
        self.handle_users_to_create(users_to_create)
        self.logger.log(LogLevel.INFO, "Sync Complete")

    def terminate(self):
        self.terminate_event.set()  # Set to True

    def _handle_interupts(self):
        if self.is_terminated:
            raise ThreadTermination("Sync terminated by user")
        if self.is_paused:
            self.logger.log(LogLevel.INFO, "Paused by user")
        self.running_event.wait()  # Block thread if False


def run_sync(
    sync_source_class: SyncSourceStrategy,
    logger: SyncLogger,
    on_sync_initialized: Optional[Callable[[Sync], None]] = None,
    **kwargs,
):
    """
    Runs the synchronization process using the provided sync source strategy and logger.

    Args:
        sync_source (SyncSourceStrategy): The strategy to use for syncing data.
        logger (SyncLogger): The logger to use for logging messages.
        on_sync_initialized (callable[[Sync], None], optional):
            A callback function that is called once the sync is initialized.
            The function receives a `Sync` instance as its argument.
            Defaults to None.

    Raises:
        APIAuthenticationError: If there is an authentication error with the API.
        Exception: For any other exceptions that occur during the sync process.
    """
    try:
        logger.log(LogLevel.INFO, "=" * 40)
        logger.log(LogLevel.INFO, "Initializing Sync")
        app_config = initialize_app_config(logger=logger, config_path=kwargs.get("config_path"))
        api_connection = initialize_api_connection(app_config, logger)
        sync_source = build_sync_source(sync_source_class, logger, **kwargs)
        sync = Sync(api_connection, app_config, sync_source, logger)

        # Call callback if provided
        if on_sync_initialized:
            on_sync_initialized(sync)
        sync.run()
    except APIAuthenticationError:
        logger.log(LogLevel.ERROR, "Failed to sync. Unable to authenticate.")
    except Exception as e:
        logger.log(LogLevel.ERROR, f"Failed to sync. {e}")


def build_sync_source(sync_source_class: type[SyncSourceStrategy], logger: SyncLogger, **kwargs):
    logger.log(LogLevel.INFO, "Initializing Sync Source")
    sync_source = create_sync_source(strategy_class=sync_source_class, logger=logger, **kwargs)
    logger.log(LogLevel.INFO, "Sync Source Initialized")
    return sync_source


def initialize_app_config(logger: SyncLogger, **kwargs):
    logger.log(LogLevel.INFO, "Loading App Config")
    app_config = AppConfig(config_path=kwargs.get("config_path"))
    app_config.load()
    logger.log(LogLevel.INFO, "App Config Loaded")
    return app_config


def initialize_api_connection(app_config, logger):
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
