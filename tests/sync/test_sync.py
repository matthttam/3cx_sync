import pytest
from unittest.mock import MagicMock, patch, call
from sync.sync import Sync, run_sync, get_api_connection
from sync.logging import SyncLogger, LogLevel
from sync.sync_strategy import SyncSourceStrategy
from tcx_api.resources.users import UsersResource
from sync.comparison import UserChangeDetail, FieldChange
from tcx_api.components.schemas.pbx import User
from app.config import AppConfig
from tcx_api.tcx_api_connection import TCX_API_Connection
from tcx_api.exceptions import APIAuthenticationError
from tcx_api.resources.exceptions.users_exceptions import (
    UserCreateError,
    UserUpdateError,
    UserListError,
    UserHotdeskLogoutError,
    UserHotdeskLookupError,
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
        sync.logout_user_hotdesks_on_disable = MagicMock()
        sync.users_resource = MagicMock(spec=UsersResource)

        # Attempt to udpate user
        sync.update_user(user_change_detail)

        # Confirm appropriate logs were made and user was updated.
        mock_logger.log.assert_any_call(LogLevel.INFO, "Updating 3CX user 123")
        mock_logger.log.assert_any_call(LogLevel.INFO, f"Changing {str(user_change_detail)}")
        sync.users_resource.update_user.assert_called_once_with(user_change_detail.user_to_update)
        sync.logout_user_hotdesks_on_disable.assert_called_once_with(user_change_detail)

    def test_update_user_with_error(self, sync, mock_logger, user_change_detail):
        sync.logout_user_hotdesks_on_disable = MagicMock()
        sync.users_resource = MagicMock(spec=UsersResource)

        # Setup UserUpdateError
        error = UserUpdateError("Failed to update user.", user_change_detail.user_to_update)
        sync.users_resource.update_user.side_effect = error

        # Attempt to udpate user
        sync.update_user(user_change_detail)

        # Confirm appropriate logs were made
        sync.users_resource.update_user.assert_called_once_with(user_change_detail.user_to_update)
        mock_logger.log.assert_any_call(LogLevel.ERROR, str(error))
        sync.logout_user_hotdesks_on_disable.assert_not_called()

    def test_logout_user_hotdesks_on_disable(self, sync, user_change_detail, user_number):
        sync.app_config.logout_hotdesk_on_disable = True
        user_change_detail.field_changes = {"Enabled": FieldChange(old=True, new=False)}
        sync._logout_user_hotdesks_by_number = MagicMock()

        # Run the logout
        sync.logout_user_hotdesks_on_disable(user_change_detail)

        sync._logout_user_hotdesks_by_number.assert_called_once_with(user_number)
        sync.logger.assert_not_called()
    
    def test_logout_user_hotdesks_on_disable_logout_error(self, sync, user_change_detail, user_number, user_id):
        error = UserHotdeskLogoutError("Failed to logout hotdesk of user.", user_id)
        sync.app_config.logout_hotdesk_on_disable = True
        user_change_detail.field_changes = {"Enabled": FieldChange(old=True, new=False)}
        sync._logout_user_hotdesks_by_number = MagicMock(side_effect=error)
        # Run the logout
        sync.logout_user_hotdesks_on_disable(user_change_detail)
        sync._logout_user_hotdesks_by_number.assert_called_once_with(user_number)
        sync.logger.log.assert_called_once_with(LogLevel.ERROR, (
            f'Unable to clear hotdesking assignment of hotdesk with ID {user_id}'
            ' out of assigned hotdesk. HTTP Error: Failed to logout hotdesk of user.'
            )
        )

    def test_logout_user_hotdesks_on_disable_lookup_error(self, sync, user_change_detail, user_number):
        error = UserHotdeskLookupError("Failed to lookup hotdesk of user.", user_number)
        sync.app_config.logout_hotdesk_on_disable = True
        user_change_detail.field_changes = {"Enabled": FieldChange(old=True, new=False)}
        sync._logout_user_hotdesks_by_number = MagicMock(side_effect=error)
        # Run the logout
        sync.logout_user_hotdesks_on_disable(user_change_detail)
        sync._logout_user_hotdesks_by_number.assert_called_once_with(user_number)
        sync.logger.log.assert_called_once_with(LogLevel.ERROR, (
            f'Unable to retrieve hotdesks for user with number {user_number}.'
            ' HTTP Error: Failed to lookup hotdesk of user.'
            )
        )
    
    def test_logout_user_hotdesks_by_number(self, sync, user_number):
        # Hotdesks are themselves a type of user
        mock_hotdesk_users = [MagicMock(spec=User, Number="HD1111"), MagicMock(spec=User, Number="HD2222")]
        sync.users_resource = MagicMock(spec=UsersResource)
        sync.users_resource.get_hotdesks_by_assigned_user_number.return_value = mock_hotdesk_users
        # Run logout by number
        sync._logout_user_hotdesks_by_number(user_number)
        sync.users_resource.get_hotdesks_by_assigned_user_number.assert_called_once_with(user_number=user_number)
        assert sync.users_resource.clear_hotdesk_assignment.call_count == len(mock_hotdesk_users)
        sync.logger.log.assert_has_calls(
            [call(LogLevel.INFO, f"Logging user {user_number} out of hotdesk HD1111"),
             call(LogLevel.INFO, f"Logging user {user_number} out of hotdesk HD2222")]
             )

    def test_logout_user_hotdesks_by_number_none(self, sync, user_number):
        # Hotdesks are themselves a type of user
        sync.users_resource = MagicMock(spec=UsersResource)
        sync.users_resource.get_hotdesks_by_assigned_user_number.return_value = []
        # Run logout by number
        sync._logout_user_hotdesks_by_number(user_number)
        sync.users_resource.get_hotdesks_by_assigned_user_number.assert_called_once_with(user_number=user_number)
        assert sync.users_resource.clear_hotdesk_assignment.call_count == 0
        sync.logger.log.assert_called_once_with(
            LogLevel.INFO, f"User {user_number} is being disabled. No hotdesk logout required as the user is not signed in to any hotdesk."
        )

    def test_sync(self, sync):
        # Mock the methods
        sync.initialize_sync_source = MagicMock()
        sync.sync_source.get_source_users = MagicMock(return_value=[])
        sync.get_users = MagicMock(return_value=[])
        sync.initialize_user_comparer = MagicMock()
        sync.handle_users_to_update = MagicMock()
        sync.handle_users_to_create = MagicMock()

        # Call the sync method
        sync.sync()

        # Assert that each method is called once (or multiple times as expected)
        sync.initialize_sync_source.assert_called_once()
        sync.sync_source.get_source_users.assert_called_once()
        sync.get_users.assert_called_once()
        sync.initialize_user_comparer.assert_called_once()
        sync.handle_users_to_update.assert_called_once()
        sync.handle_users_to_create.assert_called_once()

        # Assert that the log is called with the expected message
        sync.logger.log.assert_any_call(LogLevel.INFO, "Sync Complete")

    def test_run_sync(self, mock_sync_source, mock_logger):
        with patch('sync.sync.get_app_config') as mock_get_app_config, \
             patch('sync.sync.get_api_connection') as mock_get_api_connection, \
             patch('sync.sync.Sync') as mock_sync_class:

            mock_app_config = MagicMock()
            mock_api_connection = MagicMock()
            mock_sync_instance = MagicMock()

            mock_get_app_config.return_value = mock_app_config
            mock_get_api_connection.return_value = mock_api_connection
            mock_sync_class.return_value = mock_sync_instance

            run_sync(mock_sync_source, mock_logger)

            mock_logger.log.assert_any_call(LogLevel.INFO, "Initializing Sync")
            mock_get_app_config.assert_called_once_with(mock_logger)
            mock_get_api_connection.assert_called_once_with(mock_app_config, mock_logger)
            mock_sync_class.assert_called_once_with(mock_api_connection, mock_app_config, mock_sync_source(mock_logger), mock_logger)
            mock_sync_instance.sync.assert_called_once()


def test_run_sync_authentication_error(mock_sync_source, mock_logger):
    with patch('sync.sync.get_app_config') as mock_get_app_config, \
            patch('sync.sync.get_api_connection') as mock_get_api_connection, \
            patch('sync.sync.Sync') as mock_sync_class:
        error = APIAuthenticationError(MagicMock())
        mock_get_app_config = MagicMock()
        mock_get_api_connection.side_effect = error

        run_sync(mock_sync_source, mock_logger)

        mock_logger.log.assert_any_call(LogLevel.INFO, "Initializing Sync")
        mock_logger.log.assert_any_call(LogLevel.ERROR, "Failed to sync. Unable to authenticate.")

        # Sync is not created and sync method is not called
        mock_sync_class.assert_not_called()
        mock_sync_class.sync.assert_not_called()


def test_run_sync_any_error(mock_sync_source, mock_logger):
    with patch('sync.sync.get_app_config') as mock_get_app_config, \
            patch('sync.sync.get_api_connection') as mock_get_api_connection, \
            patch('sync.sync.Sync') as mock_sync_class:
        error = Exception(MagicMock())
        mock_get_app_config.side_effect = MagicMock()
        mock_get_api_connection.side_effect = error

        run_sync(mock_sync_source, mock_logger)

        mock_logger.log.assert_any_call(LogLevel.INFO, "Initializing Sync")
        mock_logger.log.assert_any_call(LogLevel.ERROR, f"Failed to sync. {error}")

        # Sync is not created and sync method is not called
        mock_sync_class.assert_not_called()
        mock_sync_class.sync.assert_not_called()


def test_run_sync_general_exception(mock_sync_source, mock_logger):
    with patch('sync.sync.get_app_config') as mock_get_app_config, \
            patch('sync.sync.get_api_connection') as mock_get_api_connection, \
            patch('sync.sync.Sync') as mock_sync_class:

        mock_get_app_config.side_effect = Exception("General error")

        run_sync(mock_sync_source, mock_logger)

        mock_logger.log.assert_any_call(LogLevel.INFO, "Initializing Sync")
        mock_logger.log.assert_any_call(LogLevel.ERROR, "Failed to sync. General error")
        mock_get_app_config.assert_called_once_with(mock_logger)
        mock_get_api_connection.assert_not_called()
        mock_sync_class.assert_not_called()


def test_get_api_connection(mock_app_config, mock_logger):
    with patch('sync.sync.TCX_API_Connection') as mock_tcx_api_connection_class:
        mock_api_connection_instance = MagicMock()
        mock_tcx_api_connection_class.return_value = mock_api_connection_instance

        mock_app_config.server_url = "http://example.com"
        mock_app_config["3cx"].get.side_effect = lambda key: {"username": "user", "password": "pass"}[key]

        api_connection = get_api_connection(mock_app_config, mock_logger)

        mock_logger.log.assert_any_call(LogLevel.INFO, "Initializing API Connection")
        mock_logger.log.assert_any_call(LogLevel.INFO, "API Connection Initialized")
        mock_logger.log.assert_any_call(LogLevel.INFO, "Authenticating to 3CX at http://example.com")
        mock_logger.log.assert_any_call(LogLevel.INFO, "Authentication Successful")

        mock_tcx_api_connection_class.assert_called_once_with(server_url="http://example.com")
        mock_api_connection_instance.authenticate.assert_called_once_with(username="user", password="pass")
        assert api_connection == mock_api_connection_instance


def test_get_api_connection_authentication_error(mock_app_config, mock_logger):
    with patch('sync.sync.TCX_API_Connection') as mock_tcx_api_connection_class:
        mock_api_connection = MagicMock()
        mock_tcx_api_connection_class.return_value = mock_api_connection

        mock_app_config.server_url = "http://example.com"
        mock_app_config["3cx"].get.side_effect = lambda key: {"username": "user", "password": "pass"}[key]

        error = APIAuthenticationError(MagicMock())
        mock_api_connection.authenticate.side_effect = error

        with pytest.raises(APIAuthenticationError):
            get_api_connection(mock_app_config, mock_logger)

        mock_logger.log.assert_has_calls([
            call(LogLevel.INFO, "Initializing API Connection"),
            call(LogLevel.INFO, "API Connection Initialized"),
            call(LogLevel.INFO, "Authenticating to 3CX at http://example.com"),
            call(LogLevel.ERROR, f"Failed to authenticate: {error}")
        ])

        mock_tcx_api_connection_class.assert_called_once_with(server_url="http://example.com")
        mock_api_connection.authenticate.assert_called_once_with(username="user", password="pass")