import pytest
from unittest.mock import MagicMock, patch, call
from sync.sync import Sync, run_sync
from sync.logging import SyncLogger, LogLevel
from sync.sync_strategy import SyncSourceStrategy
from tcx_api.resources.users import UsersResource
from tcx_api.resources.groups import GroupsResource
from sync.comparison import UserChangeDetail
from tcx_api.components.schemas.pbx import User
from app.config import AppConfig
from tcx_api.tcx_api_connection import TCX_API_Connection
from tcx_api.resources.exceptions.users_exceptions import (
    UserCreateError,
    UserUpdateError,
    UserListError,
    UserHotdeskLogoutError,
)

@pytest.fixture
def mock_app_config():
    return MagicMock(spec=AppConfig)


@pytest.fixture
def mock_api_connection():
    return MagicMock(spec=TCX_API_Connection)


@pytest.fixture
def mock_logger():
    return MagicMock(spec=SyncLogger)


@pytest.fixture
def mock_sync_source():
    return MagicMock(spec=SyncSourceStrategy)


@pytest.fixture
def sync(mock_app_config, mock_api_connection, mock_logger, mock_sync_source):
    return Sync(mock_api_connection, mock_app_config, mock_sync_source, mock_logger)


class TestSync:

    def test_initialize_sync_source(self, sync, mock_logger):
        sync.initialize_sync_source()
        mock_logger.log.assert_any_call(LogLevel.INFO, "Initializing Sync Source")
        sync.sync_source.initialize.assert_called_once()

    def test_get_users(self, sync, mock_logger):
        mock_users = [MagicMock(spec=User) for _ in range(3)]
        sync.user_resource = MagicMock()
        sync.user_resource.list_user.return_value = mock_users
        users = sync.get_users()
        mock_logger.log.assert_any_call(LogLevel.INFO, "Fetching Users From 3CX")
        mock_logger.log.assert_any_call(LogLevel.INFO, f"Fetched {len(users)} Users From 3CX")
        assert users == mock_users

    def test_get_users_error(self, sync, mock_logger):
        sync.user_resource = MagicMock()
        error = UserListError("Unable to retrieve users.")
        sync.user_resource.list_user.side_effect = error
        with pytest.raises(UserListError):
            sync.get_users()
        mock_logger.log.assert_any_call(LogLevel.INFO, "Fetching Users From 3CX")
        mock_logger.log.assert_any_call(LogLevel.ERROR, f"Failed to Fetch Users: {error}")

    def test_handle_users_to_update(self, sync, mock_logger):
        mock_user_change_details = [MagicMock(spec=UserChangeDetail, field_changes={}) for _ in range(2)]
        sync.update_users = MagicMock()
        sync.handle_users_to_update(mock_user_change_details)
        mock_logger.log.assert_any_call(LogLevel.INFO, f"Count of users to update: {len(mock_user_change_details)}")
        sync.update_users.assert_called_once_with(user_change_details=mock_user_change_details)

    def test_handle_users_to_update_no_users(self, sync, mock_logger):
        mock_user_change_details = []
        sync.update_users = MagicMock()
        sync.handle_users_to_update(mock_user_change_details)
        unexpected_call = call(LogLevel.INFO, f"Count of users to update: {len(mock_user_change_details)}")
        assert unexpected_call not in mock_logger.log.call_args_list
        sync.update_users.assert_not_called()
        mock_logger.log.assert_any_call(LogLevel.INFO, "No users to update.")

    def test_handle_users_to_create(self, sync, mock_logger):
        mock_users_to_create = [MagicMock(spec=User) for _ in range(2)]
        sync.create_users = MagicMock()
        sync.handle_users_to_create(mock_users_to_create)
        mock_logger.log.assert_any_call(LogLevel.INFO, f"Count of users to create: {len(mock_users_to_create)}")
        sync.create_users.assert_called_once_with(users=mock_users_to_create)

    def test_handle_users_to_create_no_users(self, sync, mock_logger):
        mock_users_to_create = []
        sync.create_users = MagicMock()
        sync.handle_users_to_create(mock_users_to_create)
        unexpected_call = call(LogLevel.INFO, f"Count of users to create: {len(mock_users_to_create)}")
        assert unexpected_call not in mock_logger.log.call_args_list
        sync.create_users.assert_not_called()
        mock_logger.log.assert_any_call(LogLevel.INFO, "No users to create.")

    def test_initialize_user_comparer(self, sync):
        sync.tcx_user_list = MagicMock()
        sync.sync_source = MagicMock()
        comparer = sync.initialize_user_comparer()
        assert comparer.tcx_user_list == sync.tcx_user_list
        assert comparer.sync_source == sync.sync_source

    def test_pause_sync(self, sync):
        sync.pause_sync()
        assert not sync.running_event.is_set()

    def test_resume_sync(self, sync):
        sync.resume_sync()
        assert sync.running_event.is_set()

    def test_get_new_user(self, sync):
        sync.user_resource = MagicMock()
        sync.group_resource = MagicMock()
        new_user = MagicMock()
        default_group = MagicMock()
        sync.group_resource.get_default_group.return_value = default_group
        sync.user_resource.get_new_user.return_value = new_user
        user = sync.get_new_user()
        assert user == new_user
        sync.group_resource.get_default_group.assert_called_once()
        assert user["PrimaryGroupId"] == default_group.Id
        assert user["Groups"] == [{"GroupId": default_group.Id, "Rights": {"RoleName": "users"}}]

    def test_create_users(self, sync):
        mock_users = [MagicMock(spec=User) for _ in range(2)]
        sync.create_user = MagicMock()
        sync.create_users(mock_users)
        assert sync.create_user.call_count == len(mock_users)

    def test_create_user(self, sync, mock_logger):
        mock_user = MagicMock(spec=User)
        mock_user.Number = "123"
        sync.user_resource = MagicMock(spec=UsersResource)
        sync.group_resource = MagicMock(spec=GroupsResource)
        sync.create_user(mock_user)
        mock_logger.log.assert_any_call(LogLevel.INFO, "Creating 3CX user 123")

    def test_update_users(self, sync):
        mock_user_change_details = [MagicMock(spec=UserChangeDetail) for _ in range(2)]
        sync.update_user = MagicMock()
        sync.update_users(mock_user_change_details)
        assert sync.update_user.call_count == len(mock_user_change_details)

    def test_update_user(self, sync, mock_logger):
        mock_user_change_detail = MagicMock(spec=UserChangeDetail)
        mock_user_change_detail.Number = "123"
        sync.user_resource = MagicMock(spec=UsersResource)
        sync.update_user(mock_user_change_detail)
        mock_logger.log.assert_any_call(LogLevel.INFO, "Updating 3CX user 123")

    def test_handle_logout_hotdesk_on_disable(self, sync, mock_logger):
        mock_user_change_detail = MagicMock(spec=UserChangeDetail)
        mock_user_change_detail.field_changes = {"Enabled": MagicMock(new=False)}
        mock_user_change_detail.Number = "123"
        sync.user_resource = MagicMock(spec=UsersResource)
        sync.log_user_out_of_assigned_hotdesks_by_number = MagicMock()
        sync.handle_logout_hotdesk_on_disable(mock_user_change_detail)
        sync.log_user_out_of_assigned_hotdesks_by_number.assert_called_with("123")

    def test_log_user_out_of_assigned_hotdesks_by_number(self, sync, mock_logger):
        user_number = "123"
        mock_hotdesk_user = MagicMock()
        sync.user_resource.get_hotdesks_by_assigned_user_number = MagicMock(return_value=[mock_hotdesk_user])
        sync.user_resource.clear_hotdesk_assignment = MagicMock()
        sync.log_user_out_of_assigned_hotdesks_by_number(user_number)
        mock_logger.log.assert_any_call(LogLevel.INFO, f"Logging user {user_number} out of hotdesk {mock_hotdesk_user.Number}")
        sync.user_resource.clear_hotdesk_assignment.assert_called_with(mock_hotdesk_user)

    def test_sync(self, sync, mock_logger):
        sync.initialize_sync_source = MagicMock()
        sync.sync_source.get_source_users = MagicMock(return_value=[])
        sync.get_users = MagicMock(return_value=[])
        sync.initialize_user_comparer = MagicMock()
        sync.handle_users_to_update = MagicMock()
        sync.handle_users_to_create = MagicMock()
        sync.sync()
        mock_logger.log.assert_any_call(LogLevel.INFO, "Sync Complete")

    def test_run_sync(self, mock_logger, mock_sync_source):
        with patch('sync.sync.Sync') as mock_sync:
            run_sync(mock_sync_source, mock_logger)
            mock_sync.assert_called_once()
            mock_sync.return_value.sync.assert_called_once()

    # def test_get_app_config(self, mock_logger):
    #     with patch('sync.sync.AppConfig') as mock_app_config:
    #         app_config = get_app_config(mock_logger)
    #         mock_app_config.assert_called_once()
    #         mock_logger.log.assert_any_call(LogLevel.INFO, "App Config Loaded")
    #         assert app_config == mock_app_config.return_value
# 
    # def test_get_api_connection(self, mock_logger, mock_app_config):
    #     with patch('sync.sync.TCX_API_Connection') as mock_api_connection:
    #         api_connection = get_api_connection(mock_app_config, mock_logger)
    #         mock_api_connection.assert_called_once_with(server_url=mock_app_config.server_url)
    #         mock_logger.log.assert_any_call(LogLevel.INFO, "API Connection Initialized")
    #         assert api_connection == mock_api_connection.return_value


class TestSyncOLD:

    def test_sync_initialization(self, sync):
        sync.sync()
        sync.logger.log.assert_any_call(LogLevel.INFO, "Initializing Sync")

    def test_load_app_config(self, sync, mock_logger):
        sync.load_app_config()
        mock_logger.log.assert_any_call(LogLevel.INFO, "Loading App Config")
        mock_logger.log.assert_any_call(LogLevel.INFO, "App Config Loaded")

    def test_create_user(self, sync, mock_logger):
        mock_user = MagicMock(spec=User)
        mock_user.Number = "123"
        sync.user_resource = MagicMock(spec=UsersResource)
        sync.group_resource = MagicMock(spec=GroupsResource)
        sync.create_user(mock_user)
        mock_logger.log.assert_any_call(LogLevel.INFO, "Creating 3CX user 123")

    def test_update_user(self, sync, mock_logger):
        mock_user_change_detail = MagicMock(spec=UserChangeDetail)
        mock_user_change_detail.Number = "123"
        sync.user_resource = MagicMock(spec=UsersResource)
        sync.update_user(mock_user_change_detail)
        mock_logger.log.assert_any_call(LogLevel.INFO, "Updating 3CX user 123")

    def test_handle_logout_hotdesk_on_disable(self, sync, mock_logger):
        mock_user_change_detail = MagicMock(spec=UserChangeDetail)
        mock_user_change_detail.field_changes = {"Enabled": MagicMock(new=False)}
        mock_user_change_detail.Number = "123"
        sync.user_resource = MagicMock(spec=UsersResource)
        sync.log_user_out_of_assigned_hotdesks_by_number = MagicMock()
        sync.handle_logout_hotdesk_on_disable(mock_user_change_detail)
        sync.log_user_out_of_assigned_hotdesks_by_number.assert_called_with("123")

    def test_run_sync(self, mock_logger, mock_sync_source):
        with patch('sync.sync.Sync') as mock_sync:
            run_sync(mock_logger, mock_sync_source)
            mock_sync.assert_called_once()
            mock_sync.return_value.sync.assert_called_once()