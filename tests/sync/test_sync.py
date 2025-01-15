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


@pytest.fixture
def user_id():
    return 123

@pytest.fixture
def user_number():
    return "123"

@pytest.fixture
def user(user_id, user_number):
    return User.model_construct(Id=user_id, Number=user_number, PrimaryGroupId=None, Groups=[])


@pytest.fixture
def user_dict(user):
    return user.model_dump()


@pytest.fixture
def new_user_dict():
    return {"Id": None, "Number": "", "PrimaryGroupId": None, "Groups": []}


@pytest.fixture
def user_change_detail(user):
    return UserChangeDetail(user_to_update=user, field_changes={})


class TestSync:

    def test_initialize_sync_source(self, sync, mock_logger):
        sync.initialize_sync_source()
        mock_logger.log.assert_any_call(LogLevel.INFO, "Initializing Sync Source")
        sync.sync_source.initialize.assert_called_once()

    def test_get_users(self, sync, mock_logger):
        mock_users = [MagicMock(spec=User) for _ in range(3)]
        sync.users_resource = MagicMock()
        sync.users_resource.list_user.return_value = mock_users
        users = sync.get_users()
        mock_logger.log.assert_any_call(LogLevel.INFO, "Fetching Users From 3CX")
        mock_logger.log.assert_any_call(LogLevel.INFO, f"Fetched {len(users)} Users From 3CX")
        assert users == mock_users

    def test_get_users_error(self, sync, mock_logger):
        sync.users_resource = MagicMock()
        error = UserListError("Unable to retrieve users.")
        sync.users_resource.list_user.side_effect = error
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

    def test_get_new_user(self, sync, user_dict):
        primary_group_id = 100

        # Setup Expected User
        expected_user = user_dict.copy()
        expected_user["PrimaryGroupId"] = primary_group_id
        expected_user["Groups"] = [{"GroupId": primary_group_id, "Rights": {"RoleName": "users"}}]

        # Mock user and group resources
        sync.users_resource = MagicMock(get_new_user=MagicMock(return_value=user_dict))
        default_group = MagicMock(Id=primary_group_id)
        sync.groups_resource = MagicMock(get_default_group=MagicMock(return_value=default_group))       

        # Get New User
        user_dict = sync.get_new_user()

        # Confirm it is as expected and default group was called.
        sync.groups_resource.get_default_group.assert_called_once()
        assert user_dict == expected_user
        assert user_dict["PrimaryGroupId"] == default_group.Id
        assert user_dict["Groups"] == [{"GroupId": default_group.Id, "Rights": {"RoleName": "users"}}]

    def test_create_users(self, sync):
        mock_users = [MagicMock(spec=User) for _ in range(2)]
        sync.create_user = MagicMock()
        sync.create_users(mock_users)
        assert sync.create_user.call_count == len(mock_users)

    def test_create_user(self, sync, mock_logger, user_number, new_user_dict, user):        
        # Setup Expected User
        expected_user_dict = new_user_dict | user.model_dump()

        # Mock users resource and get_new_user
        sync.users_resource = MagicMock(spec=UsersResource)
        sync.get_new_user = MagicMock(return_value=new_user_dict)

        # Create User
        sync.create_user(user)

        # Confirm appropriate logs were made and user was created.
        sync.users_resource.create_user.assert_called_once_with(expected_user_dict)
        mock_logger.log.assert_any_call(LogLevel.INFO, f"Creating 3CX user {user_number}")
        mock_logger.log.assert_any_call(LogLevel.INFO, f"Created 3CX user {user_number}")

    def test_create_user_with_error(self, sync, mock_logger, user_number, new_user_dict, user):
        """Test create_user method with UserCreateError logs error but doesn't raise exception."""

        # Setup Expected User
        expected_user_dict = new_user_dict | user.model_dump()

        # Mock users resource and get_new_user
        sync.users_resource = MagicMock(spec=UsersResource)
        sync.get_new_user = MagicMock(return_value=new_user_dict)

        # Setup UserCreateError
        error = UserCreateError("Failed to create user.", expected_user_dict)
        sync.users_resource.create_user.side_effect = error

        # Create User
        sync.create_user(user)

        # Confirm appropriate logs were made
        unexpected_call = call(LogLevel.INFO, f"Created 3CX user {user_number}")
        assert unexpected_call not in mock_logger.log.call_args_list
        mock_logger.log.assert_any_call(LogLevel.ERROR, str(error))

    def test_update_users(self, sync):
        mock_user_change_details = [MagicMock(spec=UserChangeDetail) for _ in range(2)]
        sync.update_user = MagicMock()
        sync.update_users(mock_user_change_details)
        assert sync.update_user.call_count == len(mock_user_change_details)

    def test_update_user(self, sync, mock_logger, user_change_detail):
        sync.handle_logout_hotdesk_on_disable = MagicMock()
        sync.users_resource = MagicMock(spec=UsersResource)

        # Attempt to udpate user
        sync.update_user(user_change_detail)

        # Confirm appropriate logs were made and user was updated.
        mock_logger.log.assert_any_call(LogLevel.INFO, "Updating 3CX user 123")
        mock_logger.log.assert_any_call(LogLevel.INFO, f"Changing {str(user_change_detail)}")
        sync.users_resource.update_user.assert_called_once_with(user_change_detail.user_to_update)
        sync.handle_logout_hotdesk_on_disable.assert_called_once_with(user_change_detail)

    def test_update_user_with_error(self, sync, mock_logger, user_change_detail):
        sync.handle_logout_hotdesk_on_disable = MagicMock()
        sync.users_resource = MagicMock(spec=UsersResource)

        # Setup UserUpdateError
        error = UserUpdateError("Failed to update user.", user_change_detail.user_to_update)
        sync.users_resource.update_user.side_effect = error

        # Attempt to udpate user
        sync.update_user(user_change_detail)

        # Confirm appropriate logs were made
        sync.users_resource.update_user.assert_called_once_with(user_change_detail.user_to_update)
        mock_logger.log.assert_any_call(LogLevel.ERROR, str(error))
        sync.handle_logout_hotdesk_on_disable.assert_not_called()

    def test_handle_logout_hotdesk_on_disable(self, sync, mock_app_config, user_change_detail):
        # Arrange
        # Mock the app_config to return True for 'logout_hotdesk_on_disable'
        mock_app_config["app"].get.return_value = True

        # Set up a field change where 'Enabled' is changed to False
        user_change_detail.field_changes = {
            "Enabled": MagicMock(new=False)
        }

        # Mock the 'log_user_out_of_assigned_hotdesks_by_number' method
        sync.log_user_out_of_assigned_hotdesks_by_number = MagicMock()

        # Act
        sync.handle_logout_hotdesk_on_disable(user_change_detail)

        # Assert
        # Check that 'log_user_out_of_assigned_hotdesks_by_number' was called with the correct user number
        sync.log_user_out_of_assigned_hotdesks_by_number.assert_called_once_with(user_change_detail.Number)
        # Ensure the app_config's get method was called correctly
        mock_app_config["app"].get.assert_called_once_with("logout_hotdesk_on_disable", False)


    def test_log_user_out_of_assigned_hotdesks_by_number(self, sync, mock_logger):
        user_number = "123"
        mock_hotdesk_user = MagicMock()
        sync.users_resource.get_hotdesks_by_assigned_user_number = MagicMock(return_value=[mock_hotdesk_user])
        sync.users_resource.clear_hotdesk_assignment = MagicMock()
        sync.log_user_out_of_assigned_hotdesks_by_number(user_number)
        mock_logger.log.assert_any_call(LogLevel.INFO, f"Logging user {user_number} out of hotdesk {mock_hotdesk_user.Number}")
        sync.users_resource.clear_hotdesk_assignment.assert_called_with(mock_hotdesk_user)

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
